import os

from mem0.vector_stores.gaussdb import GaussDB


def main():
    db = GaussDB(
        host=os.environ["GAUSSDB_HOST"],
        port=int(os.getenv("GAUSSDB_PORT", "19995")),
        user=os.environ["GAUSSDB_USER"],
        password=os.environ["GAUSSDB_PASSWORD"],
        database=os.getenv("GAUSSDB_DATABASE", "postgres"),
        collection_name=os.getenv("GAUSSDB_COLLECTION", "mem0_provider_demo"),
        embedding_model_dims=4,
        deployment_mode=os.getenv("GAUSSDB_DEPLOYMENT_MODE", "centralized"),
        vector_index_type=os.getenv("GAUSSDB_VECTOR_INDEX_TYPE", "gsdiskann"),
        vector_metric=os.getenv("GAUSSDB_VECTOR_METRIC", "cosine"),
        auto_create=True,
    )

    db.insert(
        vectors=[[1.0, 0.0, 0.0, 0.0]],
        payloads=[{
            "data": "I like coffee",
            "text_lemmatized": "I like coffee",
            "user_id": "demo_user",
        }],
    )

    rows = db.search(
        query="coffee",
        vectors=[1.0, 0.0, 0.0, 0.0],
        top_k=5,
        filters={"user_id": "demo_user"},
    )
    print(rows)


if __name__ == "__main__":
    main()

