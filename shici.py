import peewee
import sys

class Database(object):
    def __init__(self,kw):
        self.config = kw
        self.load_database();
        self.Model = self.get_model_class()

    def load_database(self):
        try:
            self.db = self.config.pop('db')
            self.engine = self.config.pop('engine')
        except KeyError:
            raise Exception('Please specify a "db" and "engine" for your database')

        try:
            self.database_class = load_class(self.engine)
            assert issubclass(self.database_class, peewee.Database)
        except ImportError:
            raise Exception('Unable to import: "%s"' % self.engine)
        except AttributeError:
            raise Exception('Database engine not found: "%s"' % self.engine)
        except AssertionError:
            raise Exception('Database engine not a subclass of peewee.Database: "%s"' % self.engine)
        self.database = self.database_class(self.db, **self.config)

    def get_model_class(self):
        class BaseModel(peewee.Model):
            class Meta:
                database = self.database
        return BaseModel

    def connect(self):
        self.database.connect()

    def close(self):
        self.database.close()

def load_class(s):
    path, klass = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, klass)