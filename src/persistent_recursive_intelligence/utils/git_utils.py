#!/usr/bin/env python3
"""
Git utilities for PRI - handle git operations for diff analysis
"""

import subprocess
import os
from pathlib import Path
from typing import List, Set, Optional
import logging

logger = logging.getLogger(__name__)


class GitRepo:
    """Handle git repository operations for PRI analysis"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path).resolve()
        self._validate_git_repo()
    
    def _validate_git_repo(self):
        """Check if the path is a git repository"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            logger.debug(f"Git repo validated: {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            raise ValueError(f"Not a git repository: {self.repo_path}")
    
    def get_changed_files(self, since_commit: Optional[str] = None, staged_only: bool = False) -> Set[Path]:
        """Get list of changed files in the repository
        
        Args:
            since_commit: Compare against this commit (default: working dir vs HEAD)
            staged_only: Only include staged changes
            
        Returns:
            Set of absolute paths to changed files
        """
        try:
            if staged_only:
                # Get staged changes only
                cmd = ['git', 'diff', '--cached', '--name-only']
            elif since_commit:
                # Compare against specific commit
                cmd = ['git', 'diff', '--name-only', since_commit]
            else:
                # Get all changes (staged + unstaged)
                cmd = ['git', 'diff', '--name-only', 'HEAD']
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            changed_files = set()
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    file_path = self.repo_path / line.strip()
                    if file_path.exists():  # File might be deleted
                        changed_files.add(file_path.resolve())
            
            logger.info(f"Found {len(changed_files)} changed files")
            return changed_files
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            return set()
    
    def get_untracked_files(self) -> Set[Path]:
        """Get list of untracked files"""
        try:
            result = subprocess.run(
                ['git', 'ls-files', '--others', '--exclude-standard'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            untracked_files = set()
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    file_path = self.repo_path / line.strip()
                    if file_path.exists():
                        untracked_files.add(file_path.resolve())
            
            return untracked_files
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            return set()
    
    def get_current_branch(self) -> str:
        """Get current branch name"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"
    
    def get_commit_hash(self, ref: str = "HEAD") -> str:
        """Get commit hash for a reference"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', ref],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()[:8]  # Short hash
        except subprocess.CalledProcessError:
            return "unknown"
    
    def get_files_in_commit_range(self, since_commit: str, until_commit: str = "HEAD") -> Set[Path]:
        """Get files changed between two commits"""
        try:
            cmd = ['git', 'diff', '--name-only', f"{since_commit}..{until_commit}"]
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            changed_files = set()
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    file_path = self.repo_path / line.strip()
                    if file_path.exists():
                        changed_files.add(file_path.resolve())
            
            return changed_files
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git commit range command failed: {e}")
            return set()


def filter_analyzable_files(files: Set[Path]) -> Set[Path]:
    """Filter to only include files that PRI can analyze"""
    analyzable_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
        '.cs', '.go', '.rs', '.php', '.rb', '.scala', '.kt', '.swift', '.lua'
    }
    
    return {f for f in files if f.suffix.lower() in analyzable_extensions}


def get_git_status_summary(repo: GitRepo) -> dict:
    """Get a summary of git repository status"""
    try:
        changed = repo.get_changed_files()
        untracked = repo.get_untracked_files()
        
        return {
            'branch': repo.get_current_branch(),
            'commit': repo.get_commit_hash(),
            'changed_files': len(changed),
            'untracked_files': len(untracked),
            'analyzable_changed': len(filter_analyzable_files(changed)),
            'analyzable_untracked': len(filter_analyzable_files(untracked))
        }
    except Exception as e:
        logger.error(f"Error getting git status: {e}")
        return {'error': str(e)}