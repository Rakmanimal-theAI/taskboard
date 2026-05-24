import pytest
from app.models import User, Project
from sqlalchemy.exc import IntegrityError

class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, db_session):
        """Test creating a valid user"""
        user = User(
            email="john@example.com",
            name="john_doe",
            hashed_password="fakehashedpassword123"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "john@example.com"
        assert user.name == "john_doe"
        assert user.created_at is not None
    
    def test_user_email_unique_constraint(self, db_session):
        """Test that email must be unique"""
        user1 = User(email="same@example.com", name="user1", hashed_password="pass")
        user2 = User(email="same@example.com", name="user2", hashed_password="pass")
        
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_user_name_unique_constraint(self, db_session):
        """Test that username must be unique"""
        user1 = User(email="email1@test.com", name="sameuser", hashed_password="pass")
        user2 = User(email="email2@test.com", name="sameuser", hashed_password="pass")
        
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_user_relationships(self, db_session):
        """Test relationship with projects"""
        user = User(email="test@test.com", name="tester", hashed_password="pass")
        db_session.add(user)
        db_session.commit()
        
        project = Project(name="Laptop", description="Gaming laptop", price=1200.00, owner_id=user.id)
        db_session.add(item)
        db_session.commit()
        
        assert len(user.items) == 1
        assert user.items[0].name == "Laptop"

class TestItemModel:
    """Test Item model"""
    
    def test_create_item(self, db_session, sample_user_data):
        """Test creating an item for a user"""
        # Create user first
        user = User(
            email=sample_user_data["email"],
            name=sample_user_data["username"],
            hashed_password="hashedpass"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create item
        item = Item(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            owner_id=user.id
        )
        db_session.add(item)
        db_session.commit()
        
        assert item.id is not None
        assert item.name == "Smartphone"
        assert item.owner_id == user.id
    
    def test_item_price_validation(self, db_session):
        """Test price cannot be negative"""
        item = Item(name="Product", description="Test", price=-10.00, owner_id=1)
        db_session.add(item)
        
        with pytest.raises(Exception):  # Or specific validation error
            db_session.commit()
        db_session.rollback()
    
    def test_item_requires_owner(self, db_session):
        """Test item must have an owner"""
        item = Item(name="Orphan Item", description="No owner", price=100.00)
        db_session.add(item)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()