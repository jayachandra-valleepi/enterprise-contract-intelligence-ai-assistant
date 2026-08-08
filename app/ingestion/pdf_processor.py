import pymupdf


class PDFProcessor:

    # --------------------------------------------------
    # EXTRACT TEXT FROM PDF
    # --------------------------------------------------

    def extract_text(self, pdf_path: str):

        document = pymupdf.open(pdf_path)

        pages = []

        for page_number, page in enumerate(
            document,
            start=1
        ):

            text = page.get_text("text")

            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

        document.close()

        return pages

    # --------------------------------------------------
    # CHECK WHETHER PDF HAS TEXT
    # --------------------------------------------------

    def has_text(self, pdf_path: str):

        document = pymupdf.open(pdf_path)

        total_text = ""

        for page in document:

            total_text += page.get_text("text")

        document.close()

        return len(total_text.strip()) > 50

    # --------------------------------------------------
    # GET PDF PAGE COUNT
    # --------------------------------------------------

    def get_page_count(self, pdf_path: str):

        document = pymupdf.open(pdf_path)

        page_count = len(document)

        document.close()

        return page_count