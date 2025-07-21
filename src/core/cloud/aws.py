import os
import subprocess

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_RDS_ENDPOINT = os.getenv("AWS_RDS_ENDPOINT")
AWS_RDS_USER = os.getenv("AWS_RDS_USER")
AWS_REGION = os.getenv("AWS_REGION")
AWS_RDS_PASSWORD = os.getenv("AWS_RDS_PASSWORD")

GCP_DB_NAME = os.getenv("GCP_DB_NAME")

class AWSHelper:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.rds_client = boto3.client('rds')

    def upload_for_s3(arquivo, bucket_name = AWS_S3_BUCKET):
        """Envia o backup para o Amazon S3."""
        print(f"Enviando {arquivo} para S3...")
        s3 = boto3.client('s3', region_name=AWS_REGION)
        try:
            s3.upload_file(arquivo, bucket_name, f"mysql-backups/{arquivo}")
            print(f"Backup enviado para s3://{bucket_name}/mysql-backups/{arquivo}")
        except NoCredentialsError:
            print("Credenciais AWS não encontradas!")

    def restore_on_rds(arquivo_sql):
        """Restaura o backup no RDS"""
        try:
            # Restaura dados
            subprocess.run(
                f"mysql -h {AWS_RDS_ENDPOINT} -u {AWS_RDS_USER} -p{AWS_RDS_PASSWORD} "
                f"{GCP_DB_NAME} < {arquivo_sql}",
                shell=True,
                check=True
            )
        except Exception as e:
            print(f"Erro na restauração: {e}")