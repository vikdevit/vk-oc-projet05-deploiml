import pytest
import os
from app.db.database import get_connection

@pytest.fixture
def db_conn():
    
    if os.getenv("CI") == "true":
        pytest.skip("Skipping DB tests in CI")

    conn = get_connection()
    yield conn
    conn.close()
