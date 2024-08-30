"""create-company-table

Revision ID: 83db2d55af7a
Revises: 3b9066b27d0d
Create Date: 2024-08-30 08:51:58.129741

"""
from alembic import op
import sqlalchemy as sa

from schemas.base_entity import CompanyMode


# revision identifiers, used by Alembic.
revision = '83db2d55af7a'
down_revision = '3b9066b27d0d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode))
    )


def downgrade() -> None:
    pass
