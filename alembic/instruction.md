* Install alembic ``pip install alembic``
* Create alembic init file and folder: ``alembic init alembic``
* Generate a version: ``alembic revision --autogenerate -m "comment here"
`` => The alembic will create function to create table if it doesn't exist.
* The code that alembic automatically generate based on your modification in model files is not exactly correct, you need to check before apply it. 
=> Edit the function in the latest version .py file in versions folder then run the command above to generate new version.
* Then you need to run another command to let the alembic know which method in new version it need to execute and to apply the method: 
  * ``alembic upgrade head`` : 
  * ``alembic  upgrade +1/+2/+3...``:
  * ``alembic downgrade -1/-2...`` : 
