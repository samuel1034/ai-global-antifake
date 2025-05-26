from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql://user:password@host:port/database"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
