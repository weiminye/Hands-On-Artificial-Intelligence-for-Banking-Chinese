# 注意事项

需要下载 https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.2.0/en_core_web_lg-3.2.0-py3-none-any.whl 到本地然后用如下命令安装

```
pip install en_core_web_lg-3.2.0-py3-none-any.whl
```

然后按照类似的方法安装**zh-core-web-trf**
```
pip install zh_core_web_trf-3.2.0-py3-none-any.whl
```

可以参考 https://blog.csdn.net/WZY31014332886/article/details/104605887/

# 做中文项目所需要用到的

## 如何寻找A股上市公司公告和年报

http://www.cninfo.com.cn/new/index

## 处理中文分词的工具和库

首先Spacy是支持中文的，如果用Spacy效果不理想，可以考虑LTP4: http://ltp.ai/ 和 https://ltp.readthedocs.io/zh_CN/latest/
