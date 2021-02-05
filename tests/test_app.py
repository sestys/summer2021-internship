import pytest
import json

from app import app
from app.utils import distance


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_no_args(client):
    rv = client.get('/discovery')
    response = json.loads(rv.data)
    assert not response['sections'][0]['restaurants'] and \
           not response['sections'][1]['restaurants'] and \
           not response['sections'][2]['restaurants']


def test_location_in_limits(client):
    cases = [[181., 0.], [-181., 0], [13., 180.01], [-34.2, -180.008]]
    for lat, lon in cases:
        rv = client.get('/discovery?lat={:.4f}&lon={:.4f}'.format(lat, lon))
        response = json.loads(rv.data)
        assert not response['sections'][0]['restaurants'] and \
               not response['sections'][1]['restaurants'] and \
               not response['sections'][2]['restaurants']


def test_distance_trivial():
    assert distance(0.0, 0.0, 0.0, 0.0) == 0


def test_distance():
    assert 69.2 < distance(51.5, 0, 51.5, -1.) < 69.3
