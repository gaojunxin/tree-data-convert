class TreeNode(dict):  
    """
        初始化一个树节点对象实例。

        参数:
        id: 节点的唯一标识符。
        title: 节点的标题。
        level: 节点在树中的层级。
        parent_id: 父节点的标识符。
        path: 节点在树中的路径。

        属性:
        children: 一个空列表，用于存储该节点的子节点。
    """
    def __init__(self, id, title, level, parent_id, path, name, menu_type, ancestors, component, hideMenu, sort, children=None):
        super().__init__()
        self['id'] = id
        self['title'] = title
        self['level'] = level
        self['parent_id'] = parent_id
        self['path'] = path
        self['name'] = name
        self['menu_type'] = menu_type
        self['ancestors'] = ancestors
        self['component'] = component
        self['hideMenu'] = hideMenu
        self['sort'] = sort
        self['children'] = children or []

    def add_child(self, child):  
        self['children'].append(child)  
        
    def __json__(self):
       return {
            "id": self['id'],
            "title": self['title'],
            "level": self['level'],
            "parentId": self['parent_id'],
            'path': self['path'],
            'name': self['name'],
            'menu_type': self['menu_type'],
            'ancestors': self['ancestors'],
            'component': self['component'],
            'hideMenu': self['hideMenu'],
            'sort': self['sort'],
            # 列表推导式，遍历子节点，递归调用__json__方法
            "children": [child.__json__() for child in self['children']]
        }
  