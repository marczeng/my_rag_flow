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
1. **安装 Docker**
  确保您的系统上已经安装了[Docker](https://docs.docker.com/get-docker/)。如果尚未安装，请根据官方文档进行安装。

2. **安装 Elasticsearch (ES)**

  1. 执行以下命令来拉取并运行Elasticsearch容器：

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

3. **安装MatrixOne**

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

4. **验证安装**

  为了验证Elasticsearch和MatrixOne是否成功安装并运行，您可以分别访问以下URL：

  - Elasticsearch: 打开浏览器并访问 http://localhost:9200/，您应该能看到Elasticsearch的响应信息。

  - MatrixOne: 目前MatrixOne没有提供Web界面，默认情况下可以通过其API进行交互。您可以使用如curl等工具测试连接：

    ```bash
    curl http://localhost:6001/
    ```

​		如果返回了相关信息，则说明安装成功。

​	5.**后续配置**

​	根据您的具体需求，您可能需要对Elasticsearch和MatrixOne进行进一步的配置。请参考各自的官方文档获取更多信息：

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [MatrixOne Documentation](https://docs.matrixorigin.io/?spm=5176.28103460.0.0.40f7451ev7aqYj)

