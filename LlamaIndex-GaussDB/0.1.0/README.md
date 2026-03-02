# 使用 llama-index-vector-stores-gaussdb 实现 GaussDB 向量检索

本文档介绍如何使用 [llama-index-vector-stores-gaussdb](https://github.com/HuaweiCloudDeveloper/llama-index-vector-stores-gaussdb) 将 GaussDB 作为向量数据库集成到 LlamaIndex 工作流中，实现文档的向量化存储与语义检索。

## 前提条件

- **Python 版本**：Python ≥ 3.10
- **GaussDB 数据库**：已获取数据库连接信息（主机、端口、用户名、密码、数据库名）
- **OpenAI API Key**：或其他兼容的 LLM/Embedding 服务

## 安装

### 1. 安装 pygsvector SDK

```bash
pip install pygsvector-0.1.0-py3-none-any.whl
```

### 2. 安装 llama-index-vector-stores-gaussdb

方式一：通过源码安装

```bash
git clone https://github.com/HuaweiCloudDeveloper/llama-index-vector-stores-gaussdb.git
cd llama-index-vector-stores-gaussdb
poetry install
```

方式二：通过 pip 安装

```bash
pip install llama_index-0.1.0-py3-none-any.whl
```

## 快速入门

### 1. 配置 OpenAI

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

### 2. 准备文档

```bash
mkdir -p 'data/paul_graham/'
wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)
```

### 3. 初始化向量存储

```python
from pygsvector import GsVecClient
from llama_index.vector_stores.gaussdb import GaussVectorStore

client = GsVecClient(
    uri="10.25.106.116:6899",
    user="llamaindex_gv",
    password=" ",
    db_name="postgres",
)

vector_store = GaussVectorStore.from_params(
    client=client,
    dim=1024,  # embedding 维度
    table_name="llama_vector",
    vidx_config={
        "pq_nseg": 1,
        "pq_nclus": 16,
        "num_parallels": 10,
        "enable_pq": True,
    },
    drop_old=True,
)
```

### 4. 创建索引

```python
from llama_index.core import StorageContext, VectorStoreIndex

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context,
)
```

### 5. 查询索引

```python
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What did the author do?")

print(response.response)
print("来源节点:", [src.node.get_content()[:100] for src in response.source_nodes])
```

## 更多信息

- 项目仓库：[llama-index-vector-stores-gaussdb](https://github.com/HuaweiCloudDeveloper/llama-index-vector-stores-gaussdb)
- 许可证：MIT
