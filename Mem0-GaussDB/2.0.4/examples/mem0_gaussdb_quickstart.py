import os

from mem0 import Memory


def main():
    api_key = os.environ["OPENAI_API_KEY"]

    config = {
        "embedder": {
            "provider": "openai",
            "config": {
                "model": os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5"),
                "api_key": api_key,
                "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1"),
            },
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": os.getenv("LLM_MODEL", "deepseek-ai/DeepSeek-V3"),
                "api_key": api_key,
                "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1"),
            },
        },
        "vector_store": {
            "provider": "gaussdb",
            "config": {
                "host": os.environ["GAUSSDB_HOST"],
                "port": int(os.getenv("GAUSSDB_PORT", "19995")),
                "user": os.environ["GAUSSDB_USER"],
                "password": os.environ["GAUSSDB_PASSWORD"],
                "database": os.getenv("GAUSSDB_DATABASE", "postgres"),
                "collection_name": os.getenv("GAUSSDB_COLLECTION", "mem0_memory"),
                "embedding_model_dims": int(os.getenv("EMBEDDING_DIMS", "1024")),
                "deployment_mode": os.getenv("GAUSSDB_DEPLOYMENT_MODE", "centralized"),
                "vector_index_type": os.getenv("GAUSSDB_VECTOR_INDEX_TYPE", "gsdiskann"),
                "vector_metric": os.getenv("GAUSSDB_VECTOR_METRIC", "cosine"),
                "auto_create": True,
            },
        },
    }

    memory = Memory.from_config(config)
    memory.add(
        "I like coffee and usually go hiking on weekends.",
        user_id="demo_user",
        infer=False,
    )

    results = memory.search("coffee", filters={"user_id": "demo_user"})
    print(results)


if __name__ == "__main__":
    main()

