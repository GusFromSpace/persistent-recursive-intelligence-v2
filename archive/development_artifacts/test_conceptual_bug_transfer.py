#!/usr/bin/env python3
"""
ADV-TEST-002: The "Conceptual Bug Transfer" Test - Advanced Knowledge Transfer

Tests the system's ability to abstract bug concepts and recognize them in 
completely different implementations. Updated for current mesopredator CLI.

Hypothesis to Disprove: The PRI's "learning" is limited to recognizing syntactic 
or structural patterns, not abstract programming concepts.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class ConceptualBugTransferTest:
    """Test cross-implementation conceptual bug recognition"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        
    def create_teacher_project(self, base_dir: Path) -> Path:
        """Create 'Project A' (Teacher) with known conceptual bug"""
        
        teacher_dir = base_dir / "teacher_project"
        teacher_dir.mkdir(exist_ok=True)
        
        # Off-by-one error in data processing script
        teacher_code = '''#!/usr/bin/env python3
"""
Teacher Project: Data Processing with Off-by-One Error

This project demonstrates a classic off-by-one error in loop iteration
that leads to incomplete data processing.
"""

import json
from typing import List, Dict

def process_sales_data(sales_records: List[Dict]) -> Dict:
    """
    Process sales records to calculate totals and statistics
    
    BUG: Off-by-one error in loop - misses last record
    """
    total_revenue = 0
    processed_count = 0
    
    # BUG: range(len(sales_records) - 1) misses the last element
    for i in range(len(sales_records) - 1):  # OFF-BY-ONE ERROR
        record = sales_records[i]
        total_revenue += record.get('amount', 0)
        processed_count += 1
    
    return {
        'total_revenue': total_revenue,
        'records_processed': processed_count,
        'average_sale': total_revenue / processed_count if processed_count > 0 else 0
    }

def validate_inventory_levels(inventory: List[int], thresholds: List[int]) -> List[bool]:
    """
    Check if inventory levels meet minimum thresholds
    
    BUG: Off-by-one error in range - doesn't check last item
    """
    validation_results = []
    
    # BUG: range(len(inventory) - 1) misses the last inventory item
    for i in range(len(inventory) - 1):  # OFF-BY-ONE ERROR
        is_sufficient = inventory[i] >= thresholds[i]
        validation_results.append(is_sufficient)
    
    return validation_results

def extract_customer_emails(customer_data: str) -> List[str]:
    """
    Extract email addresses from customer data text
    
    BUG: Slice operation misses last character
    """
    lines = customer_data.strip().split('\\n')
    emails = []
    
    for line in lines:
        if '@' in line:
            # BUG: [:-1] removes last character, potentially corrupting emails
            email = line.strip()[:-1]  # OFF-BY-ONE ERROR
            emails.append(email)
    
    return emails

# Test data demonstrating the bug
if __name__ == "__main__":
    # Sales data test
    sales = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': 200},
        {'id': 3, 'amount': 300},  # This record will be missed!
    ]
    
    result = process_sales_data(sales)
    print(f"Sales processing result: {result}")
    print(f"Expected 3 records, got {result['records_processed']}")
    print(f"Expected 600 revenue, got {result['total_revenue']}")
    
    # Inventory test
    inventory_levels = [50, 30, 20, 10]  # Last item will be missed!
    thresholds = [25, 25, 25, 25]
    
    validation = validate_inventory_levels(inventory_levels, thresholds)
    print(f"Inventory validation: {validation}")
    print(f"Expected 4 results, got {len(validation)}")
    
    # Email extraction test
    customer_text = "john.doe@email.com\\njane.smith@company.org"
    emails = extract_customer_emails(customer_text)
    print(f"Extracted emails: {emails}")
    print("Notice: emails may be corrupted due to off-by-one error")
'''
        
        (teacher_dir / "data_processor.py").write_text(teacher_code)
        
        # Create README explaining the bugs
        readme_content = """# Teacher Project: Data Processing

This project contains intentional off-by-one errors for testing purposes.

## Known Issues

1. `process_sales_data()` - Loop uses `range(len(records) - 1)`, missing last record
2. `validate_inventory_levels()` - Similar range issue, skips last inventory item  
3. `extract_customer_emails()` - String slice `[:-1]` removes last character

## Conceptual Pattern

All bugs follow the same pattern:
- **Intent**: Process all elements in a collection
- **Implementation Error**: Off-by-one mistakes in indexing/slicing
- **Result**: Last element is missed or corrupted
- **Root Cause**: Incorrect loop bounds or slice operations

This represents a fundamental conceptual error in boundary handling.
"""
        
        (teacher_dir / "README.md").write_text(readme_content)
        
        return teacher_dir
    
    def create_student_project(self, base_dir: Path) -> Path:
        """Create 'Project B' (Student) with same conceptual bug, different implementation"""
        
        student_dir = base_dir / "student_project"
        student_dir.mkdir(exist_ok=True)
        
        # Same conceptual bug but completely different syntax/context
        student_code = '''#!/usr/bin/env python3
"""
Student Project: Document Parser with Hidden Off-by-One Error

This project processes documents and extracts metadata. 
The implementation uses different syntax but has the same conceptual flaw.
"""

class DocumentProcessor:
    """Process and analyze text documents"""
    
    def __init__(self):
        self.processed_docs = []
    
    def parse_document_batch(self, documents):
        """
        Parse a batch of documents and extract metadata
        
        HIDDEN BUG: While loop condition has off-by-one error
        """
        results = []
        doc_index = 0
        
        # BUG: condition should be < len(documents), not < len(documents) - 1
        while doc_index < len(documents) - 1:  # OFF-BY-ONE ERROR (different syntax)
            doc = documents[doc_index]
            metadata = self._extract_metadata(doc)
            results.append(metadata)
            doc_index += 1
        
        return results
    
    def _extract_metadata(self, document):
        """Extract metadata from a single document"""
        lines = document.split('\\n')
        
        # Count non-empty lines but with off-by-one error
        line_count = 0
        i = 0
        # BUG: condition should be < len(lines), not < len(lines) - 1  
        while i < len(lines) - 1:  # OFF-BY-ONE ERROR (different context)
            if lines[i].strip():
                line_count += 1
            i += 1
        
        return {
            'line_count': line_count,
            'first_line': lines[0] if lines else '',
            'processed_at': 'timestamp_here'
        }
    
    def analyze_word_frequencies(self, text_samples):
        """
        Analyze word frequency across text samples
        
        HIDDEN BUG: List slicing has off-by-one error
        """
        word_counts = {}
        
        # BUG: samples[1:] skips first sample instead of starting from it
        for sample in text_samples[1:]:  # OFF-BY-ONE ERROR (different pattern)
            words = sample.lower().split()
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        return word_counts

class ReportGenerator:
    """Generate reports from processed data"""
    
    def create_summary_report(self, data_entries):
        """
        Create summary report from data entries
        
        HIDDEN BUG: Enumerate range has off-by-one error  
        """
        summary_lines = []
        
        # BUG: enumerate(data_entries[:-1]) misses last entry
        for index, entry in enumerate(data_entries[:-1]):  # OFF-BY-ONE ERROR
            line = f"{index + 1}. {entry.get('title', 'Untitled')}"
            summary_lines.append(line)
        
        return '\\n'.join(summary_lines)

# Test demonstrating the bugs
if __name__ == "__main__":
    processor = DocumentProcessor()
    
    # Document batch test
    docs = [
        "First document content",
        "Second document with\\nmultiple lines",
        "Third document here"  # This will be missed!
    ]
    
    metadata_results = processor.parse_document_batch(docs)
    print(f"Document processing: expected 3 results, got {len(metadata_results)}")
    
    # Word frequency test  
    samples = ["hello world", "world test", "final sample"]  # First sample skipped!
    frequencies = processor.analyze_word_frequencies(samples)
    print(f"Word frequencies: {frequencies}")
    print("Note: 'hello' should appear but may be missing")
    
    # Report generation test
    report_gen = ReportGenerator()
    entries = [
        {'title': 'First Entry'},
        {'title': 'Second Entry'}, 
        {'title': 'Third Entry'}  # This will be missed!
    ]
    
    summary = report_gen.create_summary_report(entries)
    print(f"Summary report:\\n{summary}")
    print("Expected 3 entries in summary")
'''
        
        (student_dir / "document_parser.py").write_text(student_code)
        
        # Create different README that doesn't hint at the pattern
        readme_content = """# Student Project: Document Parser

Advanced document processing and analysis system.

## Features

- Batch document processing with metadata extraction
- Word frequency analysis across multiple text samples  
- Automated report generation from processed data
- Object-oriented design with clean separation of concerns

## Components

- `DocumentProcessor`: Main processing engine
- `ReportGenerator`: Summary and report creation utilities

## Usage

The system processes documents in batches and extracts useful metadata
for further analysis and reporting.
"""
        
        (student_dir / "README.md").write_text(readme_content)
        
        return student_dir
    
    def train_on_teacher_project(self, teacher_dir: Path) -> Dict[str, Any]:
        """Train the system on the teacher project to learn the bug concept"""
        
        print("🧑‍🏫 Training on teacher project...")
        
        try:
            # Run analysis on teacher project using venv python
            venv_python = Path("venv/bin/python")
            if not venv_python.exists():
                venv_python = sys.executable
            
            result = subprocess.run([
                str(venv_python), "-c", """
import sys
sys.path.insert(0, '.')
import mesopredator_cli
mesopredator_cli.main()
""", "analyze", str(teacher_dir), "--verbose"
            ],
            capture_output=True,
            text=True,
            timeout=180
            )
            
            training_result = {
                'returncode': result.returncode,
                'training_successful': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Look for off-by-one detection in teacher project
            output_text = (result.stdout + result.stderr).lower()
            off_by_one_indicators = [
                'off-by-one', 'off by one', 'boundary', 'range', 'index',
                'missing last', 'incomplete', 'loop', 'iteration'
            ]
            
            detected_concepts = [indicator for indicator in off_by_one_indicators 
                               if indicator in output_text]
            
            training_result['concepts_detected'] = detected_concepts
            training_result['concept_learning_score'] = len(detected_concepts) * 10
            
            return training_result
            
        except subprocess.TimeoutExpired:
            return {
                'training_successful': False,
                'error': 'Training timed out',
                'concepts_detected': []
            }
        except Exception as e:
            return {
                'training_successful': False,
                'error': str(e),
                'concepts_detected': []
            }
    
    def test_concept_transfer(self, student_dir: Path) -> Dict[str, Any]:
        """Test if the system can recognize the same concept in student project"""
        
        print("🎓 Testing concept transfer on student project...")
        
        try:
            # Run analysis on student project using venv python
            venv_python = Path("venv/bin/python")
            if not venv_python.exists():
                venv_python = sys.executable
                
            result = subprocess.run([
                str(venv_python), "-c", """
import sys
sys.path.insert(0, '.')
import mesopredator_cli
mesopredator_cli.main()
""", "analyze", str(student_dir), "--verbose"
            ],
            capture_output=True,
            text=True,
            timeout=180
            )
            
            transfer_result = {
                'returncode': result.returncode,
                'analysis_successful': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Analyze for concept transfer evidence
            output_text = (result.stdout + result.stderr).lower()
            
            # Look for off-by-one concept recognition
            concept_indicators = [
                'off-by-one', 'off by one', 'boundary error', 'range error',
                'missing last element', 'incomplete iteration', 'loop boundary',
                'index error', 'boundary condition'
            ]
            
            detected_concepts = [indicator for indicator in concept_indicators 
                               if indicator in output_text]
            
            # Count specific off-by-one instances found
            specific_patterns = [
                'len(', '- 1', '[:-1]', 'while.*<.*len', 'range.*len.*-'
            ]
            
            pattern_matches = [pattern for pattern in specific_patterns 
                             if pattern in result.stdout]
            
            transfer_result['concepts_detected'] = detected_concepts
            transfer_result['pattern_matches'] = pattern_matches
            transfer_result['concept_transfer_score'] = len(detected_concepts) * 15 + len(pattern_matches) * 10
            transfer_result['transfer_successful'] = transfer_result['concept_transfer_score'] >= 30
            
            return transfer_result
            
        except subprocess.TimeoutExpired:
            return {
                'analysis_successful': False,
                'transfer_successful': False,
                'error': 'Analysis timed out',
                'concepts_detected': []
            }
        except Exception as e:
            return {
                'analysis_successful': False,
                'transfer_successful': False,
                'error': str(e),
                'concepts_detected': []
            }
    
    def run_conceptual_transfer_test(self) -> Dict[str, Any]:
        """Execute the complete conceptual bug transfer test"""
        
        print("🧠 ADV-TEST-002: CONCEPTUAL BUG TRANSFER TEST")
        print("=" * 80)
        print("🎯 Testing cross-implementation conceptual bug recognition")
        print("🔬 Hypothesis: System can abstract and transfer bug concepts")
        print()
        
        # Setup test environment
        self.temp_dir = Path(tempfile.mkdtemp(prefix="concept_transfer_test_"))
        print(f"📁 Created test environment: {self.temp_dir}")
        
        # Create teacher and student projects
        print("\n📚 Creating teacher project with known off-by-one bugs...")
        teacher_dir = self.create_teacher_project(self.temp_dir)
        print(f"✅ Teacher project created: {teacher_dir}")
        
        print("\n🎓 Creating student project with same conceptual bugs...")
        student_dir = self.create_student_project(self.temp_dir)
        print(f"✅ Student project created: {student_dir}")
        
        # Phase 1: Train on teacher project
        print("\n" + "="*50)
        print("PHASE 1: CONCEPT LEARNING")
        print("="*50)
        
        training_result = self.train_on_teacher_project(teacher_dir)
        
        if not training_result['training_successful']:
            print(f"❌ Training failed: {training_result.get('error', 'Unknown error')}")
            return {
                'test_id': 'ADV-TEST-002',
                'test_result': 'training_failed',
                'error': training_result.get('error')
            }
        
        print("✅ Training completed successfully")
        print(f"   Concepts detected in teacher: {training_result['concepts_detected']}")
        print(f"   Concept learning score: {training_result['concept_learning_score']}")
        
        # Phase 2: Test concept transfer
        print("\n" + "="*50)
        print("PHASE 2: CONCEPT TRANSFER")
        print("="*50)
        
        transfer_result = self.test_concept_transfer(student_dir)
        
        if not transfer_result['analysis_successful']:
            print(f"❌ Concept transfer test failed: {transfer_result.get('error', 'Unknown error')}")
            return {
                'test_id': 'ADV-TEST-002',
                'test_result': 'transfer_analysis_failed',
                'training_result': training_result,
                'error': transfer_result.get('error')
            }
        
        print("✅ Student project analysis completed")
        print(f"   Concepts detected in student: {transfer_result['concepts_detected']}")
        print(f"   Pattern matches found: {transfer_result['pattern_matches']}")
        print(f"   Concept transfer score: {transfer_result['concept_transfer_score']}")
        
        # Evaluate overall results
        transfer_successful = transfer_result['transfer_successful']
        concept_learning_adequate = training_result['concept_learning_score'] >= 20
        
        test_passed = transfer_successful and concept_learning_adequate
        
        final_results = {
            'test_id': 'ADV-TEST-002',
            'test_name': 'Conceptual Bug Transfer',
            'timestamp': datetime.now().isoformat(),
            'training_phase': {
                'successful': training_result['training_successful'],
                'concepts_detected': training_result['concepts_detected'],
                'learning_score': training_result['concept_learning_score']
            },
            'transfer_phase': {
                'successful': transfer_result['analysis_successful'],
                'transfer_detected': transfer_result['transfer_successful'],
                'concepts_detected': transfer_result['concepts_detected'],
                'pattern_matches': transfer_result['pattern_matches'],
                'transfer_score': transfer_result['concept_transfer_score']
            },
            'overall_assessment': {
                'concept_learning_adequate': concept_learning_adequate,
                'concept_transfer_successful': transfer_successful,
                'test_passed': test_passed
            },
            'test_environment': {
                'teacher_project': str(teacher_dir),
                'student_project': str(student_dir)
            }
        }
        
        # Print final assessment
        print(f"\n📊 CONCEPTUAL TRANSFER TEST RESULTS:")
        print(f"   Concept learning score: {training_result['concept_learning_score']}")
        print(f"   Concept transfer score: {transfer_result['concept_transfer_score']}")
        print(f"   Transfer successful: {transfer_successful}")
        
        if test_passed:
            print("\n🎉 CONCEPTUAL TRANSFER TEST PASSED!")
            print("✅ System demonstrates cross-implementation concept recognition")
            print("🧠 Can abstract bug patterns beyond syntactic similarities")
        else:
            print("\n❌ CONCEPTUAL TRANSFER TEST FAILED")
            if not concept_learning_adequate:
                print("⚠️ Insufficient concept learning from teacher project")
            if not transfer_successful:
                print("⚠️ Failed to recognize concept in different implementation")
            print("🔍 Learning may be limited to syntactic patterns")
        
        return final_results
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Test environment cleaned up")

def main():
    """Execute ADV-TEST-002: Conceptual Bug Transfer Test"""
    
    tester = ConceptualBugTransferTest()
    
    try:
        results = tester.run_conceptual_transfer_test()
        
        # Save results
        results_file = "conceptual_transfer_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to {results_file}")
        
        return results.get('overall_assessment', {}).get('test_passed', False)
    
    finally:
        tester.cleanup_test_environment()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)