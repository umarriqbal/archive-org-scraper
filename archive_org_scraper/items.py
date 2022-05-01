
from dataclasses import dataclass


@dataclass
class ArchiveOrgScraperItem:
    title: str
    author: str
    published: str
    publisher: str
    tags: str
    download_url: str
