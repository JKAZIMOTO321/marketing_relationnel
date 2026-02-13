from database.database_manager import DatabaseManager

class RelationService:
    def __init__(self):
        self.db = DatabaseManager()

    def get_data_tableau(self):
        data = self.db.get_relations_ClientName()
        return data