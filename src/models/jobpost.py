from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class JobPost(Base):
    __tablename__ = "job_posts"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    url = Column(String(255))
    posted_at = Column(DateTime)
    scraped_at = Column(DateTime)
    description = Column(Text)
    external_id = Column(String(255), unique=True)

    profile = relationship("Profile", back_populates="job_posts")
