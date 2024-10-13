import pytest
from app.utils.url_operation import extract_last_segment, extract_path


# `extract_last_segment` 関数のテスト
def test_extract_last_segment():
    url_1 = "https://huggingface.co/intfloat/multilingual-e5-large"
    url_2 = "https://github.com/Kewton/rag-document/"
    url_3 = "https://example.com/api/v1/resource/123/"
    
    assert extract_last_segment(url_1) == "multilingual-e5-large"
    assert extract_last_segment(url_2) == "rag-document"
    assert extract_last_segment(url_3) == "123"


# `extract_path` 関数のテスト
def test_extract_path():
    url_1 = "https://github.com/Kewton/rag-document.git"
    url_2 = "https://github.com/Kewton/rag-document"
    url_3 = "https://example.com/api/v1/resource/123"
    
    assert extract_path(url_1) == "/Kewton/rag-document"
    assert extract_path(url_2) == "/Kewton/rag-document"
    assert extract_path(url_3) == "/api/v1/resource/123"
