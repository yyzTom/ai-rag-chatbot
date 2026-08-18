import asyncio
import click
import uuid
from pathlib import Path
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models import Document
from llm_client import get_embedding

def load_txt(file_path: Path) -> str:
    """Load plain text file content"""
    return file_path.read_text(encoding="utf-8")

def load_pdf(file_path: Path) -> str:
    """Extract text from PDF file"""
    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)

def simple_chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Basic character-based text splitter"""
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - chunk_overlap)
    return chunks

async def process_files(file_path: Path, chunk_size: int, chunk_overlap: int):
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        full_text = load_txt(file_path)
    elif suffix == ".pdf":
        full_text = load_pdf(file_path)
    else:
        raise click.ClickException(f"Unsupported file type: {suffix}")
    
    click.echo(f"Loaded file: {file_path.name}, total length: {len(full_text)} chars")
    chunks = simple_chunk_text(full_text, chunk_size, chunk_overlap)
    click.echo(f"Generated {len(chunks)} chunks")
    
    file_stat = file_path.stat()
    file_size = file_stat.st_size
    file_type = suffix.removeprefix(".")
    total_chunks = len(chunks)
    document_id = uuid.uuid4()
    
    async with SessionLocal() as session:
        for idx, chunk_text in enumerate(chunks):
            click.echo(f"Processing chunk {idx+1}/{len(chunks)}")
            embedding_vec = await get_embedding(chunk_text)
            
            db_chunk = Document(
                content=chunk_text,
                file_name=file_path.name,
                file_type=file_type,
                file_size=file_size,
                total_chunks=total_chunks,  
                document_id=document_id,
                chunk_index=idx,
                embedding=embedding_vec,
            )
            session.add(db_chunk)
        await session.commit()
        
    click.echo(f"Saved all chunks to DB, document_id: {document_id}")
    
@click.command()
@click.option("--file", required=True, type=click.Path(exists=True), help="Path to .txt or .pdf file")
@click.option("--chunk_size", default=800, type=int, help="Max character per chunk")
@click.option("--chunk-overlap", default=150, type=int, help="Overlap between adjacent chunks")
def main(file, chunk_size, chunk_overlap):
    fp = Path(file)
    asyncio.run(process_files(fp, chunk_size, chunk_overlap))
    
if __name__ == "__main__":
    main()