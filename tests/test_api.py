import pytest
from pathlib import Path


@pytest.mark.integration
class TestApi:
    def test_get_empty_routes(self, client):
        response = client.get('/internal/routes')
        assert response.json == []

    def test_add_minimal_route(self, client):
        response = client.post('/internal/routes', json={
            'id': 'route1',
            'path': '/path1',
            'responses': [
                {
                    'id': 'response1',
                    'body': 'response1'
                }
            ]
        })

        assert response.status_code == 201
        assert response.json == {
            'auth': None,
            'id': 'route1',
            'method': 'GET',
            'path': '/path1',
            'response_selection': 'greedy',
            'responses': [
                {
                    'body': 'response1',
                    'delay': None,
                    'headers': {},
                    'id': 'response1',
                    'is_active': True,
                    'repeat': None,
                    'status': 200,
                    'used_count': 0,
                    'weight': 0.5
                }
            ],
            'used_count': 0
        }

    def test_add_full_route(self, client):
        response = client.post('/internal/routes', json={
            'id': 'route1',
            'path': '/endpoint1',
            'method': 'GET',
            'auth': {
                'method': 'basic',
                'username': 'username',
                'password': 'password'
            },
            'response_selection': 'random',
            'responses': [
                {
                    'id': 'response1',
                    'status': 200,
                    'weight': 0.3,
                    'repeat': 3,
                    'delay': [0.1, 0.2],
                    'headers': {
                        'content-type': 'application/json'
                    },
                    'body': {
                        'works': True
                    }
                },
                {
                    'id': 'response2',
                    'status': 500,
                    'weight': 0.1,
                    'repeat': 3,
                    'delay': [0.1, 0.2],
                    'headers': {
                        'content-type': 'application/json'
                    },
                    'body': {
                        'works': True
                    }
                }
            ]
        })

        assert response.status_code == 201
        assert response.json == {
            'auth': {
                'method': 'basic',
                'password': 'password',
                'username': 'username'
            },
            'id': 'route1',
            'method': 'GET',
            'path': '/endpoint1',
            'response_selection': 'random',
            'responses': [
                {
                    'body': {
                        'works': True
                    },
                    'delay': [
                        0.1,
                        0.2
                    ],
                    'headers': {
                        'content-type': 'application/json'
                    },
                    'id': 'response1',
                    'is_active': True,
                    'repeat': 3,
                    'status': 200,
                    'used_count': 0,
                    'weight': 0.3
                },
                {
                    'body': {
                        'works': True
                    },
                    'delay': [
                        0.1,
                        0.2
                    ],
                    'headers': {
                        'content-type': 'application/json'
                    },
                    'id': 'response2',
                    'is_active': True,
                    'repeat': 3,
                    'status': 500,
                    'used_count': 0,
                    'weight': 0.1
                }
            ],
            'used_count': 0
        }


    def test_append_route(self, client):
        client.post('/internal/routes', json={
            'id': 'route1',
            'path': '/endpoint1',
            'responses': [
                {
                    'id': 'response1',
                    'body': 'response1'
                }
            ]
        })

        client.post('/internal/routes', json={
            'id': 'route2',
            'path': '/endpoint2',
            'responses': [
                {
                    'id': 'response2',
                    'body': 'response2'
                }
            ]
        })

        response = client.get('/internal/routes')
        assert response.status_code == 200
        assert response.json == [
            {
                'auth': None,
                'id': 'route1',
                'method': 'GET',
                'path': '/endpoint1',
                'response_selection': 'greedy',
                'responses': [
                    {
                        'body': 'response1',
                        'delay': None,
                        'headers': {},
                        'id': 'response1',
                        'is_active': True,
                        'repeat': None,
                        'status': 200,
                        'used_count': 0,
                        'weight': 0.5
                    }
                ],
                'used_count': 0
            },
            {
                'auth': None,
                'id': 'route2',
                'method': 'GET',
                'path': '/endpoint2',
                'response_selection': 'greedy',
                'responses': [
                    {
                        'body': 'response2',
                        'delay': None,
                        'headers': {},
                        'id': 'response2',
                        'is_active': True,
                        'repeat': None,
                        'status': 200,
                        'used_count': 0,
                        'weight': 0.5
                    }
                ],
                'used_count': 0
            }
        ]

    def test_reset_routes(self, client):
        client.post('/internal/route', json={
            'id': 'route1',
            'path': '/endpoint1',
            'responses': [
                {
                    'id': 'response1',
                    'body': 'response1'
                }
            ]
        })

        client.delete('/internal/routes')
        response = client.get('/internal/routes')
        assert response.status_code == 200
        assert response.json == []


    def test_create_and_delete_route(self, client):
        client.post('/internal/routes', json={
            'id': 'route1',
            'path': '/endpoint1',
            'responses': [
                {
                    'id': 'response1',
                    'body': 'response1'
                }
            ]
        })

        response = client.delete('/internal/routes/route1')
        assert response.status_code == 204
        
        response = client.get('/internal/routes')
        assert response.status_code == 200
        assert response.json == []