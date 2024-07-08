from .db_storage import DBStorage

storage = DBStorage()
session = storage.session()
