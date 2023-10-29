import urllib.parse

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from database.models.myurl import MyURL

def create_engine_url(host, port, username, password, db_name):
    url = URL.create(
        drivername="mysql+pymysql",
        username=username,
        password=password,
        host=host,
        port=port,
        database=db_name,
    )
    print(url)

    # connect to server
    engine = create_engine(url, echo=True)
    return engine

def create_session_pool(engine):
    # create session pool
    session_pool = sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
