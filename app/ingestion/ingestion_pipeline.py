from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.s3_service import S3Service
from app.ingestion.pdf_processor import PDFProcessor
from app.ingestion.ocr_processor import OCRProcessor


class IngestionPipeline:

    def __init__(self):

        self.s3_service = S3Service()
        self.pdf_processor = PDFProcessor()
        self.ocr_processor = OCRProcessor()

    # --------------------------------------------------
    # PROCESS SINGLE PDF
    # --------------------------------------------------

    def process_pdf(
        self,
        s3_key: str,
        local_path: str
    ):

        documents = []

        # ----------------------------------------------
        # Get country from S3 path
        # Example:
        # France/Page_12.pdf
        # ----------------------------------------------

        country = s3_key.split("/")[0]

        # ----------------------------------------------
        # Check whether PDF contains text
        # ----------------------------------------------

        has_text = self.pdf_processor.has_text(
            local_path
        )

        # ----------------------------------------------
        # Normal PDF
        # ----------------------------------------------

        if has_text:

            print("  → Text PDF")

            pages = self.pdf_processor.extract_text(
                local_path
            )

        # ----------------------------------------------
        # Scanned PDF
        # ----------------------------------------------

        else:

            print("  → Scanned PDF - Using OCR")

            pages = self.ocr_processor.extract_text_from_pdf(
                local_path
            )

        # ----------------------------------------------
        # Convert pages to LangChain Documents
        # ----------------------------------------------

        file_name = Path(local_path).name

        for page in pages:

            text = page["text"]

            if not text.strip():
                continue

            document = Document(
                page_content=text,
                metadata={
                    "source": file_name,
                    "s3_key": s3_key,
                    "country": country,
                    "page_number": page["page_number"]
                }
            )

            documents.append(document)

        return documents

    # --------------------------------------------------
    # RUN INGESTION
    # --------------------------------------------------

    def run(
        self,
        prefix: str = "",
        local_folder: str = "data/raw"
    ):

        # ----------------------------------------------
        # Download PDFs from S3
        # ----------------------------------------------

        print("Starting S3 ingestion...")

        pdf_files = self.s3_service.download_all_pdfs(
            prefix=prefix,
            local_folder=local_folder
        )

        print(
            f"Total PDFs downloaded: {len(pdf_files)}"
        )

        # ----------------------------------------------
        # Process PDFs
        # ----------------------------------------------

        all_documents = []

        successful_files = 0
        failed_files = 0

        for pdf in pdf_files:

            s3_key = pdf["s3_key"]
            local_path = pdf["local_path"]

            print(
                f"\nProcessing: {s3_key}"
            )

            try:

                documents = self.process_pdf(
                    s3_key=s3_key,
                    local_path=local_path
                )

                all_documents.extend(
                    documents
                )

                print(
                    f"  → Documents created: "
                    f"{len(documents)}"
                )

                successful_files += 1

            except Exception as e:

                failed_files += 1

                print(
                    f"  ❌ Failed: {s3_key}"
                )

                print(
                    f"  Error: {e}"
                )

        # ----------------------------------------------
        # Final Summary
        # ----------------------------------------------

        print("\n" + "=" * 50)
        print("INGESTION SUMMARY")
        print("=" * 50)

        print(
            f"PDFs downloaded : {len(pdf_files)}"
        )

        print(
            f"Successful PDFs  : {successful_files}"
        )

        print(
            f"Failed PDFs      : {failed_files}"
        )

        print(
            f"Documents created: {len(all_documents)}"
        )

        print("=" * 50)

        return all_documents