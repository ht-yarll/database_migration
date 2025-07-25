from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError


class AWSCredentialsManager:
    def __init__(self, config: dict):
        self.role_arn = config["migrations"]["cloud"]["aws"]["sts_role_arn"]
        self.region = config["aws"]["region"]
        self._cached_creds = None
        self._expiration = None

    def get_temp_credentials(self, session_name: str = "migration-session") -> dict:
        """Obtém credenciais temporárias via STS"""
        if self._creds_valid():
            return self._cached_creds

        sts = boto3.client('sts', region_name=self.region)
        response = sts.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=session_name,
            DurationSeconds=3600  # 1 hora
        )
        
        self._cached_creds = response['Credentials']
        self._expiration = response['Credentials']['Expiration']
        return self._cached_creds

    def _creds_valid(self) -> bool:
        """Verifica se as credenciais em cache ainda são válidas"""
        return (
            self._cached_creds and 
            self._expiration and 
            datetime.now(self._expiration.tzinfo) < self._expiration
        )
