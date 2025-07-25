import subprocess


class CloudSQLService:
    def __init__(self, config: dict):
        self.config = config

    def export_mysql_gcp(self):
        """Exporta o banco para um file chamado 'backup.sql' usando mysqldump"""
        dump_file = "backup.sql"
        try:
            subprocess.run(
                f"mysqldump -h {self.config['cloud_sql']['instance_name']} -u {self.config['cloud_sql']['user']} -p{self.config['cloud_sql']['password']} "
                f"--single-transaction --routines --triggers {self.config['cloud_sql']['database_name']} > {dump_file}",
                shell=True,
                check=True
            )
            return dump_file
        
        except subprocess.CalledProcessError as e:
            print(f"Erro no dump: {e}")
            return None 