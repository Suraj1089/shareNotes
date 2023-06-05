from databases import Database
import sqlalchemy
import uuid



SQLALCHEMY_DATABASE_URL = "sqlite:///./auth.db"

database = Database(SQLALCHEMY_DATABASE_URL)


metadata = sqlalchemy.MetaData()

# Define your table(s)
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True,default=uuid.uuid4()), # using simple id
    sqlalchemy.Column("username", sqlalchemy.String(length=100)),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("expiry_date",sqlalchemy.DateTime),
    sqlalchemy.Column("api_key",sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
