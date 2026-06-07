from sqlalchemy import text

from app.core.db import SessionLocal
from app.models import (
    BrandProfile,
    ContentAsset,
    ContentTask,
    LLMCallLog,
    MediaAsset,
    Project,
    PublishJob,
    PublishResult,
    TopicCandidate,
)

# Delete child tables first to avoid FK ordering issues if the database
# ignores ON DELETE CASCADE for bulk operations or custom constraints exist.
MODELS_IN_DELETE_ORDER = [
    PublishResult,
    PublishJob,
    MediaAsset,
    ContentAsset,
    ContentTask,
    TopicCandidate,
    BrandProfile,
    Project,
    LLMCallLog,
]

SEQUENCES = [
    "projects_id_seq",
    "brand_profiles_id_seq",
    "topic_candidates_id_seq",
    "content_tasks_id_seq",
    "content_assets_id_seq",
    "media_assets_id_seq",
    "publish_jobs_id_seq",
    "publish_results_id_seq",
    "llm_call_logs_id_seq",
]


def clear_db() -> None:
    with SessionLocal() as db:
        for model in MODELS_IN_DELETE_ORDER:
            db.query(model).delete()

        for sequence_name in SEQUENCES:
            db.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"))

        db.commit()

    print("Database data cleared successfully.")


if __name__ == "__main__":
    clear_db()
