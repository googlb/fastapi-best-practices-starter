from sqlmodel import SQLModel

# Import all SQLModel models here to ensure Alembic can discover them
from app.domains.news.models import News
# from app.domains.order.models import Order

# You might not need to do anything else here.
# Alembic will typically look at SQLModel.metadata for all registered models.
# The act of importing them makes them registered.
