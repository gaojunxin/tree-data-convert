import logging
import os
import yaml
from menu_data_processor import MenuDataProcessor
from datetime import datetime


if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    excel_config = config['excel_config']
    db_config = config['database']

    # 创建一个日志记录器实例
    logger = logging.getLogger(__name__)
    # 根据需要设置日志级别
    logger.setLevel(logging.INFO)  
    # 创建一个控制台处理器
    ch = logging.StreamHandler()
    
    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 为处理器添加格式
    ch.setFormatter(formatter)
    
    # 为日志记录器添加处理器
    logger.addHandler(ch)

    menuDataProcessor = MenuDataProcessor(logger, excel_config, db_config)
    menuDataProcessor.load_data_from_excel(excel_config)
    logger.info(f'加载数据成功' )

    # 更新节点的父节点
    menuDataProcessor.update_parent(menuDataProcessor.tree, 7000, 8000)

    menuDataProcessor.save_data_to_db()

    table_name = excel_config['table_name']
    logger.info(f'所有数据已经保存到：【{table_name}】')

    # menuDataProcessor.load_data_from_db()
    # 打印树结构
    # print(menuDataProcessor.tree.show(stdout=False))

    
