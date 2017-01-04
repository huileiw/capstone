from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table

class LivingSocialPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind = engine)

    def process_item(self, item, spider):

        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
