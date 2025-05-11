from be_task_ca.database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from be_task_ca.user.model import User, CartItem
from be_task_ca.item.model import Item


def create_db_schema():
    Base.metadata.create_all(bind=engine)
