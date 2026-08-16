import os
from opensearchpy import OpenSearch

INDEX = "jobs"

def client():
    return OpenSearch(os.getenv("OPENSEARCH_URL", "http://localhost:9200"))

def ensure_index():
    c = client()
    if not c.indices.exists(index=INDEX):
        c.indices.create(
            index=INDEX,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "skills": {"type": "keyword"},
                        "company_id": {"type": "integer"},
                    }
                }
            },
        )

def index_job(job):
    ensure_index()
    client().index(
        index=INDEX,
        id=job.id,
        body={
            "title": job.title,
            "description": job.description,
            "skills": job.skills or [],
            "company_id": job.company_id,
        },
        refresh=True,
    )

def search_jobs(query):
    ensure_index()
    response = client().search(
        index=INDEX,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "description", "skills"]
                }
            }
        },
    )
    return [
        {"id": hit["_id"], **hit["_source"]}
        for hit in response["hits"]["hits"]
    ]
