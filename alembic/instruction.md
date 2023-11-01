* Install alembic ``pip install alembic``
* Create alembic init file and folder: ``alembic init alembic``
* Generate a version: ``alembic revision --autogenerate -m "comment here"
`` => The alembic will create table if it doesn't exist.
* Edit the function you want in the latest version .py file in versions folder then run the command above to generate new version and the alembic will automatically execute the operations.