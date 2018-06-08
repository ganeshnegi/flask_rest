import os
import tempfile

import pytest
import project

@pytest.fixture
def client():
    fo, project.app.config['DATABASE'] = tempfile.mkstemp()
    project.app.config['TESTING'] = True
    client = project.app.test_client()

    with project.app.app_context():
        project.init_db()
    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])