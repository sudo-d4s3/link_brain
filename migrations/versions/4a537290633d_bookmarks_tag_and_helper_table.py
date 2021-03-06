"""bookmarks, tag, and helper table

Revision ID: 4a537290633d
Revises: 
Create Date: 2020-12-19 14:12:48.381640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a537290633d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookmarks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=16), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookmarks_link'), 'bookmarks', ['link'], unique=True)
    op.create_index(op.f('ix_bookmarks_title'), 'bookmarks', ['title'], unique=True)
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('boodmark_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['boodmark_id'], ['bookmarks.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'boodmark_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('tag')
    op.drop_index(op.f('ix_bookmarks_title'), table_name='bookmarks')
    op.drop_index(op.f('ix_bookmarks_link'), table_name='bookmarks')
    op.drop_table('bookmarks')
    # ### end Alembic commands ###
