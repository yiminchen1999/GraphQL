from orator import DatabaseManager, Schema, Model
import pymysql
import time
import asyncio
import aiomysql

DATABASES = {
    "mysql": {
        "driver": "mysql",
        "host": "localhost",
        "database": "ShapeMentor",
        "user": "root",
        "password": "cym991019",
        "prefix": "",
        "port": 3306,
    }
}

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)
