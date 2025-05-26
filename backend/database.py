from sqlmodel import create_engine, SQLModel, Session
import os

DATABASE_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{
    os.environ.get('POSTGRES_PASSWORD')}@localhost:5432/AIGlobalAntifake_db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
