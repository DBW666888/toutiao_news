from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    Browse history ORM model.
    """
    __tablename__ = "history"
    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="user_news_history_unique"),
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
        Index("idx_view_time", "view_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="history id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="user id")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="news id")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="view time")

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
