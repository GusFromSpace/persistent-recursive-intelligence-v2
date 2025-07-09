# IDE Integration Guide - Mesopredator PRI

**Integrate advanced code analysis directly into your development environment**

---

## 🎯 Overview

Mesopredator PRI integrates seamlessly with popular IDEs to provide real-time code analysis, security scanning, and intelligent suggestions directly in your editor. This guide covers setup for VS Code, IntelliJ IDEA, and other major development environments.

---

## 📋 Table of Contents

1. [VS Code Integration](#vs-code-integration)
2. [IntelliJ IDEA Integration](#intellij-idea-integration)
3. [Vim/Neovim Integration](#vimneovim-integration)
4. [Emacs Integration](#emacs-integration)
5. [Language Server Protocol](#language-server-protocol)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)

---

## 💻 VS Code Integration

### 1. Official Extension Installation

#### Install from Marketplace
```bash
# Search for "Mesopredator PRI" in VS Code Extensions
# Or install via command line:
code --install-extension mesopredator.pri-vscode
```

#### Manual Installation (Development)
```bash
# Clone the extension repository
git clone https://github.com/mesopredator/pri-vscode-extension
cd pri-vscode-extension

# Install dependencies and build
npm install
npm run compile

# Package and install
vsce package
code --install-extension mesopredator-pri-*.vsix
```

### 2. Configuration

#### VS Code Settings (settings.json)
```json
{
  "mesopredator-pri": {
    "enabled": true,
    "apiEndpoint": "http://localhost:8000",
    "apiKey": "pk_live_your_api_key_here",
    "features": {
      "realTimeAnalysis": true,
      "securityScanning": true,
      "codeConnector": true,
      "memoryIntegration": true
    },
    "analysis": {
      "focusMode": "balanced",
      "maxDepth": 2,
      "enableLearning": true,
      "excludePatterns": [
        "**/node_modules/**",
        "**/venv/**",
        "**/.git/**"
      ]
    },
    "ui": {
      "showInlineHints": true,
      "highlightSeverity": "medium",
      "showProgressNotifications": true
    }
  }
}
```

### 3. Features & Usage

#### Real-time Code Analysis
- **Automatic Scanning**: Files analyzed on save
- **Inline Diagnostics**: Issues shown directly in editor
- **Quick Fixes**: Right-click for suggested fixes
- **Security Highlights**: Vulnerable code highlighted in real-time

#### Commands Available
```bash
# Open Command Palette (Ctrl+Shift+P) and search:
PRI: Analyze Current File
PRI: Analyze Entire Project
PRI: Search Memory Patterns
PRI: Code Connector Analysis
PRI: View Security Report
PRI: Train False Positive
PRI: Emergency Security Stop
```

#### Keyboard Shortcuts
```json
{
  "key": "ctrl+shift+p",
  "command": "mesopredator-pri.analyzeFile",
  "when": "editorTextFocus"
},
{
  "key": "ctrl+shift+m",
  "command": "mesopredator-pri.searchMemory",
  "when": "editorTextFocus"
},
{
  "key": "ctrl+shift+s",
  "command": "mesopredator-pri.securityScan",
  "when": "editorTextFocus"
}
```

### 4. Extension Features

#### Status Bar Integration
```
[PRI: Active] 🔍 23 issues | 🛡️ 2 security | 🧠 Learning
```

#### Problems Panel Integration
- Security issues marked with 🛡️
- Quality issues marked with 📊  
- Performance issues marked with ⚡
- Click to navigate to issue location

#### Hover Information
```typescript
// Hover over vulnerable code to see:
// 🛡️ Security Issue: SQL Injection Risk
// CWE-89: Improper Neutralization of Special Elements
// Confidence: 95%
// 💡 Quick Fix Available
```

---

## 🧠 IntelliJ IDEA Integration

### 1. Plugin Installation

#### JetBrains Marketplace
```bash
# In IntelliJ IDEA:
# File → Settings → Plugins → Marketplace
# Search: "Mesopredator PRI"
# Click Install and restart IDE
```

#### Manual Installation
```bash
# Download the plugin JAR from releases
# File → Settings → Plugins → Install Plugin from Disk
# Select the downloaded JAR file
```

### 2. Configuration

#### IntelliJ Settings
```xml
<!-- .idea/mesopredator-pri.xml -->
<component name="MesopredatorPRISettings">
  <option name="enabled" value="true" />
  <option name="apiEndpoint" value="http://localhost:8000" />
  <option name="apiKey" value="pk_live_your_api_key_here" />
  <option name="realTimeAnalysis" value="true" />
  <option name="securityFocus" value="true" />
  <option name="learningEnabled" value="true" />
  <option name="showTooltips" value="true" />
</component>
```

#### Project-specific Settings
```properties
# .idea/mesopredator-pri.properties
pri.project.focus=security
pri.analysis.depth=3
pri.memory.namespace=my_project
pri.exclude.patterns=target/**,build/**,*.class
```

### 3. Features

#### Code Inspections
- **Real-time Analysis**: Integrated with IntelliJ's inspection system
- **Custom Severity Levels**: Map PRI severities to IntelliJ warning levels
- **Batch Inspections**: Analyze entire project via "Analyze → Inspect Code"

#### Tool Windows
- **PRI Analysis**: Dedicated tool window showing all issues
- **Memory Patterns**: Browse and search learned patterns
- **Security Dashboard**: Overview of security findings

#### Quick Fixes & Intentions
```java
// Cursor on vulnerable code, press Alt+Enter to see:
// 🛡️ Fix SQL injection with parameterized query
// 📚 Learn about CWE-89
// 🔍 Search similar patterns
// ❌ Mark as false positive
```

#### Integration with Version Control
- **Pre-commit Hooks**: Scan changes before commit
- **Diff Analysis**: Analyze only modified files
- **Historical Tracking**: Track security improvements over time

---

## ⚡ Vim/Neovim Integration

### 1. Plugin Installation

#### Using vim-plug
```vim
" Add to your .vimrc or init.vim
Plug 'mesopredator/pri.vim'

" Install with:
:PlugInstall
```

#### Using packer.nvim (Neovim)
```lua
-- Add to your init.lua
use {
  'mesopredator/pri.nvim',
  config = function()
    require('pri').setup({
      api_endpoint = 'http://localhost:8000',
      api_key = 'pk_live_your_api_key_here',
      auto_analyze = true,
      show_diagnostics = true
    })
  end
}
```

### 2. Configuration

#### Vim Configuration (.vimrc)
```vim
" Mesopredator PRI Configuration
let g:pri_enabled = 1
let g:pri_api_endpoint = 'http://localhost:8000'
let g:pri_api_key = 'pk_live_your_api_key_here'
let g:pri_auto_analyze = 1
let g:pri_show_signs = 1

" Key mappings
nnoremap <leader>pa :PRIAnalyze<CR>
nnoremap <leader>pf :PRIAnalyzeFile<CR>
nnoremap <leader>pm :PRISearchMemory<CR>
nnoremap <leader>ps :PRISecurityScan<CR>
```

#### Neovim Configuration (init.lua)
```lua
require('pri').setup({
  api = {
    endpoint = 'http://localhost:8000',
    key = 'pk_live_your_api_key_here',
    timeout = 30000
  },
  features = {
    auto_analyze = true,
    show_diagnostics = true,
    inline_hints = true,
    security_focus = true
  },
  ui = {
    signs = {
      error = '🚨',
      warning = '⚠️',
      info = 'ℹ️',
      security = '🛡️'
    },
    virtual_text = true,
    highlight_groups = {
      PRIError = { fg = '#ff5555' },
      PRIWarning = { fg = '#ffb86c' },
      PRIInfo = { fg = '#8be9fd' },
      PRISecurity = { fg = '#ff79c6' }
    }
  }
})
```

### 3. Commands & Mappings

#### Available Commands
```vim
:PRIAnalyze          " Analyze current buffer
:PRIAnalyzeProject   " Analyze entire project  
:PRISearchMemory     " Search memory patterns
:PRISecurityScan     " Security-focused scan
:PRICodeConnector    " Analyze file connections
:PRIToggle           " Toggle PRI on/off
:PRIStatus           " Show analysis status
```

#### Integration with Popular Plugins

##### With COC.nvim
```json
// coc-settings.json
{
  "mesopredator-pri": {
    "enable": true,
    "apiEndpoint": "http://localhost:8000",
    "apiKey": "pk_live_your_api_key_here"
  }
}
```

##### With ALE
```vim
let g:ale_linters = {
\   'python': ['pri', 'pylint', 'flake8'],
\   'javascript': ['pri', 'eslint']
\}

let g:ale_fixers = {
\   'python': ['pri-fix', 'black'],
\   'javascript': ['pri-fix', 'prettier']
\}
```

---

## 📝 Emacs Integration

### 1. Package Installation

#### Using MELPA
```elisp
;; Add to your init.el
(require 'package)
(add-to-list 'package-archives
             '("melpa" . "https://melpa.org/packages/") t)

;; Install mesopredator-pri
M-x package-install RET mesopredator-pri RET
```

#### Manual Installation
```bash
# Clone the repository
git clone https://github.com/mesopredator/pri.el ~/.emacs.d/site-lisp/pri.el

# Add to load path in init.el
(add-to-list 'load-path "~/.emacs.d/site-lisp/pri.el")
(require 'mesopredator-pri)
```

### 2. Configuration

#### Emacs Configuration (init.el)
```elisp
;; Mesopredator PRI Configuration
(use-package mesopredator-pri
  :ensure t
  :config
  (setq mesopredator-pri-api-endpoint "http://localhost:8000"
        mesopredator-pri-api-key "pk_live_your_api_key_here"
        mesopredator-pri-auto-analyze t
        mesopredator-pri-show-flycheck-errors t)
  
  ;; Key bindings
  (global-set-key (kbd "C-c p a") 'mesopredator-pri-analyze-buffer)
  (global-set-key (kbd "C-c p p") 'mesopredator-pri-analyze-project)
  (global-set-key (kbd "C-c p m") 'mesopredator-pri-search-memory)
  (global-set-key (kbd "C-c p s") 'mesopredator-pri-security-scan)
  
  ;; Enable for programming modes
  (add-hook 'prog-mode-hook 'mesopredator-pri-mode))
```

### 3. Integration with Flycheck
```elisp
;; Add PRI as a Flycheck checker
(flycheck-define-checker mesopredator-pri
  "A code analyzer using Mesopredator PRI."
  :command ("pri-check" source-original)
  :error-patterns
  ((error line-start (file-name) ":" line ":" column ": error: " (message) line-end)
   (warning line-start (file-name) ":" line ":" column ": warning: " (message) line-end)
   (info line-start (file-name) ":" line ":" column ": info: " (message) line-end))
  :modes (python-mode js-mode java-mode))

(add-to-list 'flycheck-checkers 'mesopredator-pri)
```

---

## 🔌 Language Server Protocol (LSP)

### 1. PRI Language Server

#### Installation
```bash
# Install the PRI language server
npm install -g @mesopredator/pri-language-server

# Or via pip
pip install mesopredator-pri-langserver
```

#### Configuration
```json
{
  "server": {
    "command": "pri-langserver",
    "args": ["--stdio"],
    "environment": {
      "PRI_API_ENDPOINT": "http://localhost:8000",
      "PRI_API_KEY": "pk_live_your_api_key_here"
    }
  },
  "capabilities": {
    "textDocumentSync": "incremental",
    "hoverProvider": true,
    "diagnosticsProvider": true,
    "codeActionProvider": true,
    "completionProvider": {
      "triggerCharacters": ["."]
    }
  }
}
```

### 2. Client Setup

#### VS Code (Manual LSP)
```json
{
  "languageServerExample.enable": true,
  "languageServerExample.trace.server": "verbose",
  "languageServerExample.serverPath": "pri-langserver"
}
```

#### Neovim with nvim-lspconfig
```lua
local lspconfig = require('lspconfig')

lspconfig.pri_langserver.setup({
  cmd = { "pri-langserver", "--stdio" },
  filetypes = { "python", "javascript", "typescript", "java", "cpp" },
  root_dir = lspconfig.util.root_pattern(".git", "package.json", "pyproject.toml"),
  settings = {
    pri = {
      apiEndpoint = "http://localhost:8000",
      apiKey = "pk_live_your_api_key_here",
      enableAnalysis = true,
      securityFocus = true
    }
  }
})
```

#### Emacs with eglot
```elisp
(add-to-list 'eglot-server-programs
             '((python-mode js-mode java-mode) . ("pri-langserver" "--stdio")))
```

---

## 🚀 CI/CD Integration

### 1. GitHub Actions Integration

```yaml
name: PRI Code Analysis
on: [push, pull_request]

jobs:
  pri-analysis:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup PRI
      run: |
        pip install mesopredator-pri
        pri-server start --daemon
    
    - name: Run PRI Analysis
      run: |
        pri analyze . --output=sarif --file=pri-results.sarif
    
    - name: Upload SARIF results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: pri-results.sarif
```

### 2. GitLab CI Integration

```yaml
stages:
  - analysis

pri_analysis:
  stage: analysis
  image: python:3.9
  before_script:
    - pip install mesopredator-pri
  script:
    - pri analyze . --format=gitlab-ci
  artifacts:
    reports:
      codequality: pri-quality-report.json
    paths:
      - pri-analysis-results.json
```

### 3. Jenkins Integration

```groovy
pipeline {
    agent any
    
    stages {
        stage('PRI Analysis') {
            steps {
                sh 'pip install mesopredator-pri'
                sh 'pri analyze . --output=junit --file=pri-results.xml'
                
                publishTestResults testResultsPattern: 'pri-results.xml'
                
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'pri-reports',
                    reportFiles: 'index.html',
                    reportName: 'PRI Analysis Report'
                ])
            }
        }
    }
}
```

---

## 🔧 Advanced Configuration

### 1. Custom Analysis Rules

#### Create Custom Patterns
```python
# custom_patterns.py
from mesopredator_pri import PatternDefinition

custom_patterns = [
    PatternDefinition(
        name="deprecated_function_usage",
        pattern=r"deprecated_function\(",
        severity="medium",
        category="quality",
        description="Usage of deprecated function",
        fix_suggestion="Replace with new_function()"
    )
]
```

#### Configure in IDE
```json
{
  "mesopredator-pri": {
    "customPatterns": "./custom_patterns.py",
    "patternOverrides": {
      "sql_injection": {
        "severity": "critical",
        "autoFix": false
      }
    }
  }
}
```

### 2. Team Configuration

#### Shared Settings (.pri/config.json)
```json
{
  "team": {
    "name": "Backend Team",
    "shared_memory_namespace": "backend_patterns",
    "coding_standards": "pep8_strict",
    "security_level": "enterprise"
  },
  "analysis": {
    "focus_areas": ["security", "performance"],
    "exclude_directories": ["vendor/", "node_modules/"],
    "max_file_size_mb": 10
  },
  "notifications": {
    "slack_webhook": "https://hooks.slack.com/...",
    "email_on_critical": true,
    "daily_summary": true
  }
}
```

### 3. Performance Optimization

#### Large Project Settings
```json
{
  "performance": {
    "analysis_timeout_s": 300,
    "max_concurrent_files": 10,
    "cache_results": true,
    "incremental_analysis": true,
    "memory_limit_mb": 2048
  },
  "caching": {
    "cache_directory": ".pri/cache",
    "cache_ttl_hours": 24,
    "cache_invalidation": "content_hash"
  }
}
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. API Connection Issues
```bash
# Test API connectivity
curl -H "Authorization: Bearer pk_live_..." http://localhost:8000/health

# Check firewall settings
sudo ufw allow 8000

# Verify PRI server is running
ps aux | grep pri-server
```

#### 2. Extension Not Loading
```bash
# VS Code: Check extension logs
# Help → Developer Tools → Console
# Look for "mesopredator-pri" errors

# IntelliJ: Check IDE logs
# Help → Show Log in Explorer
# Look for plugin errors
```

#### 3. Performance Issues
```json
{
  "debug": {
    "enableDebugLogging": true,
    "profileAnalysis": true,
    "memoryUsageTracking": true
  }
}
```

#### 4. False Positives
```bash
# Train the system on false positives
pri train --false-positive file.py:123 --reason "framework_pattern"

# Update pattern confidence
pri patterns update --name "sql_injection" --confidence 0.85
```

### Support Resources

- **Documentation**: https://docs.mesopredator.com/ide-integration
- **GitHub Issues**: https://github.com/mesopredator/pri/issues
- **Community Forum**: https://community.mesopredator.com
- **Slack Support**: #pri-support in workspace

---

## 📈 Analytics & Reporting

### IDE Usage Analytics
```json
{
  "analytics": {
    "track_usage": true,
    "anonymous_metrics": true,
    "performance_tracking": true,
    "feature_usage": true
  },
  "reporting": {
    "weekly_summary": true,
    "team_dashboard": "https://dashboard.mesopredator.com",
    "export_formats": ["pdf", "json", "csv"]
  }
}
```

### Custom Dashboards
- **Security Trends**: Track security improvements over time
- **Code Quality Metrics**: Monitor technical debt reduction  
- **Team Performance**: Compare analysis results across team members
- **Pattern Learning**: Visualize memory system growth

---

*Mesopredator PRI IDE Integration - Bringing advanced code intelligence directly to your development workflow. For the latest features and updates, check our [release notes](https://github.com/mesopredator/pri/releases).*