from urllib.parse import urlparse


def extract_last_segment(url):
    """
    指定されたURLから最後のパスセグメントを抽出します。

    Parameters:
    url (str): 解析するURL文字列

    Returns:
    str: 最後のパスセグメント（例: 'multilingual-e5-large'）
    """
    parsed_url = urlparse(url)
    path = parsed_url.path  # '/intfloat/multilingual-e5-large'
    last_segment = path.rstrip('/').split('/')[-1]
    return last_segment


def extract_path(url):
    """
    指定されたURLからパス部分を抽出し、末尾の'.git'を削除します。
    
    Parameters:
    url (str): 解析するURL文字列
    
    Returns:
    str: 抽出されたパス（例: '/Kewton/rag-document'）
    """
    parsed_url = urlparse(url)
    path = parsed_url.path  # '/Kewton/rag-document.git'
    
    if path.endswith('.git'):
        path = path[:-4]  # '.git'を削除
    
    return path
