from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
from sqlmodel.orm.session import SelectOfScalar

load_dotenv()
SelectOfScalar.inherit_cache = True


def PG_Engine():
    postgresql_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('TEAM_UP_DB')}"
    # Remove echo on production
    engine = create_engine(postgresql_url, echo=False)
    SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)
    return engine


pg_engine = PG_Engine()


def get_session(engine):
    with Session(engine) as session:
        yield session


# Dependency
async def get_db(engine):
    db = get_session(engine)
    try:
        yield db
    finally:
        db.close()


# Create the database tables if they don't exist on startup
def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


# Disconnect from the database on shutdown
def disconnect_db(engine):
    engine.dispose()
