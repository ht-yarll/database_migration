import os
import hashlib
import subprocess
import mysql.connector

class BackUpValidator:
    def __init__(self, db:str):
        self.db = db

    def validate_sql(self):
        """Verifica se o arquivo SQL tem estrutura válida"""
        if not self.db.endswith('.sql'):
            raise ValueError("Arquivo não é um dump SQL válido.")
    
        if self.db.size == 0:
            raise ValueError("Arquivo SQL está vazio.")
        
        with open(self.db, 'r') as file:
            first_lines = [next(file) for _ in range(5)]

        if not any("CREATE TABLE" in line or "INSERT INTO" in line for line in first_lines):
            print("AVISO: Arquivo pode não conter dados válidos (não encontrou CREATE/INSERT)")

        return True
    
    def calculate_checksum(self, algorithm='sha256'):
        """Calcula o checksum do arquivo SQL"""
        hash_obj = hashlib.new(algorithm)
        with open(self.db, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    def mysql_sintaxe(self):
        """Verifica se o arquivo SQL é sintaticamente válido para MySQL"""
        try:
            subprocess.run(
                f"mysqlcheck --analyze --check --no-defaults -u root -p {self.db}",
                shell=True,
                check=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            return True

        except subprocess.CalledProcessError as e:
            print(f"Erros encontrados:\n{e.stderr.decode()}")
            return False
        
    def validate_compatibility_rds(self, mysql_version:str):
        """Verifica incompatibilidades com RDS"""
        with open(self.db, 'r') as f:
            content = f.read()

            problematic_patterns = [
            "DEFINER=`root`@`localhost`",
            "SET GLOBAL",
            "SUPER PRIVILEGE"
            ]

            issues = []
            for pattern in problematic_patterns:
                if pattern in content:
                    issues.append(f"Encontrado padrão problemático: {pattern}")

            if issues:
                print("AVISO: O arquivo SQL pode conter padrões incompatíveis com RDS:")
                for issue in issues:
                    print(f"- {issue}")
                return False
            return True
