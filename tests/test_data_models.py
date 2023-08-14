from moviweb_app.data_models.data_models import User, Movie, db
import pytest
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

# Make the engine
engine = create_engine("sqlite:////C:/Users/Home/PycharmProjects/moviweb_app_phase_5/moviweb_app/data/data.sqlite", future=True, echo=False)

# Create the tables in the database
db.create_all(engine)

def test_user_creation(session):

    user = User(
        name="shalom",
        user_id=1,
        username="shalom",
        password="123"
    )
    # assert session.user.name == "shalom"
    session.add(user)
    session.commit()

# Test it
with Session(bind=engine) as session:
    test_user_creation(session)

pytest.main()