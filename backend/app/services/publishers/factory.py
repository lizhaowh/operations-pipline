from fastapi import HTTPException, status

from app.services.publishers.base import BasePublisher
from app.services.publishers.manual_export import ManualExportPublisher
from app.services.publishers.playwright_assisted import PlaywrightAssistedPublisher


class PublisherFactory:
    _publishers: dict[str, type[BasePublisher]] = {
        ManualExportPublisher.mode: ManualExportPublisher,
        PlaywrightAssistedPublisher.mode: PlaywrightAssistedPublisher,
    }

    @classmethod
    def create(cls, mode: str) -> BasePublisher:
        publisher_cls = cls._publishers.get(mode)
        if publisher_cls is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"unsupported publish mode: {mode}",
            )
        return publisher_cls()
