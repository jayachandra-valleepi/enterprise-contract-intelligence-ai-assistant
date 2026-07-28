from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:

    @staticmethod
    def extract_text(pdf_path):

        loader = PyPDFLoader(pdf_path)

        documents = loader.load()

        return documents