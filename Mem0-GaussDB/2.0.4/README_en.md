# Using Mem0-GaussDB for Agent Long-Term Memory

This guide describes how to use Mem0-GaussDB with GaussDB as the vector database backend for mem0, enabling memory insertion, semantic search, metadata filtering, and keyword search for AI agents.

Mem0-GaussDB is a GaussDB-maintained mem0 adaptation. It adds a GaussDB vector store provider on top of mem0. This version is distributed as a maintained fork and does not depend on being merged into the upstream mem0 repository.

## Prerequisites

- **Python Version**: Python >= 3.10
- **GaussDB Database**: Connection details are available, including host, port, username, password, and database name
- **GaussDB Capabilities**: Vector database capabilities are enabled (`enable_vectordb`), and `FLOATVECTOR` and `JSONB` are available; centralized deployments can use `keyword_search` when BM25 is available
- **Database Encoding**: Use `UTF8` for the database and client connection, especially for Chinese `text_lemmatized` and BM25 use cases
- **Database Compatibility Mode**: This integration targets GaussDB O-compatible mode. The target instance must provide `JSONB`, `FLOATVECTOR`, `UUID`, BM25, system catalog queries, and `psycopg2` connectivity.
- **Embedding Model Service**: An available embedding API, such as OpenAI or an OpenAI-compatible service like SiliconFlow
- **Python Driver**: Install the `psycopg2` driver that matches the target GaussDB version as described in the GaussDB product documentation

## Installation

Install the GaussDB-maintained mem0 fork:

```bash
pip install "git+https://github.com/HuaweiCloudDeveloper/mem0-GaussDB.git@v2.0.4-gaussdb"
pip install openai
```

Install the `psycopg2` driver that matches the target GaussDB version according to the GaussDB product documentation.

## Quick Start

### 1. Use the Memory API

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
    "I like coffee and usually go hiking on weekends.",
    user_id="user_001",
    infer=False,
)

results = memory.search(
    "coffee",
    filters={"user_id": "user_001"},
)

print(results)
```

### 2. Use the GaussDB Provider Directly

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

## Supported Capabilities

| Capability | Centralized GaussDB | Distributed GaussDB |
|------------|---------------------|---------------------|
| `Memory.add` / `Memory.search` / `Memory.update` / `Memory.delete` | Supported | Supported |
| Vector search | Supported | Supported |
| Metadata filter | Supported | Supported |
| BM25 `keyword_search` | Supported | Not supported |
| JSONB payload storage | Supported | Supported |

## Deployment Checklist

| Check Item | Centralized GaussDB | Distributed GaussDB |
|------------|---------------------|---------------------|
| Vector dimension | `embedding_model_dims <= 4096` | `embedding_model_dims <= 1024` |
| Vectors above 1024 dimensions | Supported, but `vector_index_type="gsdiskann"` is required | Not supported; vector index capability above 1024 dimensions is currently available only on centralized GaussDB |
| Vector index | Supports `gsdiskann` / `gsivfflat`; dimensions above 1024 require `gsdiskann` | Supports `gsdiskann` / `gsivfflat`, but dimensions must not exceed 1024 in order to use vector indexes |
| BM25 `keyword_search` | Supported when BM25 capabilities and a usable BM25 index are available | Not supported; the provider returns `None` |
| Payload storage | `JSONB` | `JSONB` |
| Database encoding | `UTF8` is recommended/required, especially for Chinese `text_lemmatized` and BM25 use cases | `UTF8` is recommended/required, especially for Chinese `text_lemmatized` use cases |
| Compatibility mode | O-compatible mode | O-compatible mode |

The implementation targets GaussDB O-compatible mode and uses GaussDB `FLOATVECTOR`, `JSONB`, `UUID`, BM25 indexes, system catalog queries, and the `psycopg2` protocol. Confirm that the target instance provides these capabilities before deployment.

## Configuration

### Connection Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `connection_string` | `None` | GaussDB DSN. Takes precedence over host/port/user/password |
| `host` | `None` | Database host |
| `port` | `None` | Database port |
| `database` | `"postgres"` | Database name |
| `user` | `None` | Database username |
| `password` | `None` | Database password |
| `sslmode` | `None` | SSL mode, such as `require`, `prefer`, or `disable` |
| `sslrootcert` | `None` | SSL root certificate path |
| `schema_name` | `"public"` | Schema name |

Connection configuration priority:

```text
explicit config > environment variables > defaults
```

### Collection and Vector Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `collection_name` | `"mem0"` | Collection table name |
| `auto_create` | `True` | Automatically create the collection table on initialization |
| `embedding_model_dims` | `1536` | Embedding vector dimension |
| `deployment_mode` | `"centralized"` | GaussDB deployment mode: `centralized` or `distributed` |
| `vector_index_type` | `"gsdiskann"` | Vector index type: `gsdiskann` or `gsivfflat` |
| `vector_metric` | `"cosine"` | Vector distance metric: `cosine` or `l2` |
| `minconn` | `1` | Minimum connection pool size |
| `maxconn` | `5` | Maximum connection pool size |
| `insert_batch_size` | `2000` | Maximum rows per batch insert |
| `vector_index_maintenance_work_mem` | `None` | Temporary `maintenance_work_mem` used during vector index creation, for example `"256MB"` or `"2GB"` |

Dimension limits:

```text
centralized: embedding_model_dims <= 4096
distributed: embedding_model_dims <= 1024
embedding_model_dims > 1024 is supported only on centralized GaussDB and requires vector_index_type="gsdiskann"
```

Distributed deployments are limited to 1024 dimensions or below because vector index capability above 1024 dimensions is currently available only on centralized GaussDB. Mem0-GaussDB creates vector indexes for retrieval performance, so distributed deployments should use embedding models with 1024 dimensions or fewer.

## Filter Constraints

Supported operators:

```text
eq, ne, gt, gte, lt, lte, in, nin, contains, icontains
$and / AND, $or / OR, $not / NOT, *
```

Notes:

- `user_id`, `agent_id`, and `run_id` are redundant scope columns. They support `eq/ne/in/nin/contains/icontains`.
- Scope columns do not support `gt/gte/lt/lte` range filters.
- Non-scope payload fields support JSONB exact equality, string contains, and number / ISO-style datetime range filters.
- Unsupported operators raise `ValueError` instead of being silently downgraded.

## Keyword Search Constraints

Centralized GaussDB supports BM25 `keyword_search`. Distributed GaussDB does not support BM25 `keyword_search`.

BM25 text source priority:

```text
payload["text_lemmatized"]
payload["data"]
```

Chinese keyword search depends on the quality of `text_lemmatized` tokenization. For Chinese word-level search, explicitly store tokenized text:

```python
{
    "data": "我喜欢喝咖啡",
    "text_lemmatized": "我 喜欢 喝 咖啡"
}
```

## Notes

- Custom direct-provider IDs must be UUID strings. If `ids` is omitted, the provider generates UUIDs automatically.
- `insert()` uses upsert semantics. Writing the same `id` again replaces vector, payload, `text_lemmatized`, and scope columns.
- `update(payload=...)` uses full replacement semantics instead of merge semantics.
- Vectors and payload / JSONB filter values do not support `NaN`, `Infinity`, or `-Infinity`.
- UTF8 is recommended/required for the database and client connection, especially for Chinese `text_lemmatized` and BM25 use cases.
- The target database must have vector database capabilities enabled (`enable_vectordb`); otherwise `FLOATVECTOR`, vector indexes, and vector search capabilities are unavailable.
- This integration targets GaussDB O-compatible mode. Confirm that the target database provides `JSONB`, `FLOATVECTOR`, BM25, system catalog, and `psycopg2` connectivity first.

## More Information

- mem0 project: [https://github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)
- Mem0-GaussDB source: [https://github.com/HuaweiCloudDeveloper/mem0-GaussDB/tree/v2.0.4-gaussdb](https://github.com/HuaweiCloudDeveloper/mem0-GaussDB/tree/v2.0.4-gaussdb)
- GaussDB drivers: [https://github.com/HuaweiCloudDeveloper/gaussdb-drivers](https://github.com/HuaweiCloudDeveloper/gaussdb-drivers)
