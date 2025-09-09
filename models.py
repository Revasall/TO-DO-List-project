from datetime import datetime

from sqlalchemy import (
    Boolean,
    String,
    Integer,
    DateTime,
    func,
    create_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import config

#---Create engine and session---
engine = create_engine(config.DATABASE_URL, echo=config.ECHO_SQL)
session = sessionmaker(engine)

# ---Base---
class Base(DeclarativeBase):
    # A common base for all models
    pass

# ---Model Task---
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
# --- Console view ---
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', done={self.done})>"

def models_main():
    Base.metadata.create_all(engine)
