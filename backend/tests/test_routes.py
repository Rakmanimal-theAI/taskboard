class TestAuthRoutes:
    def test_register_success(self, client, sample_user_data):
        response = client.post("/auth/register", json=sample_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["name"] == sample_user_data["name"]
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client, sample_user_data):
        client.post("/auth/register", json=sample_user_data)
        response = client.post("/auth/register", json=sample_user_data)
        assert response.status_code == 409

    def test_login_success(self, client, sample_user_data, registered_user):
        response = client.post("/auth/login", json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client, sample_user_data, registered_user):
        response = client.post("/auth/login", json={
            "email": sample_user_data["email"],
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_unknown_email(self, client):
        response = client.post("/auth/login", json={
            "email": "nobody@example.com",
            "password": "pass"
        })
        assert response.status_code == 404

class TestProjectRoutes:
    def test_create_project(self, client, auth_headers, sample_project_data):
        response = client.post("/api/projects", json=sample_project_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_project_data["title"]
        assert data["description"] == sample_project_data["description"]

    def test_get_projects(self, client, auth_headers, created_project):
        response = client.get("/api/projects", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_single_project(self, client, auth_headers, created_project):
        response = client.get(f"/api/projects/{created_project['id']}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == created_project["id"]

    def test_get_nonexistent_project(self, client, auth_headers):
        response = client.get("/api/projects/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_project(self, client, auth_headers, created_project):
        response = client.put(
            f"/api/projects/{created_project['id']}",
            json={"title": "Updated Title", "description": "Updated desc"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    def test_delete_project(self, client, auth_headers, created_project):
        response = client.delete(f"/api/projects/{created_project['id']}", headers=auth_headers)
        assert response.status_code == 200
        get_response = client.get("/api/projects", headers=auth_headers)
        assert len(get_response.json()) == 0

    def test_unauthenticated_request(self, client):
        response = client.get("/api/projects")
        print(response.status_code, response.json())
        assert response.status_code in (401, 403)

class TestTaskRoutes:
    def test_create_task(self, client, auth_headers, created_project, sample_task_data):
        response = client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json=sample_task_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["status"] == "todo"

    def test_get_tasks(self, client, auth_headers, created_project, sample_task_data):
        client.post(f"/api/projects/{created_project['id']}/tasks", json=sample_task_data, headers=auth_headers)
        response = client.get(f"/api/projects/{created_project['id']}/tasks", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_update_task(self, client, auth_headers, created_project, sample_task_data):
        create_response = client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json=sample_task_data,
            headers=auth_headers
        )
        task_id = create_response.json()["id"]
        response = client.put(
            f"/api/projects/{created_project['id']}/tasks/{task_id}",
            json={"title": "Updated Task", "priority": "high"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Task"

    def test_delete_task(self, client, auth_headers, created_project, sample_task_data):
        create_response = client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json=sample_task_data,
            headers=auth_headers
        )
        task_id = create_response.json()["id"]
        response = client.delete(
            f"/api/projects/{created_project['id']}/tasks/{task_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        get_response = client.get(f"/api/projects/{created_project['id']}/tasks", headers=auth_headers)
        assert len(get_response.json()) == 0

class TestProjectSecurity:
    def test_user_cannot_access_other_users_project(self, client, created_project, sample_user_data):
        # Register a second user and log in
        client.post("/auth/register", json={
            "email": "other@example.com",
            "name": "otheruser",
            "password": "password123"
        })
        login = client.post("/auth/login", json={
            "email": "other@example.com",
            "password": "password123"
        })
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = client.get(
            f"/api/projects/{created_project['id']}",
            headers=other_headers
        )
        assert response.status_code == 404  # Should not expose it exists

    def test_user_cannot_delete_other_users_project(self, client, created_project):
        client.post("/auth/register", json={
            "email": "attacker@example.com",
            "name": "attacker",
            "password": "password123"
        })
        login = client.post("/auth/login", json={
            "email": "attacker@example.com",
            "password": "password123"
        })
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = client.delete(
            f"/api/projects/{created_project['id']}",
            headers=other_headers
        )
        assert response.status_code == 404

class TestTaskStatus:
    def test_update_task_status(self, client, auth_headers, created_project):
        create = client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json={"title": "A task", "priority": "medium"},
            headers=auth_headers
        )
        task_id = create.json()["id"]

        response = client.put(
            f"/api/projects/{created_project['id']}/tasks/{task_id}",
            json={"title": "A task", "priority": "medium", "status": "in_progress"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_invalid_task_status(self, client, auth_headers, created_project):
        create = client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json={"title": "A task", "priority": "medium"},
            headers=auth_headers
        )
        task_id = create.json()["id"]

        response = client.put(
            f"/api/projects/{created_project['id']}/tasks/{task_id}",
            json={"title": "A task", "priority": "medium", "status": "invalid_status"},
            headers=auth_headers
        )
        assert response.status_code == 422