"""
Base model module for Intelleva School Management System.
Provides common functionality for all models with encryption support.
"""
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from .. import db
from ..db_config import encrypt_data, decrypt_data
import json

class EncryptedMixin:
    """
    Mixin to provide encryption/decryption for sensitive model fields.
    """
    
    # List of fields to encrypt (should be overridden by child classes)
    _encrypted_fields = []
    
    # List of fields to store as encrypted JSON (should be overridden by child classes)
    _encrypted_json_fields = []
    
    @classmethod
    def register_encrypted_listeners(cls):
        """
        Register SQLAlchemy event listeners for encryption/decryption.
        """
        # Encrypt data before saving to database
        @event.listens_for(cls, 'before_insert')
        def encrypt_before_insert(mapper, connection, target):
            # Encrypt regular fields
            for field in target._encrypted_fields:
                if hasattr(target, field):
                    value = getattr(target, field)
                    if value is not None:
                        encrypted_value = encrypt_data(value)
                        setattr(target, field, encrypted_value)
            
            # Encrypt JSON fields
            for field in target._encrypted_json_fields:
                if hasattr(target, field):
                    value = getattr(target, field)
                    if value is not None:
                        # Convert to JSON string first, then encrypt
                        json_str = json.dumps(value)
                        encrypted_value = encrypt_data(json_str)
                        setattr(target, field, encrypted_value)
        
        # Encrypt data before updating database
        @event.listens_for(cls, 'before_update')
        def encrypt_before_update(mapper, connection, target):
            # Encrypt regular fields
            for field in target._encrypted_fields:
                if hasattr(target, field):
                    value = getattr(target, field)
                    if value is not None:
                        encrypted_value = encrypt_data(value)
                        setattr(target, field, encrypted_value)
            
            # Encrypt JSON fields
            for field in target._encrypted_json_fields:
                if hasattr(target, field):
                    value = getattr(target, field)
                    if value is not None:
                        # Convert to JSON string first, then encrypt
                        json_str = json.dumps(value)
                        encrypted_value = encrypt_data(json_str)
                        setattr(target, field, encrypted_value)
        
        # Decrypt data after loading from database
        @event.listens_for(cls, 'load')
        def decrypt_after_load(target, context):
            # Decrypt regular fields
            for field in target._encrypted_fields:
                if hasattr(target, field):
                    value = getattr(target, field)
                    if value is not None:
                        decrypted_value = decrypt_data(value)
                        setattr(target, field, decrypted_value)
            
            # Decrypt JSON fields
            for field in target._encrypted_json_fields:
                if hasattr(target, field):
                    value = getattr(target, field)
                    if value is not None:
                        try:
                            # Decrypt first, then parse JSON
                            decrypted_str = decrypt_data(value)
                            json_value = json.loads(decrypted_str)
                            setattr(target, field, json_value)
                        except (json.JSONDecodeError, Exception) as e:
                            # If decryption or JSON parsing fails, keep original value
                            print(f"Error decrypting JSON field {field}: {e}")

class JsonSerializableMixin:
    """
    Mixin to provide JSON serialization for models.
    """
    
    def to_dict(self, exclude=None):
        """
        Convert model to dictionary, excluding specified fields.
        
        Args:
            exclude: List of field names to exclude
            
        Returns:
            Dictionary representation of model
        """
        exclude = exclude or []
        result = {}
        
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                
                # Handle JSON fields
                if isinstance(value, dict) or isinstance(value, list):
                    result[column.name] = value
                else:
                    result[column.name] = value
                    
        return result
    
    def to_json(self, exclude=None):
        """
        Convert model to JSON string, excluding specified fields.
        
        Args:
            exclude: List of field names to exclude
            
        Returns:
            JSON string representation of model
        """
        return json.dumps(self.to_dict(exclude=exclude))

class BaseModel(db.Model, JsonSerializableMixin):
    """
    Abstract base model for all Intelleva models.
    """
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        """
        Generate table name automatically from class name.
        """
        return cls.__name__.lower()
