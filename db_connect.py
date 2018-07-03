import peewee as pw

db = pw.SqliteDatabase("data.db")


class BaseModel(pw.Model):
    class Meta:
        database = db
