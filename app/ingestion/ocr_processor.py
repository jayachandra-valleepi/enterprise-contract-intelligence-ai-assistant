import fitz
import pytesseract

from PIL import Image
from io import BytesIO


class OCRProcessor:

    # --------------------------------------------------
    # OCR SINGLE PAGE
    # --------------------------------------------------

    def extract_text_from_page(
        self,
        page
    ):

        # Convert PDF page to image
        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image_bytes = pix.tobytes("png")

        image = Image.open(
            BytesIO(image_bytes)
        )

        text = pytesseract.image_to_string(
            image
        )

        return text.strip()

    # --------------------------------------------------
    # OCR ENTIRE PDF
    # --------------------------------------------------

    def extract_text_from_pdf(
        self,
        pdf_path: str
    ):

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(
            document,
            start=1
        ):

            text = self.extract_text_from_page(
                page
            )

            pages.append({
                "page_number": page_number,
                "text": text
            })

        document.close()

        return pages