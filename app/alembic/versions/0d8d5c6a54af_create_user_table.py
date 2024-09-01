"""create-user-table

Revision ID: 0d8d5c6a54af
Revises: 
Create Date: 2024-08-30 08:51:16.245601

"""
from datetime import datetime, timezone
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from schemas.base_entity import UserRole
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision = '0d8d5c6a54af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('email', sa.String),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('role', sa.Enum(UserRole), nullable=False, default=UserRole.USER),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "full_name": "James Bond",
            "email": "james@bond.com",
            "username": "james",
            "first_name": "james",
            "last_name": "bond",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "is_active": True,
            "role": UserRole.ADMIN,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])


def downgrade() -> None:
    op.drop_table("users")
    op.execute("DROP TYPE userrole;")
