from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from kibicara.model import Mapping
from kibicara.webapi import router


app = FastAPI()
app.include_router(router, prefix='/api')
client = TestClient(app)
Mapping.create_all()


def test_register_missing_body():
    response = client.post('/api/admin/register/')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
