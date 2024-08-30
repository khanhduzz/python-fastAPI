"""create-task-table

Revision ID: 3b9066b27d0d
Revises: 0d8d5c6a54af
Create Date: 2024-08-30 08:51:52.116012

"""

import sqlalchemy as sa
from alembic import op
from schemas.base_entity import TaskStatus

# revision identifiers, used by Alembic.
revision = "3b9066b27d0d"
down_revision = "0d8d5c6a54af"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("summary", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column(
            "status", sa.Enum(TaskStatus), nullable=False, default=TaskStatus.DRAFT
        ),
        sa.Column("priority", sa.SmallInteger, nullable=False, default=0),
        sa.Column("staff_id", sa.Uuid),
        sa.Column("owner_id", sa.Uuid, nullable=False),
    )
    op.create_foreign_key("fk_task_owner", "tasks", "users", ["owner_id"], ["id"])
    op.create_foreign_key("fk_task_staff", "tasks", "users", ["staff_id"], ["id"])


def downgrade() -> None:
    op.drop_table("tasks")
    op.execute("DROP TYPE taskstatus;")
