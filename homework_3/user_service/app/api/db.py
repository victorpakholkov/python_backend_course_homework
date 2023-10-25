import os
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
from databases import Database


DATABASE_URI = os.getenv('DATABASE_URI')


engine = create_engine(DATABASE_URI)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('user_id', String(50)),
    Column('rights', ARRAY(String)),
    Column('items', ARRAY(String)),
    Column('files_id', ARRAY(String))
)


database = Database(DATABASE_URI)
