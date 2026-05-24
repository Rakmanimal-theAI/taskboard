import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, UserResponse, ItemCreate, ItemResponse

class TestUserSchemas:
    """Test Pydantic schemas for User"""
    
    def test_valid_user_create(self):
        """Test valid user creation schema"""
        user_data = {
            "email": "user@example.com",
            "username": "validuser",
            "password": "StrongP@ss123"
        }
        user = UserCreate(**user_data)
        
        assert user.email == "user@example.com"
        assert user.username == "validuser"
        assert user.password == "StrongP@ss123"
    
    def test_invalid_email_format(self):
        """Test invalid email raises validation error"""
        user_data = {
            "email": "notanemail",
            "username": "user",
            "password": "pass123"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        
        assert "value is not a valid email address" in str(exc_info.value)
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        user_data = {
            "email": "user@example.com"
            # missing username and password
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'username' for e in errors)
        assert any(e['loc'][0] == 'password' for e in errors)
    
    def test_username_min_length(self):
        """Test username minimum length"""
        user_data = {
            "email": "test@example.com",
            "username": "ab",  # assuming min length is 3
            "password": "pass123"
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_response_serialization(self, db_session):
        """Test UserResponse schema from ORM model"""
        from app.models import User
        
        user = User(
            id=1,
            email="test@example.com",
            username="testuser",
            created_at="2024-01-01T00:00:00"
        )
        
        response = UserResponse.model_validate(user)
        
        assert response.id == 1
        assert response.email == "test@example.com"
        assert response.username == "testuser"
        assert "password" not in response.model_dump()

class TestItemSchemas:
    """Test Pydantic schemas for Item"""
    
    def test_valid_item_create(self):
        """Test valid item creation schema"""
        item_data = {
            "name": "Test Product",
            "description": "A great product",
            "price": 49.99
        }
        item = ItemCreate(**item_data)
        
        assert item.name == "Test Product"
        assert item.price == 49.99
    
    def test_item_price_positive(self):
        """Test price must be positive"""
        item_data = {
            "name": "Product",
            "description": "Test",
            "price": -5.00
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(**item_data)
        
        assert "ensure this value is greater than 0" in str(exc_info.value)
    
    def test_item_name_required(self):
        """Test name is required"""
        item_data = {
            "description": "Test",
            "price": 10.00
        }
        
        with pytest.raises(ValidationError):
            ItemCreate(**item_data)