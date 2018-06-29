import peewee as pw
from db_connect import db


class BaseModel(pw.Model):
    class Meta:
        database = db


class Plugin(BaseModel):
    name = pw.CharField(max_length=50)
    description = pw.CharField()
    enabled = pw.BooleanField(default=False)