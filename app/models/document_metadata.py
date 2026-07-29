from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentMetadata:
    file_name: str
    country: str
    s3_key: str
    local_path: str
    file_size: int
    last_modified: datetime