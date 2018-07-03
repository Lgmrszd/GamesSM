import peewee as pw
from datetime import datetime
from db_connect import db, BaseModel




# class SaveSlot(BaseModel):
#     date = pw.DateTimeField(default=datetime.now)
#     plugin = pw.ForeignKeyField(Plugin, backref="saves", null=True)
#     data = pw.BlobField()
