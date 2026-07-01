from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base
from app.models.technique import Technique

ioc_technique = Table(
    "ioc_techniques",
    Base.metadata,
    Column("ioc_id", String(64), ForeignKey("iocs.id"), primary_key=True),
    Column("technique_id", String(32), ForeignKey("techniques.id"), primary_key=True),
)


class IOCSource(Base):
    __tablename__ = "ioc_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ioc_id: Mapped[str] = mapped_column(String(64), ForeignKey("iocs.id"), index=True)
    source_name: Mapped[str] = mapped_column(String(64), index=True)
    external_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    raw: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class IOC(Base):
    __tablename__ = "iocs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    value: Mapped[str] = mapped_column(String(1024), unique=True, index=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    techniques: Mapped[list[Technique]] = relationship(secondary=ioc_technique)
