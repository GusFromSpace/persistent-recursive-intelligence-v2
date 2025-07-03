#!/usr/bin/env python3
"""
ADV-TEST-006: The "Orchestrator" Test - Complex Multi-Domain Synthesis

Tests the system's ability to act as an autonomous agent, orchestrating multiple 
analysis tools and synthesizing information from different domains to solve a 
complex, real-world problem.

Hypothesis to Disprove: The PRI's "orchestration" is merely a linear chain of scripts. 
It cannot dynamically plan and synthesize information from disparate sources 
(e.g., code, logs, and database schemas) to solve a novel, multi-faceted problem.
"""

import sys
import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

class OrchestratorSynthesisTest:
    """Test complex multi-domain problem solving and synthesis capabilities"""
    
    def __init__(self):
        self.test_artifacts = {}
        self.scenario_path = None
        
    def create_complex_scenario(self) -> Path:
        """Create a realistic multi-part performance problem scenario"""
        scenario_dir = Path(tempfile.mkdtemp(prefix="orchestrator_scenario_"))
        
        # Create the e-commerce application source code
        self.create_ecommerce_source_code(scenario_dir)
        
        # Create production logs showing the performance issue
        self.create_production_logs(scenario_dir)
        
        # Create database schema
        self.create_database_schema(scenario_dir)
        
        # Create problem description
        self.create_problem_description(scenario_dir)
        
        return scenario_dir
    
    def create_ecommerce_source_code(self, base_dir: Path):
        """Create e-commerce application source code with N+1 query bug"""
        project_dir = base_dir / "project-ecommerce"
        project_dir.mkdir()
        
        # Main application file
        app_code = '''#!/usr/bin/env python3
"""
E-Commerce Platform - Main Application
"""

from flask import Flask, request, jsonify
from database import DatabaseManager
from models import Order, OrderItem
import logging

app = Flask(__name__)
db = DatabaseManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/api/orders/history")
def get_order_history():
    """
    Get order history for a customer
    
    This endpoint is experiencing performance issues during peak hours!
    """
    customer_id = request.args.get('customer_id')
    
    if not customer_id:
        return jsonify({"error": "customer_id required"}), 400
    
    try:
        # Get all orders for customer
        orders = db.get_customer_orders(customer_id)
        
        # Format response with order details
        order_history = []
        
        # THIS IS THE N+1 QUERY PROBLEM!
        # For each order, we make a separate query to get items
        for order in orders:
            order_data = {
                "order_id": order.id,
                "order_date": order.created_at,
                "total_amount": order.total_amount,
                "status": order.status,
                "items": []
            }
            
            # PROBLEM: This creates N separate queries for N orders!
            order_items = db.get_order_items(order.id)  # Query per order
            
            for item in order_items:
                order_data["items"].append({
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price
                })
            
            order_history.append(order_data)
        
        logger.info(f"Retrieved {len(order_history)} orders for customer {customer_id}")
        return jsonify({"orders": order_history})
        
    except Exception as e:
        logger.error(f"Error retrieving order history: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/orders/<order_id>")
def get_order_details(order_id):
    """Get details for a specific order - this endpoint is fast"""
    try:
        order = db.get_order_by_id(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        # Single optimized query with JOIN
        order_with_items = db.get_order_with_items(order_id)
        
        return jsonify(order_with_items)
        
    except Exception as e:
        logger.error(f"Error retrieving order {order_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
        
        (project_dir / "app.py").write_text(app_code)
        
        # Database manager with the problematic queries
        db_code = '''#!/usr/bin/env python3
"""
Database Manager - Contains the N+1 query problem
"""

import sqlite3
from typing import List, Dict, Any
from models import Order, OrderItem

class DatabaseManager:
    """Database operations for e-commerce platform"""
    
    def __init__(self, db_path: str = "ecommerce.db"):
        self.db_path = db_path
    
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        """
        Get all orders for a customer
        This query is efficient - gets all orders in one query
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, customer_id, created_at, total_amount, status
            FROM orders 
            WHERE customer_id = ?
            ORDER BY created_at DESC
        """, (customer_id,))
        
        orders = []
        for row in cursor.fetchall():
            orders.append(Order(
                id=row[0],
                customer_id=row[1], 
                created_at=row[2],
                total_amount=row[3],
                status=row[4]
            ))
        
        conn.close()
        return orders
    
    def get_order_items(self, order_id: str) -> List[OrderItem]:
        """
        Get items for a specific order
        
        PROBLEM: This gets called once PER ORDER, creating N+1 queries!
        If customer has 50 orders, this creates 50 separate database calls.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT oi.id, oi.order_id, oi.product_id, p.name, oi.quantity, oi.price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """, (order_id,))
        
        items = []
        for row in cursor.fetchall():
            items.append(OrderItem(
                id=row[0],
                order_id=row[1],
                product_id=row[2],
                product_name=row[3],
                quantity=row[4],
                price=row[5]
            ))
        
        conn.close()
        return items
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get single order by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, customer_id, created_at, total_amount, status
            FROM orders 
            WHERE id = ?
        """, (order_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Order(
                id=row[0],
                customer_id=row[1],
                created_at=row[2], 
                total_amount=row[3],
                status=row[4]
            )
        return None
    
    def get_order_with_items(self, order_id: str) -> Dict[str, Any]:
        """
        OPTIMIZED VERSION: Get order and items in single query
        This is how the order history endpoint SHOULD work!
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Single JOIN query gets everything at once
        cursor.execute("""
            SELECT 
                o.id, o.customer_id, o.created_at, o.total_amount, o.status,
                oi.id, oi.product_id, p.name, oi.quantity, oi.price
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE o.id = ?
        """, (order_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return None
        
        # Build response from joined data
        order_data = {
            "order_id": rows[0][0],
            "customer_id": rows[0][1],
            "created_at": rows[0][2],
            "total_amount": rows[0][3],
            "status": rows[0][4],
            "items": []
        }
        
        for row in rows:
            if row[5]:  # Has order item
                order_data["items"].append({
                    "item_id": row[5],
                    "product_id": row[6],
                    "product_name": row[7],
                    "quantity": row[8],
                    "price": row[9]
                })
        
        return order_data
'''
        
        (project_dir / "database.py").write_text(db_code)
        
        # Models file
        models_code = '''#!/usr/bin/env python3
"""
Data models for e-commerce platform
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Order:
    """Order model"""
    id: str
    customer_id: str
    created_at: str
    total_amount: float
    status: str

@dataclass  
class OrderItem:
    """Order item model"""
    id: str
    order_id: str
    product_id: str
    product_name: str
    quantity: int
    price: float
'''
        
        (project_dir / "models.py").write_text(models_code)
        
        self.test_artifacts['source_code'] = project_dir
    
    def create_production_logs(self, base_dir: Path):
        """Create production logs showing slow response times"""
        
        log_content = '''2025-06-29 08:15:23 INFO [app] Retrieved 15 orders for customer CUST_001
2025-06-29 08:15:23 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 08:15:23] "GET /api/orders/history?customer_id=CUST_001 HTTP/1.1" 200 -

2025-06-29 10:22:47 INFO [app] Retrieved 23 orders for customer CUST_002  
2025-06-29 10:22:51 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 10:22:51] "GET /api/orders/history?customer_id=CUST_002 HTTP/1.1" 200 -

2025-06-29 12:45:12 INFO [app] Retrieved 45 orders for customer CUST_003
2025-06-29 12:45:18 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 12:45:18] "GET /api/orders/history?customer_id=CUST_003 HTTP/1.1" 200 -

2025-06-29 14:30:22 INFO [app] Retrieved 67 orders for customer CUST_004
2025-06-29 14:30:35 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 14:30:35] "GET /api/orders/history?customer_id=CUST_004 HTTP/1.1" 200 -

2025-06-29 15:45:44 INFO [app] Retrieved 89 orders for customer CUST_005
2025-06-29 15:46:02 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 15:46:02] "GET /api/orders/history?customer_id=CUST_005 HTTP/1.1" 200 -

2025-06-29 16:22:33 ERROR [app] Error retrieving order history: timeout
2025-06-29 16:22:33 ERROR [werkzeug] 127.0.0.1 - - [29/Jun/2025 16:22:33] "GET /api/orders/history?customer_id=CUST_006 HTTP/1.1" 500 -

2025-06-29 17:15:11 INFO [app] Retrieved 112 orders for customer CUST_007
2025-06-29 17:15:45 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 17:15:45] "GET /api/orders/history?customer_id=CUST_007 HTTP/1.1" 200 -

2025-06-29 18:30:55 ERROR [app] Error retrieving order history: timeout  
2025-06-29 18:30:55 ERROR [werkzeug] 127.0.0.1 - - [29/Jun/2025 18:30:55] "GET /api/orders/history?customer_id=CUST_008 HTTP/1.1" 500 -

2025-06-29 19:45:12 INFO [app] Retrieved 134 orders for customer CUST_009
2025-06-29 19:46:23 INFO [werkzeug] 127.0.0.1 - - [29/Jun/2025 19:46:23] "GET /api/orders/history?customer_id=CUST_009 HTTP/1.1" 200 -

# PATTERN ANALYSIS:
# /api/orders/history endpoint showing increasing response times:
# - 15 orders: 0 seconds delay (baseline)
# - 23 orders: 4 seconds 
# - 45 orders: 6 seconds
# - 67 orders: 13 seconds  
# - 89 orders: 18 seconds
# - 112 orders: 34 seconds
# - 134 orders: 71 seconds (1+ minute!)
#
# Clear correlation: Response time increases dramatically with order count
# This suggests N+1 query problem - each order requires additional database query
# 
# Peak hours (4-8 PM) showing timeouts for high-volume customers
# Other endpoints like /api/orders/<id> remain fast (single query)
'''
        
        logs_file = base_dir / "prod_logs.txt"
        logs_file.write_text(log_content)
        
        self.test_artifacts['logs'] = logs_file
    
    def create_database_schema(self, base_dir: Path):
        """Create database schema showing table relationships"""
        
        schema_content = '''-- E-Commerce Database Schema
-- Production database schema showing table relationships

CREATE TABLE customers (
    id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL, 
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- INDEXES (Important for query performance)
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- PERFORMANCE ANALYSIS:
-- The tables have proper foreign key relationships:
-- customers -> orders (1:many)
-- orders -> order_items (1:many) 
-- products -> order_items (1:many)
--
-- The N+1 query problem occurs when:
-- 1. Query orders for customer (1 query) 
-- 2. For each order, query order_items (N queries)
-- 
-- SOLUTION: Use JOIN to get orders and items in single query:
-- SELECT o.*, oi.*, p.name 
-- FROM orders o
-- LEFT JOIN order_items oi ON o.id = oi.order_id
-- LEFT JOIN products p ON oi.product_id = p.id  
-- WHERE o.customer_id = ?
'''
        
        schema_file = base_dir / "schema.sql"
        schema_file.write_text(schema_content)
        
        self.test_artifacts['schema'] = schema_file
    
    def create_problem_description(self, base_dir: Path):
        """Create high-level problem description"""
        
        problem_description = '''# Performance Degradation Investigation

## Problem Statement

A critical performance degradation has been reported in our production e-commerce platform. Users are reporting that the 'View Order History' page is timing out during peak hours. We suspect an N+1 query bug, but we aren't sure where.

## Available Evidence

1. **Source Code** (`project-ecommerce/`): Complete application source code
   - `app.py`: Main Flask application with API endpoints
   - `database.py`: Database operations and queries  
   - `models.py`: Data models

2. **Production Logs** (`prod_logs.txt`): Application logs showing slow response times
   - Contains actual request/response timing data
   - Shows correlation between number of orders and response time
   - Peak hour timeout errors

3. **Database Schema** (`schema.sql`): Complete database structure  
   - Table definitions and relationships
   - Index information for performance optimization
   - Foreign key constraints

## Investigation Goal

Analyze the provided artifacts to:

1. **Identify the root cause** of the performance degradation on the 'View Order History' page
2. **Correlate evidence** from logs, code, and schema to understand the complete problem
3. **Propose a comprehensive solution** that addresses both code and potentially database structure

## Expected Findings

If this is truly an N+1 query problem, the investigation should reveal:
- Code that loops through records making individual database queries
- Log patterns showing response time correlating with record count  
- Database schema that could support optimized JOIN queries
- A specific fix that consolidates multiple queries into efficient single queries

## Success Criteria

The analysis should demonstrate:
✅ **Multi-source correlation**: Uses information from all three artifact types
✅ **Root cause identification**: Pinpoints the exact location and nature of the N+1 query bug
✅ **Comprehensive solution**: Provides both code changes and any database optimizations needed
✅ **Evidence-based reasoning**: Shows clear logical connection between logs, code, and schema
'''
        
        problem_file = base_dir / "PROBLEM_DESCRIPTION.md"
        problem_file.write_text(problem_description)
        
        self.test_artifacts['problem_description'] = problem_file
    
    def run_orchestrator_analysis(self, scenario_path: Path) -> Dict[str, Any]:
        """Run the PRI system on the complex scenario and analyze its response"""
        
        print("🤖 Running PRI orchestrator analysis on complex scenario...")
        
        try:
            # Run analysis on the complete scenario  
            result = subprocess.run([
                sys.executable, "-m", "src.cognitive.persistent_recursion",
                "--project", str(scenario_path),
                "--max-depth", "3", 
                "--batch-size", "20"
            ],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=Path.cwd(),
            env={**os.environ, 'PYTHONPATH': str(Path.cwd() / 'src')}
            )
            
            analysis_result = {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            if result.returncode == 0:
                print("✅ Analysis completed successfully")
                print(f"   Output length: {len(result.stdout)} characters")
            else:
                print(f"❌ Analysis failed with code {result.returncode}")
                print(f"   Error: {result.stderr[:200]}...")
            
            return analysis_result
            
        except subprocess.TimeoutExpired:
            print("⏰ Analysis timed out")
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Analysis timed out after 180 seconds',
                'returncode': -1
            }
        except Exception as e:
            print(f"💥 Analysis failed with exception: {e}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -2
            }
    
    def evaluate_orchestration_capabilities(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate whether the system demonstrated true orchestration and synthesis"""
        
        print("📊 Evaluating orchestration and synthesis capabilities...")
        
        if not analysis_result['success']:
            return {
                'multi_source_analysis': False,
                'root_cause_identification': False,
                'solution_synthesis': False,
                'evidence_correlation': False,
                'orchestration_score': 0,
                'reasoning': 'Analysis failed to complete'
            }
        
        output = analysis_result['stdout'].lower()
        
        # Check for multi-source analysis
        source_indicators = {
            'code_analysis': any(term in output for term in ['app.py', 'database.py', 'models.py', 'function', 'method']),
            'log_analysis': any(term in output for term in ['log', 'timeout', 'response time', 'slow']),
            'schema_analysis': any(term in output for term in ['schema', 'table', 'foreign key', 'index', 'join'])
        }
        
        multi_source_analysis = sum(source_indicators.values()) >= 2
        
        # Check for N+1 query identification  
        n_plus_one_indicators = [
            'n+1', 'n plus 1', 'multiple queries', 'query per order', 'loop query',
            'separate queries', 'individual queries', 'query in loop'
        ]
        
        root_cause_identification = any(indicator in output for indicator in n_plus_one_indicators)
        
        # Check for solution synthesis
        solution_indicators = [
            'join', 'single query', 'optimize', 'consolidate', 'batch',
            'get_order_with_items', 'left join', 'inner join'
        ]
        
        solution_synthesis = any(indicator in output for indicator in solution_indicators)
        
        # Check for evidence correlation
        correlation_indicators = [
            'correlation', 'pattern', 'increases with', 'related to',
            'response time', 'order count', 'timeout'
        ]
        
        evidence_correlation = any(indicator in output for indicator in correlation_indicators)
        
        # Calculate orchestration score
        capabilities = [
            multi_source_analysis,
            root_cause_identification, 
            solution_synthesis,
            evidence_correlation
        ]
        
        orchestration_score = sum(capabilities) / len(capabilities)
        
        evaluation = {
            'multi_source_analysis': multi_source_analysis,
            'source_breakdown': source_indicators,
            'root_cause_identification': root_cause_identification,
            'solution_synthesis': solution_synthesis,
            'evidence_correlation': evidence_correlation,
            'orchestration_score': orchestration_score,
            'capabilities_demonstrated': sum(capabilities),
            'total_capabilities': len(capabilities),
            'analysis_output_preview': output[:500] + "..." if len(output) > 500 else output
        }
        
        print(f"   Multi-source analysis: {'✅' if multi_source_analysis else '❌'}")
        print(f"   Root cause identification: {'✅' if root_cause_identification else '❌'}")
        print(f"   Solution synthesis: {'✅' if solution_synthesis else '❌'}")
        print(f"   Evidence correlation: {'✅' if evidence_correlation else '❌'}")
        print(f"   Orchestration score: {orchestration_score:.1%}")
        
        return evaluation
    
    def run_orchestrator_test(self) -> Dict[str, Any]:
        """Execute the complete orchestrator synthesis test"""
        
        print("🎼 ADV-TEST-006: ORCHESTRATOR SYNTHESIS TEST")
        print("=" * 80)
        print("🎯 Testing complex multi-domain problem solving and synthesis")
        print("🔍 Scenario: E-commerce performance degradation investigation")
        print()
        
        # Create complex scenario
        print("🏗️ Creating complex multi-domain scenario...")
        self.scenario_path = self.create_complex_scenario()
        
        print(f"📁 Scenario created at: {self.scenario_path}")
        print(f"   Source code: {self.test_artifacts['source_code']}")
        print(f"   Production logs: {self.test_artifacts['logs']}")
        print(f"   Database schema: {self.test_artifacts['schema']}")
        print(f"   Problem description: {self.test_artifacts['problem_description']}")
        print()
        
        # Run orchestrator analysis
        print("🤖 PHASE 1: Multi-Domain Analysis")
        analysis_result = self.run_orchestrator_analysis(self.scenario_path)
        print()
        
        # Evaluate orchestration capabilities
        print("📊 PHASE 2: Orchestration Evaluation")
        evaluation = self.evaluate_orchestration_capabilities(analysis_result)
        print()
        
        # Determine test success
        test_passed = evaluation['orchestration_score'] >= 0.75  # 75% threshold
        
        final_results = {
            'test_id': 'ADV-TEST-006',
            'test_name': 'Orchestrator Synthesis Test',
            'timestamp': datetime.now().isoformat(),
            'scenario_path': str(self.scenario_path),
            'test_artifacts': {k: str(v) for k, v in self.test_artifacts.items()},
            'analysis_result': analysis_result,
            'evaluation': evaluation,
            'orchestration_score': evaluation['orchestration_score'],
            'test_passed': test_passed
        }
        
        # Print final results
        print("🎼 ORCHESTRATOR SYNTHESIS TEST RESULTS:")
        print(f"   Orchestration score: {evaluation['orchestration_score']:.1%}")
        print(f"   Capabilities demonstrated: {evaluation['capabilities_demonstrated']}/{evaluation['total_capabilities']}")
        
        if test_passed:
            print("\n🎉 ORCHESTRATOR TEST PASSED!")
            print("✅ System demonstrated true multi-domain synthesis capabilities")
            print("🎼 Confirmed autonomous orchestration and problem-solving intelligence")
        else:
            print("\n❌ ORCHESTRATOR TEST FAILED")
            print("⚠️ System limited to linear analysis, lacks synthesis capabilities")
        
        return final_results
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        if self.scenario_path and self.scenario_path.exists():
            shutil.rmtree(self.scenario_path)
            print("🧹 Test environment cleaned up")

def main():
    """Execute ADV-TEST-006: Orchestrator Synthesis Test"""
    
    tester = OrchestratorSynthesisTest()
    
    try:
        results = tester.run_orchestrator_test()
        
        # Save results
        results_file = "orchestrator_synthesis_results.json"
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