from sqlalchemy import (
    create_engine,
    Boolean,
    String,
    Integer,
    DateTime,
    func,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime

engine = create_engine(
    url="postgresql+psycopg2://postgres:123zxc456vbn@localhost:5432/to-do list"
)

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String, nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullablle=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
