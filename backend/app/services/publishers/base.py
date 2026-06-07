from dataclasses import dataclass
from typing import Any


@dataclass
class PublishPayload:
    mode: str
    platform_post_id: str | None
    post_url: str | None
    raw_response_json: dict[str, Any]


class BasePublisher:
    mode: str

    def build_payload(self, asset) -> PublishPayload:
        raise NotImplementedError

