from services.cloud_sql import CloudSQLService


class GCPHelper:
    def __init__(self, config: dict):
        self.config = config
    
    def fetch_backup_on_gcp_db(self):
        try:
            cloud_sql= CloudSQLService(self.config)
            cloud_sql.export_mysql_gcp()

        except Exception as e:
            print(f"An error occurred while initializing GCP services: {e}")
            raise e
