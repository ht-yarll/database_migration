import os
import subprocess

from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

GCP_SQL_INSTANCE = os.getenv("GCP_SQL_INSTANCE")
GCP_DB_USER = os.getenv("GCP_DB_USER")
GCP_DB_PASSWORD = os.getenv("GCP_DB_PASSWORD")
GCP_DB_NAME = os.getenv("GCP_DB_NAME")

class GCPHelper:
    def __init__(self):
        self.client = storage.Client()

    def export_mysql_gcp():
        """Exporta o banco para um file chamado 'backup.sql' usando mysqldump"""
        dump_file = "backup.sql"
        try:
            subprocess.run(
                f"mysqldump -h {GCP_SQL_INSTANCE} -u {GCP_DB_USER} -p{GCP_DB_PASSWORD} "
                f"--single-transaction --routines --triggers {GCP_DB_NAME} > {dump_file}",
                shell=True,
                check=True
            )
            return dump_file
        
        except subprocess.CalledProcessError as e:
            print(f"Erro no dump: {e}")
            return None 