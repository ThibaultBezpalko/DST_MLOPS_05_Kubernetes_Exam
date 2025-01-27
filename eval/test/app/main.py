from sqlalchemy import create_engine, MetaData, text, Integer, String
from sqlalchemy.schema import Column, Table
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI
from pydantic import BaseModel
import os

print(os.environ)

app = FastAPI()

mysql_user = os.environ["MYSQL_USER"]
mysql_password = os.environ["MYSQL_PASSWORD"]
mysql_host = os.environ["HOSTNAME"]
mysql_port = os.environ["K8S_EXAM_MYSQLDB_SERVICE_PORT_3307_TCP_PORT"]
mysql_database = os.environ["MYSQL_DATABASE"]

conn_string = f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"

mysql_engine = create_engine(conn_string)

metadata = MetaData()

class TableSchema(BaseModel):
    table_name: str
    columns: dict

@app.get("/tables")
async def get_tables():
    with mysql_engine.connect() as connection:
        print("hello")
        results = connection.execute(text('SHOW TABLES;'))
        dict_res = {}
        dict_res['database'] = [str(result[0]) for result in results.fetchall()]
        return dict_res

@app.put("/table")
async def create_table(schema: TableSchema):
    columns = [Column(col_name, eval(col_type)) for col_name, col_type in schema.columns.items()]
    table = Table(schema.table_name, metadata, *columns)
    try:
        metadata.create_all(mysql_engine, tables=[table], checkfirst=False)
        return f"{schema.table_name} successfully created"
    except SQLAlchemyError as e:
        return dict({"error_msg": str(e)})

'''
from sqlalchemy import Integer, String, DateTime, Float, Boolean
from sqlalchemy.types import Integer, String, DateTime

# Dictionary mapping SQL type strings to SQLAlchemy types
SQL_TYPE_MAP = {
    "INT": Integer,
    "VARCHAR": String,
    "TIMESTAMP": DateTime,
    "FLOAT": Float,
    "BOOLEAN": Boolean,
    # Add more mappings as needed
}

@app.put("/table")
async def create_table(schema: TableSchema):
    # Map the string types to SQLAlchemy types
    columns = [Column(col_name, SQL_TYPE_MAP.get(col_type.split('(')[0], String)(*map(int, col_type.split('(')[1].strip(')').split(','))) if '(' in col_type else SQL_TYPE_MAP.get(col_type, String)) 
               for col_name, col_type in schema.columns.items()]
    table = Table(schema.table_name, metadata, *columns)
    try:
        metadata.create_all(mysql_engine, tables=[table], checkfirst=False)
        return f"{schema.table_name} successfully created"
    except SQLAlchemyError as e:
        return {"error_msg": str(e)}    
'''


'''
{
  "table_name": "user_data",
  "columns": {
    "id": "Integer"
  }
}
'''