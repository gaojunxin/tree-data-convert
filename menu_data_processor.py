import logging
import os
import pandas as pd
import yaml
from db_tools import DBTools
from treelib import Tree
from datetime import datetime



class MenuDataProcessor:
    def __init__(self, logger, excel_config, db_config):
        # 创建一个树实例
        self.tree = Tree()
        # 根节点
        self.tree.create_node("Root", "0")  
        self.logger = logger
        self.dbtools = None
        if db_config is not None:
            self.dbtools = DBTools(db_config)
        if excel_config is not None:
            self.table_name = excel_config['table_name']
    # 函数用于从 DataFrame 中构建树形结构
    def build_tree_from_dataframe(self, df, tree, excel_config):
        parent_id_list = [0] * 10
        for index, row in df.iterrows():
            data = {}
            # 计算当前节点的层级
            level = 0
            tag = 'item'
            for colNum in range(excel_config['name_start'], excel_config['name_end']):
                if not pd.isnull(row.iloc[colNum]) :
                    tag = row.iloc[colNum]
                    break
                level = level +1
            
            col_mapping = excel_config['col_mapping']
            for colName, colNum in col_mapping.items():
                if colName:
                    value = row.iloc[colNum]
                    if pd.isnull(value):
                        value = ''
                    data[colName] = value

            if level > 0:
                tree.create_node(tag, row['id'], parent_id_list[level-1], data=data)
            else:
                tree.create_node(tag, row['id'], '0', data=data)
            
            parent_id_list[level] =  row['id']   

    # 函数用于从 DataFrame 中构建树形结构
    def build_tree_from_dataframe_db(self, df, tree):
        parents = {}
        for index, row in df.iterrows():
            parent_id = row['parent_id']
            if parent_id != '0' and not tree.contains(parent_id):
                parent_node = tree.create_node("Parent", parent_id, '0')
                parents[parent_id] = parent_node
            
            if row['id'] in parents:
                tree.update_node(row['id'], tag=row['title'], parent=parent_id, data=row)
                parents.pop(row['id'])
            else:
                tree.create_node(row['title'], row['id'], parent_id, data=row)
            
            
    # 函数用于更新节点的父节点
    def update_parent(self, tree, node_id, new_parent_id):
        node = tree[node_id]
        tree.update_node(node.identifier, identifier=new_parent_id)

    # 获取祖先ID字符串
    def get_ancestors_ids_as_string(self, tree, node_id):
        # 如果节点是根节点，直接返回其ID
        if tree[node_id].is_root():
            return tree[node_id].identifier
        
        # 否则，递归地获取父节点的祖先ID字符串，然后添加当前节点的ID
        parent_id = tree.parent(node_id).identifier
        ancestors_str = self.get_ancestors_ids_as_string(tree, parent_id)
        
        # 拼接当前节点ID，注意在中间添加逗号
        return f"{ancestors_str},{tree[node_id].identifier}"

    # 函数用于从树结构中提取扁平化数据
    def extract_flat_data(self, tree):
        flat_data = []
        
        # 遍历树中的每个节点
        for node_id in tree.nodes.keys():
            node = tree[node_id]
            if node.is_root():
                continue
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            item = {
                "id": node.identifier,
                "parent_id": tree.ancestor(node.identifier),
                "title": node.tag,
                "ancestors": self.get_ancestors_ids_as_string(tree, tree.parent(node_id).identifier),
                "delevel" : tree.level(node.identifier),
                "frame_src" : '0',
                "param_path" : None,
                "transition_name" : None,
                "ignore_route" : 'N',
                "is_cache" : 'N',
                "is_affix" : 'N',
                "is_disabled" : 'N',
                "frame_type" : "0",
                "hide_tab" : '0',
                "hide_breadcrumb" : '0',
                "hide_children" : '0',
                "hide_path_for_children" : '0',
                "dynamic_level" : 1,
                "real_path" : None,
                "icon" : None,
                "status" : "0",
                "remark" : None,
                "create_by" : 1,
                "create_time" : formatted_time,
                "update_by" : None,
                "update_time" : None,
                "is_common" : "0",
                "is_default" : "Y",
                "del_flag" : 0,
                "module_id" : 1,
                "tenant_id" : 0
            }
            # 添加其他节点信息
            item.update(node.data)
            try:
                item['hide_menu'] = int(item['hide_menu'])
            except ValueError:
                self.logger.error(f"id:{item['id']}, title:{item['title']}, hide_menu:{item['hide_menu']}不是一个数字")
                item['hide_menu'] = 0

            flat_data.append(item)
        
        return pd.DataFrame(flat_data)

    def load_data_from_excel(self, excel_config):
        file_path = excel_config['excel_file_path']
        # 读取 Excel 文件
        df = pd.read_excel(file_path, engine='openpyxl')
        generate_start_id = excel_config['generate_start_id']
        df['id'] = range(generate_start_id, generate_start_id + len(df))
        # 从 DataFrame 构建树形结构
        self.build_tree_from_dataframe(df, self.tree, excel_config)

    def load_data_from_db(self):
        query = f"SELECT * FROM {self.table_name}"
        engine = self.dbtools.create_engine()
        df = pd.read_sql_query(query, engine)
        # 从 DataFrame 构建树形结构
        self.build_tree_from_dataframe_db(df, self.tree)

    def save_data_to_excel(excel_config):
        pass


    def save_data_to_db(self):
        # 保存之前先备份
        self.backup_data()
        self.dbtools.truncate_table(self.table_name)
        # 调用函数提取扁平化数据
        flat_df = self.extract_flat_data(self.tree)
        flat_df['hide_menu'] = flat_df['menu_type'].eq('X').astype(int)
        engine = self.dbtools.create_engine()
        flat_df.to_sql(name=f'{self.table_name}', schema=self.dbtools.get_schema_name(), if_exists="append", con=engine, index=False)

    # 备份数据
    def backup_data(self):
        query = f"SELECT * FROM {self.table_name}"
        engine = self.dbtools.create_engine()
        df = pd.read_sql_query(query, engine)
        # 获取当前时间并格式化
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 备份目录
        backup_dir = 'backup'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        backup_filename = os.path.join(backup_dir, f'backup_{timestamp}.csv')
        df.to_csv(backup_filename, index=False)


