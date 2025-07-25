import pathlib
import subprocess

import boto3
from botocore.exceptions import NoCredentialsError


class RDSCLient:
    def __init__(self, config: dict):
        self.rds_client = boto3.client('rds')
        self.config = config
        
    def export_and_restore_db(self):
        try:
            if not self.config['migrations']['tmp_dir']:
                raise ValueError("Temporary directory for migrations is not set in the configuration.")
            
            rds_endpoint = self.config['rds']['endpoint']
            rds_user = self.config['rds']['user']
            rds_password = self.config['rds']['password']
            db_name = self.config['rds']['db_name']
            local_file = pathlib.Path(self.config['migrations']['tmp_dir']) / 'db_dump.sql' 
            
            command = (
                f"mysql -h {rds_endpoint} -u {rds_user} -p{rds_password}"
                f"{db_name} < {local_file}"
            )
            
            process = subprocess.run(
                command,
                shell = True,
                check = True,
                capture_output=True
                )

            print("Successfully restored the database from the dump file.")
            print(f"Output: {process.stdout.decode()}")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while restoring the database: {e.stderr.decode()}")
            raise e
        
        except Exception as e:
            print(f"An error occurred while exporting and restoring the database: {e}")
            raise e