import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

TEST_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield

    db = next(get_db())
    db.execute(text("TRUNCATE TABLE books, users RESTART IDENTITY CASCADE;"))
    db.commit()
