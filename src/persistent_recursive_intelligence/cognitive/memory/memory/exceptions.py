"""
Memory system exceptions for proper error handling and graceful degradation.
"""


class MemoryError(Exception):
    """Base exception for memory system errors"""
    pass


class StorageError(MemoryError):
    """Storage-related errors (database, file system)"""
    pass


class VectorSearchError(MemoryError):
    """Vector search and embedding errors"""
    pass


class NamespaceError(MemoryError):
    """Namespace-related errors"""
    pass


class ValidationError(MemoryError):
    """Input validation errors"""
    pass


class ConfigurationError(MemoryError):
    """Configuration and setup errors"""
    pass


class CircuitBreakerError(MemoryError):
    """Circuit breaker triggered errors"""
    pass