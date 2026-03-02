# Using langchain-gaussdb for GaussDB Vector Search

This document describes how to use [langchain-gaussdb](https://github.com/HuaweiCloudDeveloper/langchain-gaussdb) to integrate GaussDB as a vector database into LangChain workflows, enabling vectorized document storage and similarity search.

## Prerequisites

- **Python Version**: Python ≥ 3.10
- **GaussDB Database**: Connection details available (host, port, username, password, database name)
- **Embedding Model Service**: An available Embedding API (e.g., OpenAI, SiliconFlow, etc.)

## Installation

Method 1: Install from source

```bash
git clone https://github.com/HuaweiCloudDeveloper/langchain-gaussdb.git
cd langchain-gaussdb
poetry install
```

Method 2: Install with pip

```bash
pip install langchain_gaussdb-0.1.0-py3-none-any.whl
```

## Quick Start

### 1. Initialize the Embedding Model

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    api_key="xxx",
    base_url="https://api.siliconflow.cn/v1",
    dimensions=1024
)
```

### 2. Connect to GaussDB Vector Store

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

### 3. Insert Documents

Use the `add_documents` function to add items to the vector store. Note that adding a document by ID will overwrite any existing document that matches that ID.

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

### 4. Delete Documents

```python
vector_store.delete(ids=["9"])
```

### 5. Similarity Search

Perform a simple similarity search with metadata filtering:

```python
results = vector_store.similarity_search(
    "ducks", k=10, filter={"location": "pond", "topic": "animals"}
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

Similarity search with score:

```python
results = vector_store.similarity_search_with_score(query="tigers", k=1)
for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")
```

### 6. Use as a Retriever

You can convert vector stores into retrievers for more convenient use within your LangChain pipeline:

```python
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1})
results = retriever.invoke("kitty")
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

## Configuration

### Connection Settings

| Parameter             | Default                 | Description                                                                                       |
|-----------------------|-------------------------|---------------------------------------------------------------------------------------------------|
| `host`                | localhost               | Database server address                                                                           |
| `port`                | 5432                    | Database connection port                                                                          |
| `user`                | gaussdb                 | Database username                                                                                 |
| `password`            | -                       | Database password                                                                                 |
| `database`            | postgres                | Default database name                                                                             |
| `min_connections`     | 1                       | Connection pool minimum size                                                                      |
| `max_connections`     | 5                       | Connection pool maximum size                                                                      |
| `table_name`          | langchain_docs          | Name of the table for storing vector data and metadata                                            |
| `index_type`          | IndexType.GSDISKANN     | Vector index algorithm type. Options: GsIVFFLAT or GsDiskANN. Default is GsDiskANN.               |
| `index_params`        | DiskAnnParams()         | Vector index params, different index_type require different index_params.                         |
| `vector_type`         | VectorType.float_vector | Type of vector representation to use. Options: floatvector or boolvector. Default is floatvector. |
| `distance_strategy`   | DistanceStrategy.COSINE | Vector similarity metric to use for retrieval. Options: l2, cosine, hamming. Default is cosine.   |
| `embedding_dimension` | 1024                    | Dimensionality of the vector embeddings.                                                          |

### Supported Combinations

| Index Types | Dimensions | Vector Type            | Supported Distance Strategies |
|-------------|-----------|------------------------|-------------------------------|
| GsIVFFLAT   | ≤1024    | floatvector/boolvector | l2/cosine/hamming             |
| GsDiskANN   | ≤4096    | floatvector            | l2/cosine                     |

## API Reference

| Method                         | Description                                 |
|--------------------------------|---------------------------------------------|
| `add_documents`                | Insert documents with automatic embedding   |
| `similarity_search`            | Basic vector similarity search              |
| `similarity_search_with_score` | Return (document, similarity_score) tuples  |
| `delete`                       | Remove documents by ID list                 |
| `get_by_ids`                   | Get documents by ID list                    |
| `drop_table`                   | Delete entire table                         |
| `from_documents`               | Initialize GaussVectorStore from documents  |

## More Information

- Repository: [langchain-gaussdb](https://github.com/HuaweiCloudDeveloper/langchain-gaussdb)
- License: MIT
