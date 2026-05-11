import pytest
from django.contrib.auth import get_user_model
from .models import Project, Task
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    # Using a unique username to avoid conflicts during registration tests
    return User.objects.create_user(username="testuser", password="testpassword")

@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def project(db, user):
    return Project.objects.create(name="Test Project", owner=user)

# --FIXED TESTS--

@pytest.mark.django_db
def test_register_user(client):
    r = client.post("/api/users/register/", {
        "username": "newuser",
        "email": "newuser@example.com", 
        "password": "testpassword",
    }, format="json")
    
    assert r.status_code == 201
    
    
@pytest.mark.django_db
def test_login_user(client, user):
    r = client.post("/api/users/login/",{
        "username": "testuser",
        "password": "testpassword",
    }, format="json")
    
    assert r.status_code == 200
    # SimpleJWT returns 'access' and 'refresh', not 'token'
    assert "access" in r.data 

@pytest.mark.django_db
def test_login_wrong_password(client, user):    
    r = client.post("/api/users/login/", {
        "username": "testuser",
        "password": "wrongpassword",
    }, format="json")
    assert r.status_code == 401
    
@pytest.mark.django_db
def test_create_project(auth_client):
    r = auth_client.post("/api/projects/", {
        "name": "Test Project",
        "description": "This is a test project",
    }, format="json")
    
    assert r.status_code == 201
    assert r.data["name"] == "Test Project"
    # Ensure your Serializer actually includes task_count in its fields
    assert r.data["task_count"] == 0

@pytest.mark.django_db
def test_list_projects_only_own(auth_client, project):
    r = auth_client.get("/api/projects/")
    assert r.status_code == 200
    if isinstance(r.data, dict) and "results" in r.data:
        assert len(r.data["results"]) == 1
    else:
        assert len(r.data) == 1
    
@pytest.mark.django_db
def test_create_task(auth_client, project):
    r = auth_client.post("/api/tasks/", {
        "project": project.id,
        "title": "Test Task",
        "status": "todo",
        "priority": "high",
    }, format="json")
    assert r.status_code == 201
    assert r.data["title"] == "Test Task"

@pytest.mark.django_db
def test_project_stats(auth_client, project, user):
    Task.objects.create(project=project, title="Task 1", status="done", priority="high")
    Task.objects.create(project=project, title="Task 2", status="todo", priority="medium")
    
    # Check your urls.py: ensure this trailing slash matches your config
    r = auth_client.get(f"/api/projects/{project.id}/stats/")
    
    assert r.status_code == 200
    assert r.data["total"] == 2
    assert r.data["done"] == 1
    # Note: If your API returns an integer or string, you might need to adjust this
    assert float(r.data["completion_pct"]) == 50.0
    
@pytest.mark.django_db
def test_unauthenticated_blocked(client):
    r = client.get("/api/projects/")
    assert r.status_code == 401