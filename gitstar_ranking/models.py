
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class GitHubRepo(Base):
    __tablename__ = 'github_repos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer)
    name = Column(String(255))
    stars = Column(Integer)
    description = Column(Text)
    language = Column(String(100))
    avatar_url = Column(String(500))
    repo_url = Column(String(500))
    image = Column(String(500))