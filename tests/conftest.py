from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.dependency import get_db
from main import app
from fastapi.testclient import TestClient
import pytest
from app.database import Base


TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL,
                            connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine,
                                autocommit=False,
                                autoflush=False)

# Функция для получения сессии базы данных через dependency injection в FastAPI
def get_test_db() -> Generator[Session, None, None]:
    # Создаём новую сессию для работы с базой данных
    db = TestSessionLocal()
    try:
        # Возвращаем сессию через yield (это позволяет FastAPI автоматически закрывать сессию)
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    # Пересоздаем все таблицы перед тестом
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    # Создаём новую сессию для работы с базой данных
    db = TestSessionLocal()
    try:
        # Возвращаем сессию через yield (это позволяет FastAPI автоматически закрывать сессию)
        yield db
    finally:
        db.close()