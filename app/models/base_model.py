from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import session, Mapped, mapped_column

from core.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[datetime] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                              nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                               default=lambda: datetime.now(timezone.utc),
                                               onupdate=lambda: datetime.now(timezone.utc))

    def save(self, commit=True):
        self.before_save()
        session.add(self)
        if commit:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        self.after_save()

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        session.commit()
        self.after_update(*args, **kwargs)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
