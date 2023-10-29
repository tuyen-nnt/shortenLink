from sqlalchemy import Column, MetaData, Table, func, DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, TIMESTAMP
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.annotation import Annotated
from sqlalchemy.sql.coercions import cls
from database.models.base import Base

class TableNameMixin:
    @declared_attr.directive
    def __tablename__(selfcls) -> str:
        return cls.__name__.lower()

class TimestampMixin:
    create_at: Mapped[DATETIME] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    update_at: Mapped[DATETIME] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )

int_pk = Annotated[
    int,
    mapped_column(Integer, primary_key=True
    )
]

# user_fk = Annotated[
#     int, mapped_column(Integer, ForeignKey("myurl.", ondelete="SET NULL"))
# ]
class MyURL(Base, TableNameMixin, TimestampMixin):
    # __tablename__ = "myurl"
    id: Mapped[int_pk]
    real_url: Mapped[str] = mapped_column(String(80))
    hash_url: Mapped[str] = mapped_column(String(80))
    shorten_url: Mapped[str] = mapped_column(String(50))

    # def __repr__(self) -> str:
    #     return f"Shortlink(id={self.id!r}, real_url={self.real_url!r}, shorten_url={self.shorten_url!r})"

