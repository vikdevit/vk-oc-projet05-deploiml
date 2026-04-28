import pytest
from app.db.database import get_connection

@pytest.fixture
def db_conn():
    conn = get_connection()
    yield conn
    conn.close()
