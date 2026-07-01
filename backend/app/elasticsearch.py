from elasticsearch import Elasticsearch

_es: Elasticsearch | None = None


def get_es() -> Elasticsearch:
    global _es
    if _es is None:
        _es = Elasticsearch("http://localhost:9200")
    return _es
