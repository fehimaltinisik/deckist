from datetime import datetime

from sqlmodel import Field


class TimestampMixin:
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow})
    updated_at: datetime = Field(sa_column_kwargs={"onupdate": datetime.utcnow})
