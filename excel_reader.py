#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

from openpyxl import load_workbook
import logging

# 定义 Excel数据表 描述信息
excel_config_definitions = {
    # 文件路径
    "excel_file_path": "demo.xlsx",
    # sheet名称
    "sheet_name": "菜单结构",
    # 名称所在行
    "name_row": 1,
    # 数据起始行
    "data_row": 2,
    # 名称起始列
    "name_start": 0,
    # 名称结束列
    "name_end": 6,
    # 生成的起始id
    "generate_start_id": 8000,
    # 扩展信息起始列
    "extension_start": 7,
    # 扩展信息结束列
    "extension_end": 10,
}

class TreeNode:  
    def __init__(self, id, title, level, parent_id, path ):  
        self.id = id
        self.title = title  
        self.level = level
        self.parent_id = parent_id
        self.path = path
        self.children = []
        
  
    def add_child(self, child):  
        self.children.append(child)  

    def __str__(self):  
        return f"TreeNode(id={self.id}, title={self.title}, level={self.level}, parent_id={self.parent_id})" 

logging.basicConfig(level=logging.INFO)

# 根据excel中数据构建树结构
def buildTreeDataFromExcel(excel_config_definitions):
    workbook = load_workbook(excel_config_definitions['excel_file_path'])
    sheet_name = "菜单结构"
    # 查看sheet页清单
    # workbook.sheet_names()
    # print("sheets：" + str(workBook.sheet_names()))
    sheet = workbook[sheet_name]

    node_list = []
    root_node_list = []

    # 每一级的父级分开存放，方便循环中存取，最大级数6
    parent_node_list = [None] * 6

    row_num = 0
    # 遍历sheet页中的行
    for row in sheet.iter_rows(min_row=excel_config_definitions['data_row'], values_only=True):
        level = 0
        name = ''
        node = TreeNode(None, None, None, None, None)
        for colNum in range(excel_config_definitions['name_start'], excel_config_definitions['name_end']):
            name = row[colNum]
            if name :
                node.id = excel_config_definitions['generate_start_id'] + row_num
                node.title = name
                node.level = level
                if level > 0:
                    parent_node = parent_node_list[level-1]
                    if parent_node:
                        parent_node.add_child(node)
                        node.parent_id = parent_node.id
                else:
                    root_node_list.append(node)
                    # print(node)
                parent_node_list[level] = node
                break
            else:
                level = level +1
        for colNum in range(excel_config_definitions['extension_start'], excel_config_definitions['extension_end']):
            name = row[colNum]
        if node.title:
            node_list.append(node)
            logging.info(node)
        row_num = row_num + 1
    

if __name__ == "__main__":
    buildTreeDataFromExcel(excel_config_definitions)