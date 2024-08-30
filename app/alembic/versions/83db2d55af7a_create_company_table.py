"""create-company-table

Revision ID: 83db2d55af7a
Revises: 3b9066b27d0d
Create Date: 2024-08-30 08:51:58.129741

"""

import sqlalchemy as sa
from alembic import op
from schemas.base_entity import CompanyMode

# revision identifiers, used by Alembic.
revision = "83db2d55af7a"
down_revision = "3b9066b27d0d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("mode", sa.Enum(CompanyMode)),
        sa.Column("owner_id", sa.Uuid, nullable=False),
    )
    op.create_foreign_key(
        "fk_company_owner", "companies", "users", ["owner_id"], ["id"]
    )

    op.add_column("users", sa.Column("company_id", sa.UUID, nullable=True))
    op.create_foreign_key(
        "fk_staff_company", "users", "companies", ["company_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_column("users", "company_id")
    op.drop_table("companies")
    op.execute("DROP TYPE companymode;")
    
