from sqlalchemy.orm import sessionmaker
from models import Recipe, db_connect, create_recipes_table

class AllRecipesPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_recipes_table(engine)
        self.Session = sessionmaker(bind = engine)

    def process_item(self, item, spider):

        session = self.Session()
        recipe = Recipe(**item)

        try:
            session.add(recipe)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
