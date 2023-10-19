import os
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine)
from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

files = Table(
    'files',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('extention', String(10)),
    Column('size', Integer),
)

database = Database(DATABASE_URI)
