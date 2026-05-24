import pytest
from unittest.mock import patch
from app.models import User, Item

class TestUserRoutes:
    """Test user API endpoints"""
    
    def test_create_user_success(self, client, sample_user_data):
        """Test successful user creation"""
        response = client.post("/users/", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]
        assert "id" in data
        assert "password" not in data
    
    def test_create_user_duplicate_email(self, client, sample_user_data, db_session):
        """Test creating user with existing email"""
        # Create first user
        client.post("/users/", json=sample_user_data)
        
        # Try to create second user with same email
        response = client.post("/users/", json=sample_user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_get_user_by_id(self, client, sample_user_data, db_session):
        """Test retrieving a user by ID"""
        # Create user first
        create_response = client.post("/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Get user
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        assert response.json()["email"] == sample_user_data["email"]
        assert response.json()["id"] == user_id
    
    def test_get_nonexistent_user(self, client):
        """Test getting user that doesn't exist"""
        response = client.get("/users/99999")
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_get_all_users(self, client, db_session):
        """Test retrieving all users"""
        # Create multiple users
        users_data = [
            {"email": "user1@test.com", "username": "user1", "password": "pass1"},
            {"email": "user2@test.com", "username": "user2", "password": "pass2"},
        ]
        
        for user_data in users_data:
            client.post("/users/", json=user_data)
        
        response = client.get("/users/")
        
        assert response.status_code == 200
        assert len(response.json()) >= 2

class TestItemRoutes:
    """Test item API endpoints"""
    
    @pytest.fixture
    def authenticated_user(self, client, sample_user_data):
        """Create user and return auth token (if using JWT)"""
        # For simplicity, we'll just create user and return ID
        response = client.post("/users/", json=sample_user_data)
        return response.json()["id"]
    
    def test_create_item(self, client, authenticated_user, sample_item_data):
        """Test creating an item for a user"""
        response = client.post(
            f"/users/{authenticated_user}/items/",
            json=sample_item_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_item_data["name"]
        assert data["price"] == sample_item_data["price"]
        assert data["owner_id"] == authenticated_user
    
    def test_get_user_items(self, client, authenticated_user, sample_item_data):
        """Test getting all items for a user"""
        # Create an item
        client.post(f"/users/{authenticated_user}/items/", json=sample_item_data)
        
        # Get items
        response = client.get(f"/users/{authenticated_user}/items/")
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert items[0]["name"] == sample_item_data["name"]
    
    def test_delete_item(self, client, authenticated_user, sample_item_data):
        """Test deleting an item"""
        # Create item
        create_response = client.post(
            f"/users/{authenticated_user}/items/",
            json=sample_item_data
        )
        item_id = create_response.json()["id"]
        
        # Delete item
        delete_response = client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 204
        
        # Verify item is gone
        get_response = client.get(f"/users/{authenticated_user}/items/")
        assert len(get_response.json()) == 0
    
    def test_update_item(self, client, authenticated_user, sample_item_data):
        """Test updating an item"""
        # Create item
        create_response = client.post(
            f"/users/{authenticated_user}/items/",
            json=sample_item_data
        )
        item_id = create_response.json()["id"]
        
        # Update item
        update_data = {"name": "Updated Name", "price": 59.99}
        update_response = client.put(f"/items/{item_id}", json=update_data)
        
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Name"
        assert update_response.json()["price"] == 59.99