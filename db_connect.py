import peewee as pw

db = pw.SqliteDatabase("data.db")
mem_db = pw.SqliteDatabase(":memory:")


class BaseModel(pw.Model):
    class Meta:
        database = db


class MemoryBaseModel(pw.Model):
    class Meta:
        database = mem_db