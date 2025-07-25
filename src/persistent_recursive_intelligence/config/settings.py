from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # API Configuration
    host: str = Field(default="0.0.0.0", env="METRICS_HOST")
    port: int = Field(default=8000, env="METRICS_PORT")
    workers: int = Field(default=1, env="METRICS_WORKERS")

    # Service Configuration
    service_name: str = Field(default="metrics-baseline", env="SERVICE_NAME")
    version: str = Field(default="1.0.0", env="SERVICE_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Performance Settings
    response_timeout_ms: int = Field(default=50, env="RESPONSE_TIMEOUT_MS")
    max_request_size: int = Field(default=1024*1024, env="MAX_REQUEST_SIZE")  # 1MB

    # Health Check Settings
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")

    # Circuit Breaker Settings
    circuit_breaker_threshold: int = Field(default=5, env="CIRCUIT_BREAKER_THRESHOLD")
    circuit_breaker_timeout: int = Field(default=60, env="CIRCUIT_BREAKER_TIMEOUT")

    # Integration Settings
    trading_bot_url: str = Field(default="", env="TRADING_BOT_URL")
    code_analysis_url: str = Field(default="", env="CODE_ANALYSIS_URL")

    # Security Settings
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    class Config:
        pass

# Global settings instance