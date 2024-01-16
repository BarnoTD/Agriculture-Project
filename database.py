# database.py

from databases import Database
import sqlalchemy

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

farms = sqlalchemy.Table(
    "farms",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("location", sqlalchemy.String),
    sqlalchemy.Column("crops", sqlalchemy.String),
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("farm_id", None, sqlalchemy.ForeignKey("farms.id")),
)

# Create the tables
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(bind=engine)
