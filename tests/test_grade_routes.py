from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.grade_schemas import Grade


@pytest.fixture(scope="module")
def setup_database():
    from _pytest.monkeypatch import MonkeyPatch
    monkeypatch = MonkeyPatch()
    monkeypatch.setenv("DB_USER", "testuser")
    monkeypatch.setenv("DB_PASSWORD", "testpassword")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")
    yield
    monkeypatch.undo()


@pytest.fixture(scope="module")
def app(setup_database):
    from app.server import app
    return app


@pytest.fixture
def db_session():
    return MagicMock()


@pytest.fixture(scope="module")
def test_client(app):
    client = TestClient(app)
    yield client


@pytest.mark.asyncio
async def test_get_grades_by_student_success(db_session, test_client):
    # Create some sample grades
    grade1 = Grade(student_id=1, subject_id=1, grade=90)
    grade2 = Grade(student_id=1, subject_id=2, grade=85)

    db_session.query.return_value.filter_by.return_value.all.return_value = [grade1, grade2]

    response = test_client.get('/grades/student/1')
    assert response.status_code == 200
    assert response.json()['data']  # Assert that data exists


@pytest.mark.asyncio
async def test_get_grades_by_student_not_found(db_session):
    response = await client.get('/student/999')
    assert response.status_code == 404
    assert response.json()['error'] == 'No grades found for this student'


@pytest.mark.asyncio
async def test_get_grades_by_student_validation_error(client):
    # Assuming student_id must be an integer
    response = await client.get('/student/abc')
    assert response.status_code == 422
    # Add assertions for specific validation error details if needed


# Mocking a database error requires more complex setup
@pytest.mark.asyncio
@pytest.mark.parametrize("mock_db_error", [True], indirect=True)
async def test_get_grades_by_student_db_error(client, mock_db_error):
    ...
