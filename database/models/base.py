from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, registry, mapped_column
from sqlalchemy.sql.annotation import Annotated

int_pk = Annotated[
    int,
    mapped_column(Integer, primary_key=True)
]

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            int_pk: Integer,
        }
    )
