import magic
from fastapi import UploadFile

from utilities.extraction.base_extractor import BaseExtractor
from utilities.extraction.docx_extractor import DOCXExtractor
from utilities.extraction.image_extractor import ImageExtractor
from utilities.extraction.pdf_extractor import PDFExtractor
from utilities.extraction.raw_text_extractor import RawTextExtractor

_MIME_MAP: dict[str, type[BaseExtractor]] = {
    "application/pdf": PDFExtractor,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DOCXExtractor,
    "application/zip": DOCXExtractor,  # DOCX is a zip under the hood
    "image/png": ImageExtractor,
    "image/jpeg": ImageExtractor,
    "image/webp": ImageExtractor,
    "image/tiff": ImageExtractor,
    "text/plain": RawTextExtractor,
}


class ExtractorFactory:
    @staticmethod
    def create(content: bytes) -> BaseExtractor:
        mime = magic.from_buffer(content, mime=True)
        extractor_class = _MIME_MAP.get(mime, RawTextExtractor)
        return extractor_class()

    @staticmethod
    def create_from_upload(file: UploadFile) -> "ExtractorFactory":
        raise NotImplementedError("Read file bytes first, then use ExtractorFactory.create(bytes)")
