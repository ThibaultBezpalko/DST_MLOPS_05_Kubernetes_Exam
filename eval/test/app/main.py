from sqlalchemy import create_engine, MetaData, text, Integer, String
from sqlalchemy.schema import Column, Table
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI
from pydantic import BaseModel
import os

print(f"\
========================================================================================\n\
Environment variables:\n\n\
{os.environ}\n\
========================================================================================\n\
")

app = FastAPI()

mysql_user = os.environ["MYSQL_USER"] # 'dstuser'
mysql_password = os.environ["MYSQL_PASSWORD"] # 'dstuser2025!_'
mysql_host = os.environ["MYSQL_HOST"] # 'k8s-exam-fastapi'
mysql_port = os.environ["K8S_EXAM_MYSQLDB_SERVICE_SERVICE_PORT"] # '3307'
mysql_database = os.environ["MYSQL_DATABASE"] # 'k8s-exam-db'

print(f"\
========================================================================================\n\
Database connection variables:\n\n\
mysql_user = {mysql_user}\n\
mysql_password = {mysql_password}\n\
mysql_host = {mysql_host}\n\
mysql_port = {mysql_port}\n\
mysql_database = {mysql_database}\n\
========================================================================================\n\
"
)

conn_string = f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"

mysql_engine = create_engine(conn_string)

metadata = MetaData()

class TableSchema(BaseModel):
    table_name: str
    columns: dict

@app.get("/tables")
async def get_tables():
    '''
    To list the created tables in MYSQL DB
    '''
    with mysql_engine.connect() as connection:
        results = connection.execute(text('SHOW TABLES;'))
        dict_res = {}
        dict_res['database'] = [str(result[0]) for result in results.fetchall()]
        return dict_res

@app.put("/table")
async def create_table(schema: TableSchema):
    '''
    To create a new database

    Example to use in IPADDRESS:30000/docs#/table route
    {
        "table_name": "user_data",
        "columns": {
            "id": "Integer"
        }
    }
    '''
    columns = [Column(col_name, eval(col_type)) for col_name, col_type in schema.columns.items()]
    table = Table(schema.table_name, metadata, *columns)
    try:
        metadata.create_all(mysql_engine, tables=[table], checkfirst=False)
        return f"{schema.table_name} successfully created"
    except SQLAlchemyError as e:
        return dict({"error_msg": str(e)})
