参考了https://github.com/wangle1218/KBQA-for-Diagnosis
## 基于知识图谱的医疗诊断知识问答系统
### 环境

- python    >= 3.6
- pyahocorasick==1.4.2
- requests==2.25.1
- gevent==1.4.0
- jieba==0.42.1
- six==1.15.0
- gensim==3.8.3
- matplotlib==3.1.3
- Flask==1.1.1
- numpy==1.16.0
- bert4keras==0.9.1
- tensorflow==1.14.0
- Keras==2.3.1
- py2neo==2020.1.1
- tqdm==4.42.1
- pandas==1.0.1
- termcolor==1.1.0
- itchat==1.3.10
- ahocorasick==0.9
- flask_compress==1.9.0
- flask_cors==3.0.10
- flask_json==0.3.4
- GPUtil==1.4.0
- pyzmq==22.0.3
- scikit_learn==0.24.1

### 运行方式
0. **下载意图识别模型文件**

链接：https://pan.baidu.com/s/1HYB3RwfDs_JcreuEYH51Tw 
提取码：b3cd 

**下载roberta预训练模型**
[从哈工大官方github下载，点这里](https://github.com/ymcui/Chinese-BERT-wwm#%E4%B8%AD%E6%96%87%E6%A8%A1%E5%9E%8B%E4%B8%8B%E8%BD%BD)，下载RBT3,Chinese 版本（貌似是这个，反正是一个三层的简单版）；[或者直接点这里用讯飞云下载](http://pan.iflytek.com/#/link/275E5B46185C982D4AF5AC295E1651B6)

下载好后解压放在项目路径下，然后在bert意图识别文件夹的 `app.py`代码里改一下预训练模型的路径。

**启动neo4j**

打开cmd ，进入安装目录，输入`neo4j.bat console`就行；如果是Linux系统，你可以输入`./neo4j start`后台启动
