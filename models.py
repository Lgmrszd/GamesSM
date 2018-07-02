import peewee as pw
from datetime import datetime
from db_connect import db


class BaseModel(pw.Model):
    class Meta:
        database = db


class Plugin(BaseModel):
    name = pw.CharField(max_length=50, primary_key=True)
    description = pw.CharField()
    enabled = pw.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broken = False


class SaveSlot(BaseModel):
    date = pw.DateTimeField(default=datetime.now)
    plugin = pw.ForeignKeyField(Plugin, backref="saves", null=True)
    data = pw.BlobField()
