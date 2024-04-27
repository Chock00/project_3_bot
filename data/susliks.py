import sqlalchemy
from .db_session import SqlAlchemyBase


class Suslik(SqlAlchemyBase):
    __tablename__ = 'susliks'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    information = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    foto_bytes = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
