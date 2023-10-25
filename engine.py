from sqlalchemy import create_engine
import OrmDatabase as ORM

engine = create_engine('mysql://user:password@server', echo=True) # connect to server

from sqlalchemy.orm import Session

with Session(engine) as session:
    spongebob = ORM.User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[ORM.Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = ORM.User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            ORM.Address(email_address="sandy@sqlalchemy.org"),
            ORM.Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = ORM.User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()

from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(user)