import pytest
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, Session as SQLModelSession
from fastapi.testclient import TestClient
from .main import app, get_session
from .models import UserCreate, UserRead
import os
from dotenv import load_dotenv
import os
load_dotenv()


def PG_Engine():
    postgresql_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('TEAM_UP_DB')}"
    # Remove echo on production
    engine = create_engine(postgresql_url, echo=False)
    SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)
    return engine


@pytest.fixture(name="session")
def session_fixture():
    engine = PG_Engine()
    SQLModel.metadata.create_all(engine)
    with SQLModelSession(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_new_user(client: TestClient):
    # create a mock user object
    user = UserCreate(
        username="testuser",
        password="testpassword",
        email="testuser@example.com",
        mobile="1234567890",
        first_name="Test",
        last_name="User",
        user_photo=None,
        disabled=True
    )

    # make a post request to the /new_user endpoint with the user data
    response = client.post("/new_user", json=user.dict())
    data = response.json()
    # assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # assert that the response data matches the expected user data
    expected_user = UserRead(
        id=1,
        username="testuser",
        email="testuser@example.com",
        mobile="1234567890",
        first_name="Test",
        last_name="User",
        user_photo=None,
        disabled=True
    )
    assert response.json() == expected_user.dict()
