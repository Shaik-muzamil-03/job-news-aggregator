from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class ScrapeLog(Base):
    __tablename__ = "scrape_logs"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    status = Column(String(50))
    message = Column(Text)

    profile = relationship("Profile", back_populates="scrape_logs")
