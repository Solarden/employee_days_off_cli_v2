"""create employee & vacation

Revision ID: 654b76c8e53b
Revises:
Create Date: 2022-08-20 15:16:39.649991

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "654b76c8e53b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "employee",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=True),
        sa.Column("free_days", sa.Integer(), nullable=True),
        sa.Column("on_demand", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "employee_vacation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column("vacation_start", sa.DateTime(), nullable=True),
        sa.Column("vacation_end", sa.DateTime(), nullable=True),
        sa.Column("no_days", sa.Integer(), nullable=True),
        sa.Column("on_demand", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["employee_id"], ["employee.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("employee_vacation")
    op.drop_table("employee")
    # ### end Alembic commands ###