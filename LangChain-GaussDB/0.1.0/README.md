# 使用 langchain-gaussdb 实现 GaussDB 向量检索

本文档介绍如何使用 [langchain-gaussdb](https://github.com/HuaweiCloudDeveloper/langchain-gaussdb) 将 GaussDB 作为向量数据库集成到 LangChain 工作流中，实现文档的向量化存储与相似度检索。

## 前提条件

- **Python 版本**：Python ≥ 3.10
- **GaussDB 数据库**：已获取数据库连接信息（主机、端口、用户名、密码、数据库名）
- **Embedding 模型服务**：可用的 Embedding API（如 OpenAI、SiliconFlow 等）

## 安装

方式一：通过源码安装

```bash
git clone https://github.com/HuaweiCloudDeveloper/langchain-gaussdb.git
cd langchain-gaussdb
poetry install
```

方式二：通过 pip 安装

```bash
pip install langchain_gaussdb-0.1.0-py3-none-any.whl
```

## 快速入门

### 1. 初始化 Embedding 模型

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    api_key="xxx",
    base_url="https://api.siliconflow.cn/v1",
    dimensions=1024
)
```

### 2. 连接 GaussDB 向量存储

```python
from langchain_gaussdb import GaussVectorSettings, GaussVectorStore

config = GaussVectorSettings(
    host="192.xx.xx.xx",
    port=9800,
    user="langchain_gv",
    password="Gauss_234",
    database="postgres",
    table_name="my_docs"
)

vector_store = GaussVectorStore(
    embedding=embeddings,
    config=config
)
```

### 3. 插入文档

使用 `add_documents` 函数向向量存储中添加文档。注意：如果使用相同 ID 添加文档，将覆盖已有文档。

```python
from langchain_core.documents import Document

docs = [
    Document(
        page_content="there are fishes in the pond",
        metadata={"id": 1, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="ducks are also found in the pond",
        metadata={"id": 2, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="tigers are big and strong",
        metadata={"id": 3, "location": "zoo", "topic": "animals"},
    ),
    Document(
        page_content="fresh apples are available at the market",
        metadata={"id": 4, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the market also sells fresh oranges",
        metadata={"id": 5, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the new art exhibit is fascinating",
        metadata={"id": 6, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a sculpture exhibit is also at the museum",
        metadata={"id": 7, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a new coffee shop opened on Main Street",
        metadata={"id": 8, "location": "Main Street", "topic": "food"},
    ),
    Document(
        page_content="the book club meets at the library",
        metadata={"id": 9, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="the library hosts a weekly story time for kids",
        metadata={"id": 10, "location": "library", "topic": "reading"},
    ),
]

vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
```

### 4. 删除文档

```python
vector_store.delete(ids=["9"])
```

### 5. 相似度搜索

支持带元数据过滤的相似度搜索：

```python
results = vector_store.similarity_search(
    "ducks", k=10, filter={"location": "pond", "topic": "animals"}
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

带相似度分数的搜索：

```python
results = vector_store.similarity_search_with_score(query="tigers", k=1)
for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")
```

### 6. 作为 Retriever 使用

可以将向量存储转换为检索器，方便集成到 LangChain 管道中：

```python
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1})
results = retriever.invoke("kitty")
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

## 配置参数

### 连接设置

| 参数                  | 默认值                   | 说明                                                                  |
|-----------------------|-------------------------|-----------------------------------------------------------------------|
| `host`                | localhost               | 数据库服务器地址                                                       |
| `port`                | 5432                    | 数据库连接端口                                                         |
| `user`                | gaussdb                 | 数据库用户名                                                           |
| `password`            | -                       | 数据库密码                                                             |
| `database`            | postgres                | 数据库名称                                                             |
| `min_connections`     | 1                       | 连接池最小连接数                                                       |
| `max_connections`     | 5                       | 连接池最大连接数                                                       |
| `table_name`          | langchain_docs          | 存储向量数据和元数据的表名                                              |
| `index_type`          | IndexType.GSDISKANN     | 向量索引算法类型，可选 GsIVFFLAT 或 GsDiskANN，默认 GsDiskANN           |
| `index_params`        | DiskAnnParams()         | 向量索引参数，不同 index_type 需要配置不同的参数                         |
| `vector_type`         | VectorType.float_vector | 向量表示类型，可选 floatvector 或 boolvector，默认 floatvector           |
| `distance_strategy`   | DistanceStrategy.COSINE | 向量相似度度量策略，可选 l2、cosine、hamming，默认 cosine                |
| `embedding_dimension` | 1024                    | 向量嵌入维度                                                           |

### 支持的索引与距离策略组合

| 索引类型    | 维度上限 | 向量类型               | 支持的距离策略          |
|-------------|---------|------------------------|------------------------|
| GsIVFFLAT   | ≤1024   | floatvector/boolvector | l2/cosine/hamming      |
| GsDiskANN   | ≤4096   | floatvector            | l2/cosine              |

## API 参考

| 方法                           | 说明                           |
|--------------------------------|-------------------------------|
| `add_documents`                | 插入文档并自动生成向量嵌入       |
| `similarity_search`            | 基本向量相似度搜索              |
| `similarity_search_with_score` | 返回 (文档, 相似度分数) 元组    |
| `delete`                       | 按 ID 列表删除文档              |
| `get_by_ids`                   | 按 ID 列表获取文档              |
| `drop_table`                   | 删除整个表                      |
| `from_documents`               | 从文档列表初始化 GaussVectorStore |

## 更多信息

- 项目仓库：[langchain-gaussdb](https://github.com/HuaweiCloudDeveloper/langchain-gaussdb)
- 许可证：MIT
