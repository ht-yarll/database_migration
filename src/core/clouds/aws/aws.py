from services.rds import RDSCLient
from services.s3 import S3Client
from services.sts import AWSCredentialsManager


class AWS:
    def __init__(self, config: dict):
        self.config = config
        
    def run_flow(self):
        try:
            rds = RDSCLient(self.config)
            s3 = S3Client(self.config)
            sts = AWSCredentialsManager(self.config)
            
            
        except Exception as e:
            print(f"An error occurred while initializing AWS services: {e}")
            raise e
