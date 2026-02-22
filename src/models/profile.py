from sqlalchemy import Column, Integer, String, Boolean, Text
from .base import Base

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)
    profile_url = Column(String(255), nullable=False)
    search_criteria = Column(Text)
    active = Column(Boolean, default=True)

    job_posts = relationship("JobPost", back_populates="profile")
    scrape_logs = relationship("ScrapeLog", back_populates="profile")
