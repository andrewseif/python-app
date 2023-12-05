import subprocess
import json


def test_hello_world_endpoint():
    result = subprocess.run(
        ['curl', 'http://localhost:8080/'],
        capture_output=True,
        text=True
    )
    response = json.loads(result.stdout)
    assert response == {"message": "Hello World"}


def test_health_check_endpoint():
    result = subprocess.run(
        ['curl', 'http://localhost:8080/health'],
        capture_output=True,
        text=True
    )
    response = json.loads(result.stdout)
    assert response["status"] == "success"
