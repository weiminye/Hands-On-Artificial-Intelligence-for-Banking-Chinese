英文版原书代码网址在：https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Banking

此处的中文版代码主要修改了如下几处：

- 针对中文环境做了一些处理。
- 把一些需要付费才能使用的库和工具换成了免费的库和工具
- 为了降低学习门槛，把部分代码和数据做了部分汉化。本书作者是专家，但我的定位是科普工作者，所以降低学习门槛，让更多的人学习到这些技术是我的主要责任。如果你有其他方面的追求，可以直接看英文版原书代码网址：https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Banking

# 技术讲解视频

第7章例子2：技术讲解视频：[上市公司年报分析](https://www.bilibili.com/video/BV1vr4y1p7p5?spm_id_from=333.999.0.0) 。相关源代码：[第7章/例子2上市公司公告之年报/第7章第2个例子一气呵成版.py](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC7%E7%AB%A0/%E4%BE%8B%E5%AD%902%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A%E4%B9%8B%E5%B9%B4%E6%8A%A5/%E7%AC%AC7%E7%AB%A0%E7%AC%AC2%E4%B8%AA%E4%BE%8B%E5%AD%90%E4%B8%80%E6%B0%94%E5%91%B5%E6%88%90%E7%89%88.py) 。
第9章聊天机器人 - 例子2：技术讲解视频：[基于Neo4J知识图谱的聊天机器人](https://www.bilibili.com/video/BV13S4y1P7X2?spm_id_from=333.999.0.0) 。相关源代码：[第9章/聊天机器人/原书例子汉化版.py](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC9%E7%AB%A0/%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA/%E5%8E%9F%E4%B9%A6%E4%BE%8B%E5%AD%90%E6%B1%89%E5%8C%96%E7%89%88.py) 。

## 风险提示：

1. 其中的可解释信息目前业界尚在探索，目前尚没有理想的方案，所有人都在摸索，因此仅供参考。
2. 例子4、例子5因为涉及某具体上市公司，出于降低风险的考虑，现已删除。

# 注意事项

需要下载 https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.2.0/en_core_web_lg-3.2.0-py3-none-any.whl 到本地然后用如下命令安装

```
pip install en_core_web_lg-3.2.0-py3-none-any.whl
```

然后按照类似的方法安装**zh_core_web_sm**
```
pip install zh_core_web_sm-3.2.0-py3-none-any.whl
```

可以参考 https://blog.csdn.net/WZY31014332886/article/details/104605887/

# 做中文项目所需要用到的

## 如何寻找A股上市公司公告和年报

http://www.cninfo.com.cn/new/index

## 处理中文分词的工具和库

首先Spacy是支持中文的，如果用Spacy效果不理想，可以考虑LTP4: http://ltp.ai/ 和 https://ltp.readthedocs.io/zh_CN/latest/
