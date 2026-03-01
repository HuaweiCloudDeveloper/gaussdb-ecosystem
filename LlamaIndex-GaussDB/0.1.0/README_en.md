# Using llama-index-vector-stores-gaussdb for GaussDB Vector Search

This document describes how to use [llama-index-vector-stores-gaussdb](https://github.com/HuaweiCloudDeveloper/llama-index-vector-stores-gaussdb) to integrate GaussDB as a vector database into LlamaIndex workflows, enabling vectorized document storage and semantic search.

## Prerequisites

- **Python Version**: Python ≥ 3.10
- **GaussDB Database**: Connection details available (host, port, username, password, database name)
- **OpenAI API Key**: Or another compatible LLM/Embedding service

## Installation

### 1. Install pygsvector SDK

```bash
pip install pygsvector-0.1.0-py3-none-any.whl
```

### 2. Install llama-index-vector-stores-gaussdb

Method 1: Install from source

```bash
git clone https://github.com/HuaweiCloudDeveloper/llama-index-vector-stores-gaussdb.git
cd llama-index-vector-stores-gaussdb
poetry install
```

Method 2: Install with pip

```bash
pip install llama_index-0.1.0-py3-none-any.whl
```

## Quick Start

### 1. Setup OpenAI

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

### 2. Prepare Documents

```bash
mkdir -p 'data/paul_graham/'
wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)
```

### 3. Initialize Vector Store

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
    dim=1024,  # embedding dimension
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

### 4. Create the Index

```python
from llama_index.core import StorageContext, VectorStoreIndex

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context,
)
```

### 5. Query the Index

```python
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What did the author do?")

print(response.response)
print("Source nodes:", [src.node.get_content()[:100] for src in response.source_nodes])
```

## More Information

- Repository: [llama-index-vector-stores-gaussdb](https://github.com/HuaweiCloudDeveloper/llama-index-vector-stores-gaussdb)
- License: MIT
