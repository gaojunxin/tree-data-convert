from typing import Any
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql.base import PGDialect

class DBTools:
    def __init__(self, db_config) -> None:
        self.db_host = db_config['host']
        self.db_port = db_config['port']
        self.db_user = db_config['user']
        self.db_password = db_config['password']
        self.db_dbname = db_config['dbname']
        self.schema_name = db_config['schema_name']
        self.dict_name_map = {}
        self.dict_id_map = {}
        PGDialect._get_server_version_info = lambda *args: (4, 8, 5)
    def get_connection(self):
        return psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_dbname,
            options=f"-c search_path={self.schema_name}"
        )
    
    def create_engine(self) -> Any:
        conn_args = {
            "options": f"-c search_path={self.schema_name}"
        }
        engine = create_engine(f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_dbname}", connect_args=conn_args)
        return engine
    def get_schema_name(self):
        return self.schema_name

    def truncate_table(self, table_name):
        sql = f'TRUNCATE TABLE "{self.schema_name}"."{table_name}"'
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception as e:
                    self.logger.error(f"清空[{table_name}]数据失败", exc_info=True)