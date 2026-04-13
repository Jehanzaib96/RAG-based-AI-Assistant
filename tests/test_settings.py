from backend.app.core.settings import Settings


def test_cors_origins_parsing() -> None:
    settings = Settings(APP_CORS_ORIGINS="http://localhost:3000, http://localhost:8501")
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost:8501"]
