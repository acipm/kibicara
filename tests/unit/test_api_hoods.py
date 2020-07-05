from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from kibicara.model import Mapping
from kibicara.webapi import router


app = FastAPI()
app.include_router(router, prefix='/api')
client = TestClient(app)
Mapping.create_all()


def test_hood_read_all():
    response = client.get('/api/hoods/')
    assert response.status_code == status.HTTP_200_OK


def test_hood_create_unauthorized():
    response = client.post('/api/hoods/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hood_read_unauthorized():
    response = client.get('/api/hoods/{hood_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hood_update_unauthorized():
    response = client.put('/api/hoods/{hood_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hood_delete_unauthorized():
    response = client.delete('/api/hoods/{hood_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_read_all_unauthorized():
    response = client.get('/api/hoods/{hood_id}/triggers/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_create_unauthorized():
    response = client.post('/api/hoods/{hood_id}/triggers/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_read_unauthorized():
    response = client.get('/api/hoods/{hood_id}/triggers/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_read_all_unauthorized():
    response = client.get('/api/hoods/{hood_id}/triggers/{trigger_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_update_unauthorized():
    response = client.put('/api/hoods/{hood_id}/triggers/{trigger_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_delete_unauthorized():
    response = client.delete('/api/hoods/{hood_id}/triggers/{trigger_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_read_all_unauthorized():
    response = client.get('/api/hoods/{hood_id}/badwords/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_create_unauthorized():
    response = client.post('/api/hoods/{hood_id}/badwords/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_read_unauthorized():
    response = client.get('/api/hoods/{hood_id}/badwords/{badword_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_update_unauthorized():
    response = client.put('/api/hoods/{hood_id}/badwords/{badword_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_delete_unauthorized():
    response = client.delete('/api/hoods/{hood_id}/badwords/{badword_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_read_all_unauthorized():
    response = client.get('/api/hoods/{hood_id}/test/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_create_unauthorized():
    response = client.post('/api/hoods/{hood_id}/test/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_read_unauthorized():
    response = client.get('/api/hoods/{hood_id}/test/{test_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_delete_unauthorized():
    response = client.delete('/api/hoods/{hood_id}/test/{test_id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_message_read_all_unauthorized():
    response = client.get('/api/hoods/{hood_id}/test/{test_id}/messages/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_message_create_unauthorized():
    response = client.post('/api/hoods/{hood_id}/test/{test_id}/messages/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
