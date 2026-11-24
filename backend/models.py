
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel


def utc_now():
    return datetime.now(timezone.utc)


# ユーザー
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)

    public_id: str = Field(
        default_factory=lambda: uuid4().hex,
        unique=True,
        index=True,
    )

    display_name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=utc_now)


# 写真・PDFの記録
class Record(SQLModel, table=True):
    __tablename__ = "records"

    __table_args__ = (
        CheckConstraint(
            "file_type IN ('image', 'pdf')"
        ),
        CheckConstraint("page_count >= 1"),
        CheckConstraint(
            "file_type != 'image' OR page_count = 1"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    title: str
    file_type: str
    file_path: str
    original_filename: str
    page_count: int = Field(default=1)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# 位置指定型メモ
class Memo(SQLModel, table=True):
    __tablename__ = "memos"

    __table_args__ = (
        UniqueConstraint("record_id", "page_number", "slot"),
        CheckConstraint("slot IN (1, 2)"),
        CheckConstraint("page_number >= 1"),
        CheckConstraint("x_norm >= 0 AND x_norm <= 1"),
        CheckConstraint("y_norm >= 0 AND y_norm <= 1"),
    )

    id: int | None = Field(default=None, primary_key=True)
    record_id: int = Field(foreign_key="records.id", index=True)

    page_number: int = Field(default=1)
    slot: int

    x_norm: float
    y_norm: float

    title: str
    content: str = Field(default="")

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# メモの添付ファイル
class Attachment(SQLModel, table=True):
    __tablename__ = "attachments"

    id: int | None = Field(default=None, primary_key=True)
    memo_id: int = Field(foreign_key="memos.id", index=True)

    file_name: str
    file_path: str
    mime_type: str

    created_at: datetime = Field(default_factory=utc_now)


# 記録の共有情報
class RecordShare(SQLModel, table=True):
    __tablename__ = "record_shares"

    __table_args__ = (
        UniqueConstraint("record_id", "user_id"),
        CheckConstraint("permission IN ('view', 'edit')"),
    )

    id: int | None = Field(default=None, primary_key=True)

    record_id: int = Field(foreign_key="records.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    permission: str = Field(default="view")
    created_at: datetime = Field(default_factory=utc_now)
