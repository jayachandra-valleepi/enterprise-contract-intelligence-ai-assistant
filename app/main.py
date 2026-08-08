from app.ingestion.ingestion_pipeline import IngestionPipeline


pipeline = IngestionPipeline()

documents = pipeline.run(
    prefix="",
    local_folder="data/raw"
)

print(
    f"\nFinal Documents: {len(documents)}"
)