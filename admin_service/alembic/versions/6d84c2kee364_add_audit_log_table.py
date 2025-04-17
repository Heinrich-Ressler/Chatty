"""add audit_log table

Revision ID:6d84c2kee364
Revises: 5b97b2cee267
Create Date: 2025-04-10 15:12:01.440415

"""
from alembic import op
import sqlalchemy as sa


# ID ревизии и предыдущей миграции
revision = '6d84c2kee364'
down_revision = '5b97b2cee267'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True)
    )


def downgrade():
    op.drop_table('audit_log')