# app/db/init_db.py
from app.db.base_class import Base
from app.db.session import engine

def init_db(create_tables: bool = True):
    """
    Idempotent: will create all tables defined by SQLAlchemy models.
    Keep this function small and safe for dev use.
    """
    if create_tables:
        Base.metadata.create_all(bind=engine)