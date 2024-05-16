import json
from excel_reader import TreeDataExcelReader
import logging
import psycopg2
import yaml


# 创建一个日志记录器实例
logger = logging.getLogger(__name__)
# 根据需要设置日志级别
logger.setLevel(logging.DEBUG)  

# 导入数据到 MySQL 数据库
def importDataToMysqlDB():
    # 连接到 MySQL 服务器
    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="123456",
    #     database="xy-cloud"
    # )
    pass

# 导入数据到 Kingbase 数据库
def importDataToKingbaseDB(dbconfig, schema_name, table_name, menu_list):

    # 插入语句
    sql = f'''
    INSERT INTO "{schema_name}"."{table_name}" (id,parent_id,name,title,menu_type, delevel, ancestors,"path",frame_src,component,
    param_path,transition_name,ignore_route,is_cache,is_affix,is_disabled,frame_type,hide_tab,hide_menu,hide_breadcrumb,
    hide_children,hide_path_for_children,dynamic_level,real_path,perms,icon,sort,status,remark,create_by,create_time,
    update_by,update_time,is_common,is_default,del_flag,module_id,tenant_id) 
    VALUES
    (%(id)s,%(parent_id)s,%(name)s,%(title)s,%(menu_type)s,%(level)s,%(ancestors)s,%(path)s,NULL,%(component)s,NULL,NULL,'N','Y','N','N','0','0',%(hideMenu)s,'0','0','0',5,NULL,'',NULL,%(sort)s,'0',
    '',NULL,'2023-11-15 14:20:04',NULL,NULL,'1','Y',0,1,0);

    '''

    with psycopg2.connect(
        host=dbconfig['host'],
        port=dbconfig['port'],
        user=dbconfig['user'],
        password=dbconfig['password'],
        database=dbconfig['dbname'],
    ) as conn:
        with conn.cursor() as cursor:
            # 使用executemany()方法，传入SQL和字典列表
            logging.info(menu_list)
            try:
                cursor.executemany(sql, menu_list)
                conn.commit()
            except Exception as e:
                logging.error("执行executemany失败", exc_info=True)


if __name__ == '__main__':

    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    excel_config = config['excel_config']
    dbconfig = config['database']
  
    excelReader = TreeDataExcelReader(logger)

    # 读取excel文件
    excelReader.buildTreeDataFromExcel(excel_config)

    # 插入到数据库
    importDataToKingbaseDB(dbconfig, excel_config['schema_name'], excel_config['table_name'], excelReader.node_list)