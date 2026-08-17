"""
Document ingestion package for the Xerox Contract Intelligence RAG system

THe Ingestion pipeline

WS S3
    ↓
PDF download
    ↓
PDF extraction
    ↓
Text cleaning
    ↓
Metadata extraction
    ↓
Chunking
    ↓
PostgreSQL metadata
    ↓
Vector store in the next phase

"""