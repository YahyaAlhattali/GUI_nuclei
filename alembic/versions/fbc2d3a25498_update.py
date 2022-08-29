"""update

Revision ID: fbc2d3a25498
Revises: 2ed20bde3865
Create Date: 2022-08-25 08:51:56.476304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc2d3a25498'
down_revision = '2ed20bde3865'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scan', sa.Column('name', sa.String(), nullable=True))
    op.create_index(op.f('ix_scan_name'), 'scan', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scan_name'), table_name='scan')
    op.drop_column('scan', 'name')
    # ### end Alembic commands ###