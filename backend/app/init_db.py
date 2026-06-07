from app.core.db import Base, engine
from app.models import (
    BrandProfile,
    ContentAsset,
    ContentTask,
    LLMCallLog,
    Project,
    PublishJob,
    PublishResult,
    TopicCandidate,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
