"""add documents table with pgvector vector column #13

Revision ID: 63fa219bc771
Revises: 48e7d69d8668
Create Date: 2026‑08‑18

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision: str = '63fa219bc771'
down_revision: Union[str, Sequence[str], None] = '48e7d69d8668'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_name", sa.String(), nullable=False),
        sa.Column("file_type", sa.String(), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("total_chunks", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.UUID(), nullable=False),
        sa.Column("embedding", Vector(1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index('ix_document_document_chunk', 'documents', ['document_id', 'chunk_index'])
    op.create_index('ix_document_file_name', 'documents', ['file_name'])

    op.execute("""
CREATE INDEX ix_documents_embedding_hnsw 
ON documents USING hnsw (embedding vector_l2_ops);
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_documents_embedding_hnsw;")
    op.execute("DROP INDEX IF EXISTS ix_document_document_chunk;")
    op.execute("DROP INDEX IF EXISTS ix_document_file_name;")
    op.drop_table("documents")