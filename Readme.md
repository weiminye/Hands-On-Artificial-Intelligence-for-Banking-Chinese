# Neo4j & DataFun GraphTalk 2022年4月8日讲座相关代码

- 例子1：技术讲解视频：[上市公司年报分析](https://www.bilibili.com/video/BV1vr4y1p7p5?spm_id_from=333.999.0.0) 。相关源代码：[第7章/例子2上市公司公告之年报/第7章第2个例子一气呵成版.py](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC7%E7%AB%A0/%E4%BE%8B%E5%AD%902%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A%E4%B9%8B%E5%B9%B4%E6%8A%A5/%E7%AC%AC7%E7%AB%A0%E7%AC%AC2%E4%B8%AA%E4%BE%8B%E5%AD%90%E4%B8%80%E6%B0%94%E5%91%B5%E6%88%90%E7%89%88.py) 。
- 例子2：技术讲解视频：[基于Neo4J知识图谱的聊天机器人](https://www.bilibili.com/video/BV13S4y1P7X2?spm_id_from=333.999.0.0) 。相关源代码：[第9章/聊天机器人/原书例子汉化版.py](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC9%E7%AB%A0/%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA/%E5%8E%9F%E4%B9%A6%E4%BE%8B%E5%AD%90%E6%B1%89%E5%8C%96%E7%89%88.py) 。
- 例子3：技术讲解视频：[基于Neo4J知识图谱的聊天机器人 - 支持同义词近义词](https://www.bilibili.com/video/BV1YZ4y1U7g6?spm_id_from=333.999.0.0) 。相关源代码：[第9章/聊天机器人/支持同义词和近义词.py](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC9%E7%AB%A0/%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA/%E6%94%AF%E6%8C%81%E5%90%8C%E4%B9%89%E8%AF%8D%E5%92%8C%E8%BF%91%E4%B9%89%E8%AF%8D.py) 。
- 例子4：技术讲解视频：[小数据推理 - 基于Neo4J知识图谱的上市公司公告实例](https://www.bilibili.com/video/BV1jY4y1i7Df?spm_id_from=333.999.0.0) 。相关源代码：[第9章/上市公司公告/某上市公司公告-小数据推理-1.ipynb](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC9%E7%AB%A0/%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A/%E6%9F%90%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A-%E5%B0%8F%E6%95%B0%E6%8D%AE%E6%8E%A8%E7%90%86-1.ipynb) 。
- 例子5：技术讲解视频：[小数据推理 - 基于Neo4J知识图谱的上市公司公告实例（2）](https://www.bilibili.com/video/BV1iZ4y1U737?spm_id_from=333.999.0.0) 。相关源代码：[第9章/上市公司公告/某上市公司公告-小数据推理-2.ipynb](https://github.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/blob/main/%E7%AC%AC9%E7%AB%A0/%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A/%E6%9F%90%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A-%E5%B0%8F%E6%95%B0%E6%8D%AE%E6%8E%A8%E7%90%86-2.ipynb) 。

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
