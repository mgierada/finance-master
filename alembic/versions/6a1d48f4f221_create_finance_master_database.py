"""create finance_master database

Revision ID: 6a1d48f4f221
Revises: 
Create Date: 2023-04-19 13:16:18.742012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6a1d48f4f221"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE DATABASE IF NOT EXISTS finance_master;")


def downgrade() -> None:
    op.execute("DROP DATABASE IF EXISTS finance_master;")
