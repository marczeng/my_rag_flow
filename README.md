## 1、项目简介

​	本项目旨在通过**智能体（Agent）**与**检索增强生成（Retrieval-Augmented Generation, RAG）**技术相结合的方式，构建一个高效、灵活的知识库问答系统。该系统能够自动识别并读取包括**docx**和**pdf**在内的多种文件格式，并对内容进行智能段落切分。为了适应不同类型的文档结构，我们实现了多种**段落切分算法**，确保信息提取的准确性和完整性。

​	项目的核心特色在于使用**向量数据库**来存储经过处理的文件内容，这种方式不仅提高了数据存储效率，同时也为后续的信息检索提供了强有力的支持。针对检索召回部分，我们设计了多种策略，以保证用户能够快速且精准地获取所需信息。

​	此外，系统支持为**Agent模式**的任务流插件提供**API**接口，允许开发者依据具体的应用场景进行定制化开发，从而极大地提升了系统的灵活性和扩展性。我们的最终目标是为用户提供一个无缝衔接、体验优秀的问答平台，使知识查询过程变得简单而直观。

​	此项目非常适合希望利用先进AI技术优化内部知识管理流程的企业或团队，以及任何对构建智能化问答系统感兴趣的开发者。欢迎有兴趣的朋友加入，共同探索知识管理和智能问答的新纪元。

## 2、核心特性

- **自动识别和读取文件**：支持docx、pdf等多种格式
- **多种段落切分算法**：适应不同文档结构的智能段落处理
- **向量数据库存储**：高效的数据存储与检索机制
- **多样化检索召回方式**：确保信息快速精准获取
- **Agent模式任务流API**：灵活的任务编排与扩展能力
- **优秀的问答体验**：提供无缝的知识查询服务

## 3、快速开始
**3.1 安装 Docker**
确保您的系统上已经安装了[Docker](https://docs.docker.com/get-docker/)。如果尚未安装，请根据官方文档进行安装。

**3.2 安装 Elasticsearch (ES)**

执行以下命令来拉取并运行Elasticsearch容器：

  ```bash
  # 拉取最新版本的Elasticsearch镜像
  docker pull docker.elastic.co/elasticsearch/elasticsearch:7.10.2
  
  # 运行Elasticsearch容器
  docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.2
  ```

  - `-d`：后台运行容器。
  - `--name elasticsearch`：为容器指定一个名称。
  - `-p 9200:9200 -p 9300:9300`：将容器的端口映射到主机的端口。
  - `-e "discovery.type=single-node"`：设置环境变量以允许单节点集群。

**3.3 安装MatrixOne**

  接下来，通过以下命令安装MatrixOne向量数据库：

  ```bash
  # 拉取MatrixOne的Docker镜像
  docker pull matrixorigin/matrixone:latest
  
  # 创建并运行MatrixOne容器
  docker run -d --name matrixone -p 6001:6001 matrixorigin/matrixone:latest
  ```

  - `-d`：后台运行容器。
  - `--name matrixone`：为容器指定一个名称。
  - `-p 6001:6001`：将容器的6001端口映射到主机的6001端口。

**3.4 验证安装**

  为了验证Elasticsearch和MatrixOne是否成功安装并运行，您可以分别访问以下URL：

  - Elasticsearch: 打开浏览器并访问 http://localhost:9200/，您应该能看到Elasticsearch的响应信息。

  - MatrixOne: 目前MatrixOne没有提供Web界面，默认情况下可以通过其API进行交互。您可以使用如curl等工具测试连接：

    ```bash
    curl http://localhost:6001/
    ```

​		如果返回了相关信息，则说明安装成功。

**3.5 后续配置**

​	根据您的具体需求，您可能需要对Elasticsearch和MatrixOne进行进一步的配置。请参考各自的官方文档获取更多信息：

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [MatrixOne Documentation](https://docs.matrixorigin.io/?spm=5176.28103460.0.0.40f7451ev7aqYj)

**3.6 配置环境**

```bash
pip install .
```

## 4、实验过程

### **4.1 数据集**

​	本[数据集](https://www.datafountain.cn/competitions/1045)源自CCF大数据与计算智能大赛（CCF BDCI），一项由中国计算机学会自2013年起举办的专注于大数据与人工智能领域的挑战赛事。此次数据集特别由联通数字科技有限公司提供支持，这是一家隶属于中国联通的专业子公司，致力于成为“可信赖的数字化转型专家”。通过整合云计算、大数据、物联网、人工智能等核心技术能力，联通数科为本次大赛提供了宝贵的数据资源。

​	该数据集围绕实际行业应用场景设计，旨在促进前沿技术与行业应用问题的解决，助力产业升级与社会高质量数据人才的培养。具体而言，数据集涵盖了多方面的电信业务场景，包括但不限于用户行为分析、网络优化、服务质量提升等领域，为参赛者提供了丰富的实践素材和挑战机会，以推动技术创新和实际应用解决方案的发展。

### **4.2 启动服务**

```bash
python src/app.py
```

[上传文件](request_addfile_example.py)

```python
import requests
import json
import os

# 服务地址
API_URL = "http://localhost:8001/api/v1/knowledge/generate"

"""
sessionId = request.sessionId,
input_files = request.input_files,
vec_db_category = request.vec_db_category,
file_type = request.file_type,
file_extension = request.file_extension,
embedding_model_name = request.embedding_model_name
"""

for tag in ["AF","AT","AW","AY","AZ"]:

    file_list = os.listdir("data/docx2/{}-folder".format(tag))

    for i,file in enumerate(file_list):
        file_path = os.path.join("data/docx2/{}-folder".format(tag),file)

        # 构造请求数据
        payload = {
            "sessionId": "user_{}".format(i),
            "input_files":file_path,
            "vec_db_category": "matrixone",
            "cache": True,
            "file_type": tag,
            "file_extension": "docx",
            "embedding_model_name": "bge"
        }

        # 发送 POST 请求
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        # 输出响应结果
        print("Status Code:", response.status_code)
        print("Response Body:", response.json())
```

### **4.3 评估结果**

```bash
# 生成中间缓存文件
python eval.py

# 计算最终分数结果
python quality_evaluate.py
```

#### **4.3.1 文件检索评估**

**📊 Recall@K（召回率@K）算法介绍**

**（1）概念简介**

在信息检索与推荐系统中，**Recall@K（召回率@K）** 是衡量系统在前 K 个返回结果中能覆盖多少相关项目的一个重要指标。

它结合了经典的“召回率”思想，并将其限制在前 K 个结果中进行评估，特别适用于推荐系统、搜索引擎等场景。

**（2）定义**

**🔹 召回率（Recall）**

召回率是衡量检索系统找到所有相关文档的能力，其定义为：

$$
{Recall} = \frac{检索到的相关文档数}{所有相关文档数}
$$

**🔹 Recall@K**

Recall@K 是召回率的一个变种，只考虑系统返回的前 K 个结果：

$$
{Recall@K} = \frac{前 K 个结果中相关文档的数量}{所有相关文档的数量}
$$

**（3）实验结果**

|          | k=1  | k=2  | k=3  |
| -------- | ---- | ---- | ---- |
| Recall@K | 0.84 | 0.89 | 0.94 |

#### **4.3.2 评测分数评估**

实验整体评测的分数是：0.7249255620283581，评测规则如下：

对于任意问题，采用如下公式评分： 

![公式](images/%E5%85%AC%E5%BC%8F.png)



## 5、后续工作

目前系统已初步实现基于文本内容的检索与问答能力，但仍在持续迭代优化中。为提升系统的全面性、准确性与实用性，未来将从以下几个方面进行功能拓展和技术升级：

### ✅ 当前待完善内容

- **表格数据检索能力尚未接入**：当前系统主要面向纯文本内容进行处理，暂未支持对表格结构化数据的有效检索。
- **PDF等复杂格式解析能力缺失**：系统尚不支持对 PDF 等非纯文本格式文件的智能解析与内容提取。

### 🚀 后续重点开发方向

#### （1）多模态内容处理能力增强

- 引入 **表格识别与结构化解析模块**，实现对表格字段、行列关系的理解与检索；
- 支持 **PDF 文件解析**，包括文字提取、图表识别、表格还原等功能，提升多源文档的兼容性与可用性。

#### （2）RAG（Retrieval-Augmented Generation）技术体系完善

未来将逐步引入以下关键技术模块，构建更强大、灵活的智能检索与生成体系：

| 模块                    | 功能说明                                                     |
| ----------------------- | ------------------------------------------------------------ |
| **多种 Embedding 模型** | 接入如 BERT、Sentence-BERT、ChatGLM-Embedding、Contriever 等不同模型，提升向量表示的多样性与语义匹配精度 |
| **多种召回机制**        | 实现混合召回策略，包括关键词召回、向量召回、图谱召回、协同过滤召回等，提升召回覆盖率和相关性 |
| **多种检索算法**        | 支持 BM25、ANN（Approximate Nearest Neighbor）、FAISS、Milvus、Hybrid Search 等主流检索算法 |
| **多种文本切分算法**    | 针对长文本内容，引入滑动窗口、语义边界分割、段落级切分等多种文本划分策略，提升上下文理解与检索效果 |

#### （3）可扩展架构设计

- 构建模块化、插件式的 RAG 技术框架，便于快速集成新模型、新算法；
- 支持动态配置 embedding 模型、召回策略、排序模型等关键组件，满足不同场景下的业务需求。

------

通过以上持续迭代与技术深化，平台将在未来具备更强的通用性和适应性，能够更好地服务于多样化的知识管理、智能问答、辅助决策等应用场景。
