from fastapi import UploadFile

from utilities.extraction.base_extractor import BaseExtractor
from utilities.extraction.docx_extractor import DOCXExtractor
from utilities.extraction.image_extractor import ImageExtractor
from utilities.extraction.pdf_extractor import PDFExtractor
from utilities.extraction.raw_text_extractor import RawTextExtractor

_CONTENT_TYPE_MAP: dict[str, type[BaseExtractor]] = {
    "application/pdf": PDFExtractor,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DOCXExtractor,
    "image/png": ImageExtractor,
    "image/jpeg": ImageExtractor,
    "image/jpg": ImageExtractor,
    "image/webp": ImageExtractor,
    "image/tiff": ImageExtractor,
    "text/plain": RawTextExtractor,
}


class ExtractorFactory:
    @staticmethod
    def create(file: UploadFile) -> BaseExtractor:
        content_type = file.content_type or ""
        extractor_class = _CONTENT_TYPE_MAP.get(content_type, RawTextExtractor)
        return extractor_class()
