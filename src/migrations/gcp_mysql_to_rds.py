from helpers.aws_helper import AWSHelper
from helpers.gcp_helper import GCPHelper

class MigrationPipeline:
    def __init__(self):
        self.aws_helper = AWSHelper()
        self.gcp_helper = GCPHelper()

    def migrate(self):
        dump_file = self.gcp_helper.export_mysql_gcp()
        if not dump_file:
            print("Erro ao exportar do GCP.")
            return

        # Upload to AWS S3
        self.aws_helper.upload_para_s3(dump_file)

        # Restore to AWS RDS
        self.aws_helper.restaurar_no_rds(dump_file)