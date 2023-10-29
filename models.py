from sqlalchemy import Column, MetaData, Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

# https://docs.sqlalchemy.org/en/14/orm/quickstart.html#simple-select
class Shortlink(Base):
    __tablename__ = "myurl"

    id: Mapped[int] = mapped_column(primary_key=True)
    real_url: Mapped[str] = mapped_column(String(80))
    hash_url: Mapped[str] = mapped_column(String(80))
    shorten_url: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"Shortlink(id={self.id!r}, real_url={self.real_url!r}, shorten_url={self.shorten_url!r})"
