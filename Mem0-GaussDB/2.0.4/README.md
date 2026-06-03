# 使用 Mem0-GaussDB 实现 Agent 长期记忆

本文档介绍如何使用 Mem0-GaussDB 将 GaussDB 作为 mem0 的向量数据库后端，实现 Agent 记忆的写入、语义检索、元数据过滤和关键词检索。

Mem0-GaussDB 是 GaussDB 生态维护的 mem0 适配版本，在 mem0 基础上新增 GaussDB vector store provider。当前版本采用部门维护 fork 方式提供，不依赖官方 mem0 主仓合入。

## 前提条件

- **Python 版本**：Python >= 3.10
- **GaussDB 数据库**：已获取数据库连接信息，包括主机、端口、用户名、密码和数据库名
- **GaussDB 能力**：已开启向量库能力（`enable_vectordb`），支持 `FLOATVECTOR`、`JSONB`；集中式部署支持 BM25 能力时可使用 `keyword_search`
- **数据库编码**：数据库和客户端连接建议使用 `UTF8`，中文 `text_lemmatized` 和 BM25 场景要求 UTF8
- **数据库兼容模式**：当前适配面向 GaussDB O 兼容模式；目标实例需具备 `JSONB`、`FLOATVECTOR`、`UUID`、BM25、系统目录查询和 `psycopg2` 连接能力
- **Embedding 模型服务**：可用的 Embedding API，例如 OpenAI 或 SiliconFlow 等 OpenAI-compatible 服务
- **Python 驱动**：建议按 GaussDB 产品文档安装与目标数据库版本配套的 `psycopg2` 驱动

## 安装

当前示例使用 GaussDB 生态维护的 mem0 fork 安装：

```bash
pip install "git+https://github.com/HuaweiCloudDeveloper/mem0-GaussDB.git@v2.0.4-gaussdb"
pip install openai
```

请按 GaussDB 产品文档安装与目标数据库版本配套的 `psycopg2` 驱动。

## 快速入门

### 1. 使用 Memory API

```python
from mem0 import Memory

config = {
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "BAAI/bge-large-zh-v1.5",
            "api_key": "YOUR_API_KEY",
            "openai_base_url": "https://api.siliconflow.cn/v1",
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "deepseek-ai/DeepSeek-V3",
            "api_key": "YOUR_API_KEY",
            "openai_base_url": "https://api.siliconflow.cn/v1",
        },
    },
    "vector_store": {
        "provider": "gaussdb",
        "config": {
            "host": "127.0.0.1",
            "port": 19995,
            "user": "gaussdb_user",
            "password": "gaussdb_password",
            "database": "postgres",
            "collection_name": "mem0_memory",
            "embedding_model_dims": 1024,
            "deployment_mode": "centralized",
            "vector_index_type": "gsdiskann",
            "vector_metric": "cosine",
            "auto_create": True,
        },
    },
}

memory = Memory.from_config(config)

memory.add(
    "我喜欢喝咖啡，周末经常去爬山",
    user_id="user_001",
    infer=False,
)

results = memory.search(
    "咖啡",
    filters={"user_id": "user_001"},
)

print(results)
```

### 2. 直接使用 GaussDB Provider

```python
from mem0.vector_stores.gaussdb import GaussDB

db = GaussDB(
    host="127.0.0.1",
    port=19995,
    user="gaussdb_user",
    password="gaussdb_password",
    database="postgres",
    collection_name="mem0_provider_demo",
    embedding_model_dims=4,
    deployment_mode="centralized",
    vector_index_type="gsdiskann",
    vector_metric="cosine",
)

db.insert(
    vectors=[[1.0, 0.0, 0.0, 0.0]],
    payloads=[{
        "data": "I like coffee",
        "text_lemmatized": "I like coffee",
        "user_id": "user_001",
    }],
)

rows = db.search(
    query="coffee",
    vectors=[1.0, 0.0, 0.0, 0.0],
    top_k=5,
    filters={"user_id": "user_001"},
)

print(rows)
```

## 支持能力

| 能力 | 集中式 GaussDB | 分布式 GaussDB |
|------|----------------|----------------|
| `Memory.add` / `Memory.search` / `Memory.update` / `Memory.delete` | 支持 | 支持 |
| 向量检索 | 支持 | 支持 |
| metadata filter | 支持 | 支持 |
| BM25 `keyword_search` | 支持 | 不支持 |
| JSONB payload 存储 | 支持 | 支持 |

## 部署前检查

| 检查项 | 集中式 GaussDB | 分布式 GaussDB |
|--------|----------------|----------------|
| 向量维度 | `embedding_model_dims <= 4096` | `embedding_model_dims <= 1024` |
| 1024 维以上向量 | 支持，但必须使用 `vector_index_type="gsdiskann"` | 不支持；当前超过 1024 维的向量索引能力仅集中式支持 |
| 向量索引 | 支持 `gsdiskann` / `gsivfflat`；1024 维以上仅支持 `gsdiskann` | 支持 `gsdiskann` / `gsivfflat`，但为了使用向量索引，维度不得超过 1024 |
| BM25 `keyword_search` | 支持，要求 BM25 能力和可用 BM25 索引 | 不支持，provider 返回 `None` |
| payload 存储 | `JSONB` | `JSONB` |
| 数据库编码 | 建议/要求 `UTF8`，尤其是中文 `text_lemmatized` 和 BM25 场景 | 建议/要求 `UTF8`，尤其是中文 `text_lemmatized` 场景 |
| 兼容模式 | O 兼容模式 | O 兼容模式 |

当前实现面向 GaussDB O 兼容模式，会使用 GaussDB 的 `FLOATVECTOR`、`JSONB`、`UUID`、BM25 索引、系统目录查询和 `psycopg2` 连接协议。使用前需要确认目标实例已具备这些能力。

## 配置参数

### 连接参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `connection_string` | `None` | GaussDB DSN，优先级高于 host/port/user/password |
| `host` | `None` | 数据库地址 |
| `port` | `None` | 数据库端口 |
| `database` | `"postgres"` | 数据库名 |
| `user` | `None` | 用户名 |
| `password` | `None` | 密码 |
| `sslmode` | `None` | SSL 模式，例如 `require`、`prefer`、`disable` |
| `sslrootcert` | `None` | SSL 根证书路径 |
| `schema_name` | `"public"` | schema 名称 |

连接配置优先级：

```text
显式入参 > 环境变量 > 默认值
```

### Collection 和向量参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `collection_name` | `"mem0"` | collection 表名 |
| `auto_create` | `True` | 初始化时是否自动创建 collection 表 |
| `embedding_model_dims` | `1536` | embedding 向量维度 |
| `deployment_mode` | `"centralized"` | GaussDB 部署模式，支持 `centralized`、`distributed` |
| `vector_index_type` | `"gsdiskann"` | 向量索引类型，支持 `gsdiskann`、`gsivfflat` |
| `vector_metric` | `"cosine"` | 向量距离类型，支持 `cosine`、`l2` |
| `minconn` | `1` | 连接池最小连接数 |
| `maxconn` | `5` | 连接池最大连接数 |
| `insert_batch_size` | `2000` | 单批写入最大行数 |
| `vector_index_maintenance_work_mem` | `None` | 创建向量索引时临时设置的 `maintenance_work_mem`，例如 `"256MB"`、`"2GB"` |

维度限制：

```text
centralized: embedding_model_dims <= 4096
distributed: embedding_model_dims <= 1024
embedding_model_dims > 1024 时，仅集中式支持，且必须使用 vector_index_type="gsdiskann"
```

分布式限制在 1024 维及以下，是因为当前超过 1024 维的向量索引能力仅集中式支持。Mem0-GaussDB 默认需要创建向量索引用于检索性能，因此分布式部署需使用 1024 维及以下的 embedding 模型。

## Filter 约束

支持的 operator：

```text
eq, ne, gt, gte, lt, lte, in, nin, contains, icontains
$and / AND, $or / OR, $not / NOT, *
```

说明：

- `user_id`、`agent_id`、`run_id` 是 scope 冗余列，支持 `eq/ne/in/nin/contains/icontains`。
- scope 冗余列不支持 `gt/gte/lt/lte` range filter。
- 非 scope payload 字段支持 JSONB exact equality、字符串包含和 number / ISO-style datetime range filter。
- 不支持的 operator 会抛出 `ValueError`，不会静默降级。

## Keyword Search 约束

集中式 GaussDB 支持 BM25 `keyword_search`，分布式 GaussDB 不支持 BM25 `keyword_search`。

BM25 文本来源优先级：

```text
payload["text_lemmatized"]
payload["data"]
```

中文关键词检索依赖 `text_lemmatized` 的分词质量。对于中文词级查询，建议显式写入分词后的文本：

```python
{
    "data": "我喜欢喝咖啡",
    "text_lemmatized": "我 喜欢 喝 咖啡"
}
```

## 注意事项

- direct provider 自定义 `id` 必须是 UUID 字符串；不传 `ids` 时 provider 会自动生成 UUID。
- `insert()` 是 upsert 语义，同 `id` 再写会覆盖 vector、payload、`text_lemmatized` 和 scope 冗余列。
- `update(payload=...)` 是 full replacement，不是 merge。
- vector 和 payload / JSONB filter 不支持 `NaN`、`Infinity`、`-Infinity`。
- 数据库和连接建议/要求使用 UTF8，尤其是中文 `text_lemmatized` 和 BM25 场景。
- 目标库需要开启向量库能力（`enable_vectordb`）；否则 `FLOATVECTOR`、向量索引和向量检索相关能力不可用。
- 当前适配面向 GaussDB O 兼容模式；使用前需要确认目标库已具备 `JSONB`、`FLOATVECTOR`、BM25、系统目录和 `psycopg2` 连接能力。

## 更多信息

- mem0 项目地址：[https://github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)
- Mem0-GaussDB 适配源码：[https://github.com/HuaweiCloudDeveloper/mem0-GaussDB/tree/v2.0.4-gaussdb](https://github.com/HuaweiCloudDeveloper/mem0-GaussDB/tree/v2.0.4-gaussdb)
- GaussDB 驱动说明：[https://github.com/HuaweiCloudDeveloper/gaussdb-drivers](https://github.com/HuaweiCloudDeveloper/gaussdb-drivers)
