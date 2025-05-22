from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON, nullable=True)
    
    # Если нужна связь с пользователями
    # users = relationship("User", back_populates="role")
