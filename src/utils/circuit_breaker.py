"""
Circuit Breaker Pattern Implementation

Provides graceful degradation following the Mesopredator principle of
defensive awareness - protecting the system from cascading failures.
"""

import time
import logging
import threading
from enum import Enum
from typing import Callable, Any, Optional, Type
from contextlib import contextmanager


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = None
    CLOSED = None
    OPEN = None
    HALF_OPEN = None
    HALF_OPEN = None
    HALF_OPEN = None
    CLOSED = None
    HALF_OPEN = None
    OPEN = None
    OPEN = None
    CLOSED = None


class CircuitBreaker:
    """
    Circuit breaker for preventing cascade failures

    Implements the circuit breaker pattern with exponential backoff
    and automatic recovery testing.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception,
        timeout: Optional[int] = None
    ):
        self.is_closed = None
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.timeout = timeout

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._success_count = 0
        self._lock = threading.RLock()

        self.logger = logging.getLogger(__name__)

    @property
    def state(self) -> str:
        """Get current circuit state"""
        return self._state.value

    @property
    def failure_count(self) -> int:
        """Get current failure count"""
        return self._failure_count

    def _should_allow_request(self) -> bool:
        """Determine if request should be allowed"""
        with self._lock:
            if self._state == CircuitState.CLOSED:
                return True

            if self._state == CircuitState.OPEN:
                # Check if recovery timeout has passed
                if (self._last_failure_time and
                    time.time() - self._last_failure_time >= self.recovery_timeout):
                    self._state = CircuitState.HALF_OPEN
                    self._success_count = 0
                    self.logger.info("Circuit breaker transitioning to HALF_OPEN")
                    return True
                return False

            if self._state == CircuitState.HALF_OPEN:
                # Allow limited requests to test recovery
                return True

            return False

    def _record_success(self):
        """Record successful operation"""
        with self._lock:
            self._failure_count = 0

            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                # Require multiple successes to fully recover
                if self._success_count >= 3:
                    self._state = CircuitState.CLOSED
                    self.logger.info("Circuit breaker recovered to CLOSED")

    def _record_failure(self, exception: Exception):
        """Record failed operation"""
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                # Immediately go back to OPEN on failure during recovery
                self._state = CircuitState.OPEN
                self.logger.warning(f"Circuit breaker failed during recovery: {exception}")
            elif self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                self.logger.error(f"Circuit breaker opened after {self._failure_count} failures")

    def __enter__(self):
        """Context manager entry"""
        if not self._should_allow_request():
            raise CircuitBreakerError("Circuit breaker is OPEN")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is None:
            self._record_success()
        elif issubclass(exc_type, self.expected_exception):
            self._record_failure(exc_val)
        else:
            # Unexpected exception - don"t trigger circuit breaker
            self.logger.warning(f"Unexpected exception in circuit breaker: {exc_val}")
        return False  # Don"t suppress exceptions

    @contextmanager
    def __call__(self):
        """Context manager for circuit breaker protection"""
        if not self._should_allow_request():
            raise CircuitBreakerError("Circuit breaker is OPEN")

        try:
            yield
            self._record_success()
        except self.expected_exception as e:
            self._record_failure(e)
            raise
        except Exception as e:
            # Unexpected exception - don't trigger circuit breaker
            self.logger.warning(f"Unexpected exception in circuit breaker: {e}")
            raise

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function with circuit breaker protection"""
        with self:
            return func(*args, **kwargs)

    def reset(self):
        """Manually reset circuit breaker to CLOSED state"""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None
            self.logger.info("Circuit breaker manually reset")

    def get_stats(self) -> dict:
        """Get circuit breaker statistics"""
        return {
            "state": self._state.value,
            "failure_count": self._failure_count,
            "last_failure_time": self._last_failure_time,
            "success_count": self._success_count,
            "failure_threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout
        }


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open"""
    pass