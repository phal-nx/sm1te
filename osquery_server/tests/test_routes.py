import os
import tempfile

import mock
import pytest
import redis

from osquery_server import flaskr


@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


@mock.patch.object(redis.Redis, 'mset')
def test_enrollment(client, test_mset):
    """Start with a blank database."""
    enrollment_key = 'alksjdf'
    flaskr.app.g.ENROLL_SECRET = enrollment_key
    response = client.post('/enrollment', data=dict(
        enroll_secret=enrollment_key,
        host_identifier='phil-desktop',
        host_details={'test'}
    ), follow_redirects=True)
    assert test_mset.called

    # Bad enrollment key
    response = client.post('/enrollment', data=dict(
        enroll_secret='fake',
        host_identifier='phil-desktop',
        host_details={'test'}
    ), follow_redirects=True)
    assert not test_mset.called


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data