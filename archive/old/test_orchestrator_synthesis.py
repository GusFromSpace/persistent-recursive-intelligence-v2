#!/usr/bin/env python3
"""
ADV-TEST-006: The "Orchestrator" Test - Complex Multi-Domain Synthesis

Tests the system's ability to synthesize information from disparate sources
to solve complex, real-world problems. Updated for current architecture.

Hypothesis to Disprove: The PRI's "orchestration" is merely linear analysis.
It cannot dynamically synthesize information from code, logs, and schemas.
"""

import sys
import os
import json
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class OrchestratorSynthesisTest:
    """Test complex multi-domain synthesis capabilities"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        
    def create_complex_scenario(self) -> Dict[str, Path]:
        """Create realistic multi-domain problem scenario"""
        
        self.temp_dir = Path(tempfile.mkdtemp(prefix="orchestrator_test_"))
        scenario_dir = self.temp_dir / "ecommerce_scenario"
        scenario_dir.mkdir(exist_ok=True)
        
        # 1. Create application source code with N+1 query bug
        app_dir = scenario_dir / "project-ecommerce"
        app_dir.mkdir(exist_ok=True)
        
        # Models with problematic relationships
        models_code = '''#!/usr/bin/env python3
"""
E-commerce Models with Hidden N+1 Query Problem

This models.py contains relationship definitions that enable N+1 queries
when not properly handled by the view layer.
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Customer:
    """Customer model"""
    id: int
    email: str
    name: str
    created_at: datetime

@dataclass  
class Order:
    """Order model with customer relationship"""
    id: int
    customer_id: int  # Foreign key to Customer
    order_date: datetime
    status: str
    total_amount: float
    
    # This relationship definition enables lazy loading
    # which can cause N+1 queries if not handled properly
    def get_customer(self, db_connection):
        """Fetch customer for this order - POTENTIAL N+1 SOURCE"""
        return db_connection.get_customer_by_id(self.customer_id)

@dataclass
class OrderItem:
    """Order item model"""
    id: int
    order_id: int  # Foreign key to Order
    product_id: int
    quantity: int
    unit_price: float
    
    def get_order(self, db_connection):
        """Fetch order for this item - POTENTIAL N+1 SOURCE"""
        return db_connection.get_order_by_id(self.order_id)
    
    def get_product(self, db_connection):
        """Fetch product for this item - POTENTIAL N+1 SOURCE"""
        return db_connection.get_product_by_id(self.product_id)

@dataclass
class Product:
    """Product model"""
    id: int
    name: str
    description: str
    price: float
    category_id: int

class DatabaseConnection:
    """Simulated database connection with query logging"""
    
    def __init__(self):
        self.query_count = 0
        self.queries_executed = []
    
    def execute_query(self, query: str):
        """Execute query and log for analysis"""
        self.query_count += 1
        self.queries_executed.append({
            'query': query,
            'timestamp': datetime.now(),
            'query_number': self.query_count
        })
        # Simulate query execution time
        import time
        time.sleep(0.001)  # 1ms per query
    
    def get_customer_by_id(self, customer_id: int):
        """Single customer lookup - each call is a separate query"""
        self.execute_query(f"SELECT * FROM customers WHERE id = {customer_id}")
        return Customer(customer_id, f"user{customer_id}@email.com", f"User {customer_id}", datetime.now())
    
    def get_order_by_id(self, order_id: int):
        """Single order lookup"""
        self.execute_query(f"SELECT * FROM orders WHERE id = {order_id}")
        return Order(order_id, 1, datetime.now(), "completed", 99.99)
    
    def get_orders_for_customer(self, customer_id: int):
        """Get all orders for customer"""
        self.execute_query(f"SELECT * FROM orders WHERE customer_id = {customer_id}")
        return [Order(i, customer_id, datetime.now(), "completed", 99.99) for i in range(1, 4)]
    
    def get_order_items(self, order_id: int):
        """Get items for an order - another potential N+1 source"""
        self.execute_query(f"SELECT * FROM order_items WHERE order_id = {order_id}")
        return [OrderItem(i, order_id, i+10, 1, 29.99) for i in range(1, 4)]
'''
        
        (app_dir / "models.py").write_text(models_code)
        
        # Views with N+1 query bug
        views_code = '''#!/usr/bin/env python3
"""
E-commerce Views with N+1 Query Bug

The order history view contains a classic N+1 query problem:
1 query to get orders + N queries to get customer for each order
"""

from models import DatabaseConnection, Order, Customer
from typing import List, Dict, Any
import time

class OrderHistoryView:
    """View for displaying customer order history - CONTAINS N+1 BUG"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def get_order_history(self, customer_id: int) -> Dict[str, Any]:
        """
        Get order history for customer
        
        BUG: This method has a classic N+1 query problem!
        1. First query gets all orders for customer
        2. Then N queries (one per order) to get customer details
        3. Plus N more queries to get order items
        
        For 100 orders, this becomes 201 queries instead of 3!
        """
        start_time = time.time()
        
        # Query 1: Get all orders for customer
        orders = self.db.get_orders_for_customer(customer_id)
        
        order_history = []
        
        # N+1 BUG: Loop through orders and make individual queries
        for order in orders:
            # QUERY N: Get customer for each order (unnecessary!)
            customer = order.get_customer(self.db)
            
            # QUERY N+1: Get items for each order
            order_items = self.db.get_order_items(order.id)
            
            # Additional N queries for product details
            items_with_products = []
            for item in order_items:
                product = item.get_product(self.db)  # Another N+1 pattern!
                items_with_products.append({
                    'item': item,
                    'product': product
                })
            
            order_history.append({
                'order': order,
                'customer': customer,  # Same customer every time!
                'items': items_with_products,
                'total_queries_so_far': self.db.query_count
            })
        
        end_time = time.time()
        
        return {
            'orders': order_history,
            'total_queries': self.db.query_count,
            'execution_time': end_time - start_time,
            'performance_issue': self.db.query_count > len(orders) * 2
        }

def simulate_slow_order_history_endpoint():
    """
    Simulate the problematic endpoint that causes timeouts
    This function demonstrates the performance issue
    """
    db = DatabaseConnection()
    view = OrderHistoryView(db)
    
    print("Simulating order history request...")
    result = view.get_order_history(customer_id=1)
    
    print(f"Query Count: {result['total_queries']}")
    print(f"Execution Time: {result['execution_time']:.2f}s")
    print(f"Performance Issue Detected: {result['performance_issue']}")
    
    return result

if __name__ == "__main__":
    # This will demonstrate the N+1 query problem
    simulate_slow_order_history_endpoint()
'''
        
        (app_dir / "views.py").write_text(views_code)
        
        # 2. Create production logs showing slow response times
        logs_content = '''[2025-07-03 14:23:15] INFO - GET /orders/history?customer_id=1 - Response: 200 - Time: 0.045s
[2025-07-03 14:23:16] INFO - GET /orders/history?customer_id=2 - Response: 200 - Time: 0.052s
[2025-07-03 14:23:17] INFO - GET /orders/history?customer_id=3 - Response: 200 - Time: 0.041s
[2025-07-03 14:23:18] WARN - GET /orders/history?customer_id=4 - Response: 200 - Time: 2.134s
[2025-07-03 14:23:19] ERROR - GET /orders/history?customer_id=5 - Response: 500 - Time: 30.000s - TIMEOUT
[2025-07-03 14:23:20] WARN - GET /orders/history?customer_id=6 - Response: 200 - Time: 3.567s
[2025-07-03 14:23:21] ERROR - GET /orders/history?customer_id=7 - Response: 500 - Time: 30.000s - TIMEOUT
[2025-07-03 14:23:22] WARN - GET /orders/history?customer_id=8 - Response: 200 - Time: 4.123s
[2025-07-03 14:23:23] ERROR - GET /orders/history?customer_id=9 - Response: 500 - Time: 30.000s - TIMEOUT
[2025-07-03 14:23:24] CRITICAL - GET /orders/history?customer_id=10 - Response: 500 - Time: 30.000s - TIMEOUT
[2025-07-03 14:23:25] INFO - Multiple timeout errors detected on /orders/history endpoint
[2025-07-03 14:23:26] WARN - Customer complaints received about slow order history page
[2025-07-03 14:23:27] ERROR - Peak hour performance degradation detected
[2025-07-03 14:23:28] INFO - Database query count spike: 2,341 queries in last minute
[2025-07-03 14:23:29] WARN - Database connection pool exhaustion warning
[2025-07-03 14:23:30] ERROR - Performance monitoring alert: /orders/history average response time: 8.2s
[2025-07-03 14:24:01] INFO - Normal traffic resumed, response times back to normal
[2025-07-03 14:24:02] INFO - GET /orders/history?customer_id=11 - Response: 200 - Time: 0.048s'''
        
        (scenario_dir / "prod_logs.txt").write_text(logs_content)
        
        # 3. Create database schema
        schema_content = '''-- E-commerce Database Schema
-- This schema shows the relationships that enable N+1 queries

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index for email lookups
    INDEX idx_customer_email (email)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    
    -- Foreign key relationship (enables joins)
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    
    -- MISSING INDEX: This is part of the performance problem!
    -- INDEX idx_orders_customer_id (customer_id) -- Should exist but doesn't!
    
    -- Existing indexes
    INDEX idx_orders_date (order_date),
    INDEX idx_orders_status (status)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER,
    
    INDEX idx_products_category (category_id),
    INDEX idx_products_price (price)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    
    -- Foreign key relationships
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    
    -- MISSING INDEXES: These contribute to the N+1 problem!
    -- INDEX idx_order_items_order_id (order_id) -- Should exist!
    -- INDEX idx_order_items_product_id (product_id) -- Should exist!
    
    -- Compound index for order+product lookups
    INDEX idx_order_items_compound (order_id, product_id)
);

-- Performance Analysis Comments:
-- 1. Missing index on orders.customer_id causes slow customer order lookups
-- 2. Missing indexes on order_items foreign keys cause slow item fetching
-- 3. The compound index helps but doesn't solve the N+1 query pattern
-- 4. Proper solution requires JOIN queries, not individual lookups

-- Optimal query for order history (what SHOULD be used):
-- SELECT o.*, c.name, c.email, oi.*, p.name as product_name
-- FROM orders o
-- JOIN customers c ON o.customer_id = c.id  
-- JOIN order_items oi ON o.id = oi.order_id
-- JOIN products p ON oi.product_id = p.id
-- WHERE o.customer_id = ?
-- ORDER BY o.order_date DESC;

-- Current inefficient pattern (what IS being used):
-- 1. SELECT * FROM orders WHERE customer_id = ?
-- 2. For each order: SELECT * FROM customers WHERE id = ?
-- 3. For each order: SELECT * FROM order_items WHERE order_id = ?
-- 4. For each item: SELECT * FROM products WHERE id = ?
-- Result: 1 + N + N + (N*M) queries instead of 1 JOIN query!'''
        
        (scenario_dir / "schema.sql").write_text(schema_content)
        
        return {
            'scenario_dir': scenario_dir,
            'app_code': app_dir,
            'logs': scenario_dir / "prod_logs.txt",
            'schema': scenario_dir / "schema.sql"
        }
    
    def test_multi_domain_synthesis(self, scenario_paths: Dict[str, Path]) -> Dict[str, Any]:
        """Test if system can synthesize information across all three domains"""
        
        print("🔬 Testing multi-domain synthesis capabilities...")
        
        # Create analysis prompt that requires synthesis
        analysis_prompt = scenario_paths['scenario_dir'] / "synthesis_challenge.md"
        prompt_content = '''# Performance Investigation Challenge

## Problem Statement
Our e-commerce platform is experiencing critical performance issues during peak hours. 
The "View Order History" page is timing out, causing customer complaints and lost revenue.

## Available Evidence
1. **Application Code** (project-ecommerce/): Source code for the order history functionality
2. **Production Logs** (prod_logs.txt): Server logs showing response times and errors  
3. **Database Schema** (schema.sql): Database structure and relationship definitions

## Investigation Goal
Analyze ALL THREE sources of evidence to:
1. Identify the root cause of the performance degradation
2. Explain why the issue manifests during peak hours but not normal traffic
3. Propose a comprehensive solution that addresses both code and database issues
4. Demonstrate understanding of how the three evidence sources relate to each other

## Success Criteria
- Must reference findings from all three evidence sources
- Must identify the N+1 query pattern in the code
- Must correlate slow response times in logs to specific code patterns
- Must recognize database schema issues that contribute to the problem
- Must propose solutions that address multiple layers (code, queries, database)

This requires true synthesis - connecting insights across code, logs, and schema.
'''
        
        analysis_prompt.write_text(prompt_content)
        
        try:
            # Run mesopredator analyze on the entire scenario
            result = subprocess.run([
                sys.executable, "-c", """
import sys
sys.path.insert(0, '.')
import mesopredator_cli
mesopredator_cli.main()
""", "analyze", str(scenario_paths['scenario_dir'])
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for complex analysis
            )
            
            # Analyze the response for synthesis capabilities
            synthesis_analysis = self.analyze_synthesis_capability(result, scenario_paths)
            
            return {
                'analysis_completed': result.returncode == 0,
                'synthesis_analysis': synthesis_analysis,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                'analysis_completed': False,
                'synthesis_analysis': {
                    'synthesis_achieved': False,
                    'reason': 'Analysis timed out'
                },
                'error': 'Analysis timed out after 5 minutes'
            }
        except Exception as e:
            return {
                'analysis_completed': False,
                'synthesis_analysis': {
                    'synthesis_achieved': False,
                    'reason': f'Error: {str(e)}'
                },
                'error': str(e)
            }
        finally:
            # Clean up prompt file
            if analysis_prompt.exists():
                analysis_prompt.unlink()
    
    def analyze_synthesis_capability(self, result, scenario_paths: Dict[str, Path]) -> Dict[str, Any]:
        """Analyze if the system achieved true multi-domain synthesis"""
        
        output_text = result.stdout.lower()
        
        # Check for evidence of analyzing all three domains
        domain_analysis = {
            'code_analysis': any(term in output_text for term in [
                'models.py', 'views.py', 'n+1', 'query', 'loop', 'get_customer'
            ]),
            'log_analysis': any(term in output_text for term in [
                'timeout', 'response time', '30.000s', 'slow', 'performance'
            ]),
            'schema_analysis': any(term in output_text for term in [
                'index', 'foreign key', 'join', 'customer_id', 'missing'
            ])
        }
        
        domains_analyzed = sum(domain_analysis.values())
        
        # Check for synthesis indicators (connecting insights across domains)
        synthesis_indicators = [
            'correlate', 'relationship', 'connects to', 'causes', 'results in',
            'explains why', 'due to', 'because', 'leads to', 'pattern'
        ]
        
        synthesis_mentions = sum(1 for indicator in synthesis_indicators if indicator in output_text)
        
        # Check for specific N+1 query pattern recognition
        n_plus_one_recognition = any(term in output_text for term in [
            'n+1', 'n plus 1', 'multiple queries', 'query per', 'individual queries'
        ])
        
        # Check for comprehensive solution (addressing multiple layers)
        solution_completeness = {
            'code_fix': any(term in output_text for term in [
                'join', 'eager loading', 'prefetch', 'bulk query'
            ]),
            'database_fix': any(term in output_text for term in [
                'index', 'foreign key index', 'customer_id index'
            ]),
            'performance_fix': any(term in output_text for term in [
                'reduce queries', 'optimize', 'batch', 'single query'
            ])
        }
        
        solution_layers = sum(solution_completeness.values())
        
        # Calculate synthesis score
        synthesis_score = 0
        synthesis_score += domains_analyzed * 25  # 25 points per domain
        synthesis_score += synthesis_mentions * 5   # 5 points per synthesis indicator
        synthesis_score += (20 if n_plus_one_recognition else 0)  # 20 points for N+1 recognition
        synthesis_score += solution_layers * 10     # 10 points per solution layer
        
        # Determine if synthesis was achieved
        synthesis_achieved = (
            domains_analyzed >= 3 and  # Analyzed all domains
            synthesis_mentions >= 3 and  # Shows synthesis thinking
            n_plus_one_recognition and  # Identified core problem
            solution_layers >= 2  # Proposed multi-layer solution
        )
        
        return {
            'synthesis_achieved': synthesis_achieved,
            'synthesis_score': synthesis_score,
            'domains_analyzed': domains_analyzed,
            'domain_analysis': domain_analysis,
            'synthesis_mentions': synthesis_mentions,
            'n_plus_one_recognized': n_plus_one_recognition,
            'solution_completeness': solution_completeness,
            'solution_layers': solution_layers,
            'analysis_details': {
                'total_domains': 3,
                'domains_found': list(k for k, v in domain_analysis.items() if v),
                'synthesis_indicators_found': synthesis_mentions,
                'multi_layer_solution': solution_layers >= 2
            }
        }
    
    def run_orchestrator_synthesis_test(self) -> Dict[str, Any]:
        """Execute the complete orchestrator synthesis test"""
        
        print("🎭 ADV-TEST-006: ORCHESTRATOR SYNTHESIS TEST")
        print("=" * 80)
        print("🎯 Testing multi-domain synthesis and orchestration capabilities")
        print("🔬 Hypothesis: System can synthesize insights across code, logs, and schemas")
        print()
        
        # Create complex scenario
        print("📁 Creating complex multi-domain scenario...")
        scenario_paths = self.create_complex_scenario()
        print(f"✅ Scenario created: {scenario_paths['scenario_dir']}")
        print(f"   📂 Application code: {scenario_paths['app_code']}")
        print(f"   📜 Production logs: {scenario_paths['logs']}")
        print(f"   🗃️  Database schema: {scenario_paths['schema']}")
        
        # Test synthesis capability
        print("\n🔬 Testing synthesis capability...")
        synthesis_result = self.test_multi_domain_synthesis(scenario_paths)
        
        if not synthesis_result['analysis_completed']:
            print(f"❌ Analysis failed: {synthesis_result.get('error', 'Unknown error')}")
            return {
                'test_id': 'ADV-TEST-006',
                'test_result': 'analysis_failed',
                'error': synthesis_result.get('error')
            }
        
        print("✅ Analysis completed")
        
        # Evaluate synthesis results
        synthesis_analysis = synthesis_result['synthesis_analysis']
        synthesis_achieved = synthesis_analysis['synthesis_achieved']
        
        print(f"\n📊 Synthesis Analysis Results:")
        print(f"   Domains analyzed: {synthesis_analysis['domains_analyzed']}/3")
        print(f"   Domain breakdown: {synthesis_analysis['domain_analysis']}")
        print(f"   Synthesis indicators: {synthesis_analysis['synthesis_mentions']}")
        print(f"   N+1 pattern recognized: {synthesis_analysis['n_plus_one_recognized']}")
        print(f"   Solution layers: {synthesis_analysis['solution_layers']}")
        print(f"   Synthesis score: {synthesis_analysis['synthesis_score']}")
        
        # Overall test assessment
        test_passed = synthesis_achieved
        
        final_results = {
            'test_id': 'ADV-TEST-006',
            'test_name': 'Orchestrator Synthesis Test',
            'timestamp': datetime.now().isoformat(),
            'scenario_complexity': {
                'domains': 3,
                'evidence_sources': ['code', 'logs', 'schema'],
                'problem_type': 'N+1 query performance issue'
            },
            'synthesis_results': synthesis_analysis,
            'test_passed': test_passed,
            'scenario_paths': {k: str(v) for k, v in scenario_paths.items()}
        }
        
        print(f"\n📊 ORCHESTRATOR SYNTHESIS TEST RESULTS:")
        if synthesis_achieved:
            print("🎉 ORCHESTRATOR SYNTHESIS TEST PASSED!")
            print("✅ System demonstrated true multi-domain synthesis")
            print("🧠 Can correlate insights across code, logs, and schemas")
            print("🔧 Proposed comprehensive multi-layer solutions")
        else:
            print("❌ ORCHESTRATOR SYNTHESIS TEST FAILED")
            print("⚠️ System shows limited synthesis capability")
            print("🔍 Analysis appears to be linear rather than orchestrated")
            if synthesis_analysis['domains_analyzed'] < 3:
                print(f"   • Only analyzed {synthesis_analysis['domains_analyzed']}/3 domains")
            if synthesis_analysis['synthesis_mentions'] < 3:
                print("   • Limited evidence of cross-domain correlation")
            if not synthesis_analysis['n_plus_one_recognized']:
                print("   • Failed to identify core N+1 query pattern")
        
        return final_results
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Test environment cleaned up")

def main():
    """Execute ADV-TEST-006: Orchestrator Synthesis Test"""
    
    tester = OrchestratorSynthesisTest()
    
    try:
        results = tester.run_orchestrator_synthesis_test()
        
        # Save results
        results_file = "orchestrator_synthesis_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to {results_file}")
        
        return results['test_passed']
    
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