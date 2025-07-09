# Mesopredator PRI - Comprehensive API Documentation

**Version:** 2.0.0  
**Status:** Production Ready  
**Security Level:** Defense-in-Depth Hardened  

---

## 🚀 Quick Start

```bash
# Start the PRI API server
cd /home/gusfromspace/Development/persistent-recursive-intelligence
python -m src.api.rest.simple_api

# API Available at: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
```

## 📋 Table of Contents

1. [Authentication & Security](#authentication--security)
2. [Core Analysis API](#core-analysis-api)
3. [Memory Intelligence API](#memory-intelligence-api)
4. [Code Connector API](#code-connector-api)
5. [Security & Safety API](#security--safety-api)
6. [Feature Flags API](#feature-flags-api)
7. [Metrics & Monitoring API](#metrics--monitoring-api)
8. [CLI Integration API](#cli-integration-api)
9. [WebSocket Real-time API](#websocket-real-time-api)
10. [Error Handling](#error-handling)
11. [SDK & Client Libraries](#sdk--client-libraries)

---

## 🔐 Authentication & Security

### API Key Authentication
```http
POST /api/v1/auth/generate-key
Authorization: Bearer <admin-token>
```

**Request:**
```json
{
  "name": "analysis-service",
  "permissions": ["analysis:read", "memory:write"],
  "expires_in_days": 30
}
```

**Response:**
```json
{
  "api_key": "pk_live_abc123...",
  "permissions": ["analysis:read", "memory:write"],
  "expires_at": "2025-08-02T10:30:00Z",
  "rate_limits": {
    "requests_per_hour": 1000,
    "concurrent_requests": 10
  }
}
```

### Security Headers (Required)
```http
Authorization: Bearer pk_live_abc123...
X-PRI-Client-Version: 2.0.0
X-PRI-Request-ID: req_12345
Content-Type: application/json
```

---

## 🧠 Core Analysis API

### 1. Project Analysis

#### Comprehensive Project Scan
```http
POST /api/v1/analysis/project
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "project_path": "/path/to/project",
  "analysis_config": {
    "focus": "security",
    "max_depth": 3,
    "enable_learning": true,
    "batch_size": 20,
    "include_patterns": ["**/*.py", "**/*.js"],
    "exclude_patterns": ["**/node_modules/**", "**/venv/**"]
  },
  "output_format": "detailed",
  "async_processing": true
}
```

**Response:**
```json
{
  "analysis_id": "analysis_abc123",
  "status": "processing",
  "project_path": "/path/to/project",
  "estimated_completion": "2025-07-03T15:45:00Z",
  "progress_url": "/api/v1/analysis/analysis_abc123/progress",
  "webhook_url": null
}
```

#### Get Analysis Results
```http
GET /api/v1/analysis/{analysis_id}
Authorization: Bearer pk_live_abc123...
```

**Response:**
```json
{
  "analysis_id": "analysis_abc123",
  "status": "completed",
  "project_path": "/path/to/project",
  "summary": {
    "total_files": 156,
    "issues_found": 23,
    "security_rating": "B+",
    "quality_score": 87.5,
    "analysis_duration": 45.2
  },
  "issues": [
    {
      "id": "issue_001",
      "category": "security",
      "severity": "high",
      "file_path": "src/auth.py",
      "line_number": 45,
      "column": 12,
      "title": "Potential SQL Injection",
      "description": "User input used directly in SQL query without sanitization",
      "code_snippet": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
      "recommendation": "Use parameterized queries or ORM methods",
      "confidence": 0.95,
      "cwe_id": "CWE-89",
      "fix_suggestions": [
        {
          "type": "replace",
          "original": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
          "suggested": "query = \"SELECT * FROM users WHERE id = ?\"",
          "safety_score": 98
        }
      ]
    }
  ],
  "patterns_learned": 5,
  "memory_entries_added": 12,
  "performance_metrics": {
    "files_per_second": 3.47,
    "memory_usage_mb": 245,
    "cpu_usage_percent": 15.2
  }
}
```

### 2. File-Level Analysis

#### Analyze Individual File
```http
POST /api/v1/analysis/file
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "file_path": "/path/to/file.py",
  "content": "def vulnerable_function(user_input):\n    return eval(user_input)",
  "language": "python",
  "context": {
    "project_path": "/path/to/project",
    "file_dependencies": ["utils.py", "config.py"]
  }
}
```

**Response:**
```json
{
  "file_path": "/path/to/file.py",
  "language": "python",
  "issues": [
    {
      "id": "eval_security_risk",
      "severity": "critical",
      "line": 2,
      "title": "Code Injection via eval()",
      "description": "eval() function with user input creates code injection vulnerability",
      "cwe_id": "CWE-94",
      "confidence": 0.99
    }
  ],
  "quality_metrics": {
    "complexity": 1,
    "maintainability": 45,
    "test_coverage": 0
  },
  "suggestions": [
    "Replace eval() with safer alternatives like ast.literal_eval()",
    "Add input validation before processing"
  ]
}
```

---

## 🧠 Memory Intelligence API

### 1. Memory Storage

#### Store Pattern or Knowledge
```http
POST /api/v1/memory/store
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "content": {
    "pattern": "SQL injection via string concatenation",
    "code_example": "query = \"SELECT * FROM users WHERE id = \" + user_id",
    "fix_pattern": "Use parameterized queries",
    "languages": ["python", "javascript", "java"]
  },
  "metadata": {
    "type": "security_pattern",
    "severity": "high",
    "cwe_id": "CWE-89",
    "project_context": "web_application",
    "confidence": 0.95,
    "tags": ["sql", "injection", "parameterized_queries"]
  },
  "namespace": "security_patterns"
}
```

**Response:**
```json
{
  "memory_id": "mem_abc123",
  "status": "stored",
  "vector_embedding": true,
  "similarity_indexed": true,
  "namespace": "security_patterns"
}
```

### 2. Memory Search & Retrieval

#### Semantic Pattern Search
```http
POST /api/v1/memory/search
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "query": "database query security patterns",
  "search_type": "semantic",
  "filters": {
    "type": "security_pattern",
    "severity": ["high", "critical"],
    "languages": ["python", "javascript"]
  },
  "limit": 10,
  "similarity_threshold": 0.7,
  "namespace": "security_patterns"
}
```

**Response:**
```json
{
  "query": "database query security patterns",
  "results": [
    {
      "memory_id": "mem_abc123",
      "content": {
        "pattern": "SQL injection via string concatenation",
        "code_example": "query = \"SELECT * FROM users WHERE id = \" + user_id",
        "fix_pattern": "Use parameterized queries"
      },
      "similarity_score": 0.92,
      "metadata": {
        "type": "security_pattern",
        "cwe_id": "CWE-89",
        "confidence": 0.95
      },
      "created_at": "2025-07-01T10:30:00Z"
    }
  ],
  "total_results": 5,
  "search_duration_ms": 23
}
```

### 3. Cross-Project Pattern Transfer

#### Transfer Learned Patterns
```http
POST /api/v1/memory/transfer
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "source_projects": [
    {"path": "/path/to/project1", "weight": 1.0},
    {"path": "/path/to/project2", "weight": 0.8}
  ],
  "target_project": "/path/to/new/project",
  "transfer_config": {
    "pattern_types": ["security", "quality", "performance"],
    "min_confidence": 0.8,
    "adapt_to_context": true,
    "max_patterns": 50
  }
}
```

**Response:**
```json
{
  "transfer_id": "transfer_xyz789",
  "status": "completed",
  "patterns_transferred": 23,
  "adaptations_made": 8,
  "transfer_summary": {
    "security_patterns": 12,
    "quality_patterns": 7,
    "performance_patterns": 4
  },
  "target_project": "/path/to/new/project"
}
```

---

## 🔗 Code Connector API

### 1. Connection Analysis

#### Analyze Code Connections
```http
POST /api/v1/connector/analyze
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "orphaned_files": [
    "/path/to/utils.py",
    "/path/to/cache_helper.py",
    "/path/to/validators.py"
  ],
  "main_files": [
    "/path/to/main.py",
    "/path/to/core/processor.py",
    "/path/to/api/handlers.py"
  ],
  "analysis_config": {
    "threshold": 0.3,
    "max_suggestions": 20,
    "include_reasoning": true,
    "semantic_analysis": true
  }
}
```

**Response:**
```json
{
  "analysis_id": "conn_abc123",
  "connections": [
    {
      "orphaned_file": "/path/to/cache_helper.py",
      "target_file": "/path/to/core/processor.py",
      "connection_score": 0.85,
      "connection_type": "function_import",
      "integration_suggestions": [
        "from utils.cache_helper import CacheManager, clear_cache",
        "Consider integrating at line 45: Function 'process_data' might benefit from caching"
      ],
      "reasoning": [
        "High semantic similarity (0.75) - files work in related domains",
        "Detected potential need (0.65) - main file has TODOs that orphaned file addresses",
        "Good structural compatibility (0.70) - no conflicts detected"
      ],
      "risk_assessment": {
        "import_conflicts": false,
        "dependency_cycles": false,
        "performance_impact": "low"
      }
    }
  ],
  "performance_metrics": {
    "analysis_time_ms": 234,
    "files_analyzed": 6,
    "suggestions_generated": 12
  }
}
```

### 2. Connection Implementation

#### Apply Connection Suggestions
```http
POST /api/v1/connector/apply
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "analysis_id": "conn_abc123",
  "selected_connections": ["conn_001", "conn_003"],
  "safety_config": {
    "backup_files": true,
    "validate_syntax": true,
    "run_tests": false,
    "require_approval": true
  }
}
```

**Response:**
```json
{
  "application_id": "apply_xyz789",
  "status": "pending_approval",
  "changes_preview": [
    {
      "file": "/path/to/core/processor.py",
      "line": 1,
      "type": "import_addition",
      "content": "from utils.cache_helper import CacheManager"
    }
  ],
  "safety_checks": {
    "syntax_valid": true,
    "no_conflicts": true,
    "backup_created": true
  },
  "approval_url": "/api/v1/connector/apply_xyz789/approve"
}
```

---

## 🛡️ Security & Safety API

### 1. Security Validation

#### Validate Code Changes
```http
POST /api/v1/security/validate
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "original_code": "def process_user_input(data):\n    return data.upper()",
  "modified_code": "def process_user_input(data):\n    return eval(data)",
  "context": {
    "file_path": "/path/to/handler.py",
    "function_name": "process_user_input",
    "language": "python"
  }
}
```

**Response:**
```json
{
  "validation_id": "val_abc123",
  "security_status": "BLOCKED",
  "risk_level": "critical",
  "threats_detected": [
    {
      "type": "code_injection",
      "severity": "critical",
      "cwe_id": "CWE-94",
      "description": "eval() function introduces arbitrary code execution vulnerability",
      "confidence": 0.99
    }
  ],
  "safety_score": 5,
  "recommendation": "REJECT - Contains critical security vulnerability"
}
```

### 2. Emergency Controls

#### Trigger Emergency Stop
```http
POST /api/v1/security/emergency-stop
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "reason": "Potential malicious activity detected",
  "scope": "all_operations",
  "immediate": true
}
```

**Response:**
```json
{
  "status": "emergency_stop_activated",
  "timestamp": "2025-07-03T15:30:00Z",
  "operations_halted": ["analysis", "memory_write", "file_operations"],
  "recovery_token": "emergency_recovery_abc123"
}
```

---

## 🚩 Feature Flags API

### 1. Feature Flag Management

#### Get Feature Flag Status
```http
GET /api/v1/features/{flag_name}
Authorization: Bearer pk_live_abc123...
```

**Response:**
```json
{
  "name": "advanced_recursive_analysis",
  "enabled": true,
  "rollout_percentage": 100.0,
  "user_enabled": true,
  "description": "Enable advanced recursive self-improvement analysis",
  "metadata": {
    "created_at": "2025-07-01T10:00:00Z",
    "updated_at": "2025-07-03T14:30:00Z",
    "auto_rollback": true,
    "metrics_threshold": {
      "error_rate": 5.0,
      "analysis_time": 60.0
    }
  }
}
```

#### Update Feature Flag
```http
PATCH /api/v1/features/{flag_name}
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "enabled": true,
  "rollout_percentage": 75.0,
  "user_whitelist": ["user_123", "user_456"]
}
```

### 2. Feature Usage Analytics

#### Record Feature Metrics
```http
POST /api/v1/features/{flag_name}/metrics
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "metric_name": "analysis_time",
  "value": 45.2,
  "user_id": "user_123",
  "context": {
    "project_size": "medium",
    "analysis_type": "security"
  }
}
```

---

## 📊 Metrics & Monitoring API

### 1. System Metrics

#### Get System Health
```http
GET /api/v1/metrics/health
Authorization: Bearer pk_live_abc123...
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-03T15:30:00Z",
  "components": {
    "api_server": {
      "status": "healthy",
      "response_time_ms": 23,
      "uptime_hours": 48.5
    },
    "memory_database": {
      "status": "healthy",
      "memory_count": 1247,
      "last_backup": "2025-07-03T06:00:00Z"
    },
    "vector_search": {
      "status": "healthy",
      "index_size": 2048,
      "search_latency_ms": 12
    },
    "security_systems": {
      "status": "active",
      "threats_blocked_today": 3,
      "last_security_scan": "2025-07-03T15:00:00Z"
    }
  },
  "performance": {
    "requests_per_hour": 156,
    "avg_response_time_ms": 245,
    "error_rate_percent": 0.02
  }
}
```

### 2. Performance Analytics

#### Get Performance Metrics
```http
GET /api/v1/metrics/performance
Authorization: Bearer pk_live_abc123...
Query: ?period=24h&granularity=1h
```

**Response:**
```json
{
  "period": "24h",
  "granularity": "1h",
  "metrics": [
    {
      "timestamp": "2025-07-03T14:00:00Z",
      "analysis_requests": 45,
      "avg_analysis_time_s": 23.4,
      "memory_operations": 156,
      "error_count": 1,
      "cpu_usage_percent": 12.5,
      "memory_usage_mb": 245
    }
  ],
  "summary": {
    "total_analyses": 1087,
    "avg_performance": "excellent",
    "trending": "stable"
  }
}
```

---

## 🖥️ CLI Integration API

### 1. CLI Command Execution

#### Execute CLI Command via API
```http
POST /api/v1/cli/execute
Authorization: Bearer pk_live_abc123...
```

**Request:**
```json
{
  "command": "analyze",
  "args": ["/path/to/project"],
  "options": {
    "--focus": "security",
    "--output-file": "results.json",
    "--verbose": true
  },
  "async_execution": true
}
```

**Response:**
```json
{
  "execution_id": "exec_abc123",
  "command": "analyze /path/to/project --focus security",
  "status": "running",
  "started_at": "2025-07-03T15:30:00Z",
  "estimated_duration_s": 45,
  "progress_url": "/api/v1/cli/exec_abc123/progress"
}
```

### 2. CLI Results Retrieval

#### Get CLI Execution Results
```http
GET /api/v1/cli/{execution_id}/results
Authorization: Bearer pk_live_abc123...
```

**Response:**
```json
{
  "execution_id": "exec_abc123",
  "status": "completed",
  "exit_code": 0,
  "stdout": "Analysis completed successfully. Found 23 issues across 156 files.",
  "stderr": "",
  "output_files": [
    {
      "path": "results.json",
      "size_bytes": 45678,
      "download_url": "/api/v1/cli/exec_abc123/download/results.json"
    }
  ],
  "execution_time_s": 42.3
}
```

---

## 🔄 WebSocket Real-time API

### 1. Real-time Analysis Updates

#### Connect to Analysis Stream
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analysis');

ws.onopen = function() {
    // Subscribe to analysis updates
    ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'analysis_progress',
        analysis_id: 'analysis_abc123'
    }));
};

ws.onmessage = function(event) {
    const update = JSON.parse(event.data);
    console.log('Analysis progress:', update);
};
```

**WebSocket Message Format:**
```json
{
  "type": "analysis_progress",
  "analysis_id": "analysis_abc123",
  "progress": {
    "files_analyzed": 45,
    "total_files": 156,
    "current_file": "/path/to/current/file.py",
    "issues_found": 12,
    "completion_percent": 28.8
  },
  "timestamp": "2025-07-03T15:35:00Z"
}
```

### 2. System Status Stream

#### Monitor System Status
```javascript
const statusWs = new WebSocket('ws://localhost:8000/ws/system');

statusWs.onmessage = function(event) {
    const status = JSON.parse(event.data);
    console.log('System status:', status);
};
```

---

## ⚠️ Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "INVALID_PROJECT_PATH",
    "message": "The specified project path does not exist or is not accessible",
    "details": {
      "path": "/invalid/path",
      "reason": "directory_not_found"
    },
    "request_id": "req_abc123",
    "timestamp": "2025-07-03T15:30:00Z",
    "documentation_url": "https://docs.pri.com/errors/INVALID_PROJECT_PATH"
  }
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted for async processing |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (e.g., duplicate analysis) |
| 422 | Unprocessable Entity | Valid JSON but invalid data |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | System under maintenance |

### Common Error Codes

- `INVALID_API_KEY`: API key is malformed or expired
- `RATE_LIMIT_EXCEEDED`: Too many requests in time window  
- `PROJECT_NOT_FOUND`: Specified project path doesn't exist
- `ANALYSIS_IN_PROGRESS`: Another analysis is already running
- `SECURITY_VIOLATION`: Request blocked by security system
- `FEATURE_DISABLED`: Requested feature is disabled via feature flag
- `MEMORY_LIMIT_EXCEEDED`: System memory limit reached
- `INVALID_FILE_FORMAT`: Unsupported file type or format

---

## 📚 SDK & Client Libraries

### Official SDKs

#### Python SDK
```bash
pip install mesopredator-pri-client
```

```python
from mesopredator_pri import PRIClient

client = PRIClient(api_key='pk_live_abc123...', base_url='http://localhost:8000')

# Analyze project
analysis = client.analyze_project('/path/to/project', focus='security')
print(f"Found {len(analysis.issues)} issues")

# Search memory patterns
patterns = client.search_memory('sql injection patterns', limit=10)
for pattern in patterns:
    print(f"Pattern: {pattern.content}")
```

#### JavaScript/TypeScript SDK
```bash
npm install @mesopredator/pri-client
```

```typescript
import { PRIClient } from '@mesopredator/pri-client';

const client = new PRIClient({
  apiKey: 'pk_live_abc123...',
  baseURL: 'http://localhost:8000'
});

// Analyze project
const analysis = await client.analyzeProject('/path/to/project', {
  focus: 'security',
  enableLearning: true
});

console.log(`Found ${analysis.issues.length} issues`);
```

### Community SDKs

- **Go**: `github.com/community/pri-go-client`
- **Rust**: `pri-rust-client` crate
- **Java**: `com.mesopredator:pri-java-client`
- **C#**: `Mesopredator.PRI.Client` NuGet package

---

## 🔧 Configuration & Deployment

### Environment Variables
```bash
# API Configuration
PRI_API_HOST=0.0.0.0
PRI_API_PORT=8000
PRI_API_WORKERS=4

# Database Configuration  
PRI_DB_PATH=/var/lib/pri/memory.db
PRI_VECTOR_INDEX_PATH=/var/lib/pri/vectors

# Security Configuration
PRI_API_KEY_SECRET=your-secret-key
PRI_RATE_LIMIT_PER_HOUR=1000
PRI_MAX_CONCURRENT_REQUESTS=10

# Feature Flags
PRI_FEATURE_FLAGS_PATH=/etc/pri/feature_flags.json
PRI_ENABLE_WEBSOCKETS=true

# Monitoring
PRI_ENABLE_METRICS=true
PRI_METRICS_PORT=9090
PRI_LOG_LEVEL=INFO
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 8000

CMD ["python", "-m", "src.api.rest.simple_api"]
```

### Health Check Endpoint
```bash
curl -f http://localhost:8000/health || exit 1
```

---

## 📈 Rate Limits & Quotas

| Endpoint Category | Requests/Hour | Concurrent | Notes |
|-------------------|---------------|------------|-------|
| Analysis | 100 | 5 | Resource intensive |
| Memory Operations | 1000 | 20 | Fast operations |
| Search | 500 | 10 | Moderate cost |
| Metrics | 2000 | 50 | Lightweight |
| CLI Integration | 200 | 3 | May spawn processes |

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1625234567
X-RateLimit-Retry-After: 3600
```

---

## 🎯 Best Practices

### 1. Security
- Always use HTTPS in production
- Rotate API keys regularly (max 90 days)
- Implement proper request validation
- Monitor for unusual usage patterns

### 2. Performance
- Use async processing for large projects
- Implement proper caching strategies
- Batch memory operations when possible
- Monitor memory usage during analysis

### 3. Error Handling
- Implement exponential backoff for retries
- Handle rate limits gracefully
- Log all error responses for debugging
- Provide meaningful error messages to users

### 4. Integration
- Use webhooks for long-running operations
- Implement proper timeout handling
- Cache frequently accessed patterns
- Use feature flags for gradual rollouts

---

*This API documentation is automatically generated and kept in sync with the actual implementation. For the latest updates, visit the interactive documentation at `/docs`.*