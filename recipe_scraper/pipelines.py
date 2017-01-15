from sqlalchemy.orm import sessionmaker
from models import Books, db_connect, create_books_table

class GoodReadslPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_books_table(engine)
        self.Session = sessionmaker(bind = engine)

    def process_item(self, item, spider):

        session = self.Session()
        book = Books(**item)

        try:
            session.add(book)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
