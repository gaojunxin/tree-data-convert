# 父子分级树Excel导入工具

这个工具的目的是将excel中的分级结构转换为父子分级，然后导入数据库。

提供了命令使用方式和webui方式。

因为工作中这种场景比较多，所以想单独拿出来做一个比较通用的工具。

## 功能截图

![image.png](http://image.gaojunxin.cn/i/2024/04/25/662a28aeb7d9b.png)

## 开始

安装poetry
```
pip install poetry
```

安装依赖
```
poetry install 
```

运行后端服务

```
poetry run python app.py

```

运行前端
```
cd ui-vue

pnpm install

pnpm dev



```

导入菜单到人大进仓数据库
```
poetry run python main.py

# 代码中可以通过更新id号来实现插入任意节点
menuDataProcessor.update_parent(menuDataProcessor.tree, 7000, 8000)

```

## 目前进度

目前还在开发中，逐步完善。


## 联系我

我的博客：[www.gaojunxin.cn](https://www.gaojunxin.cn)

我的邮箱: gjx.xin@qq.com