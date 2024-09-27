from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownTextSplitter
import os
import glob
from app.utils.logger import declogger, writeinfolog, writedebuglog

markdown_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=100)


@declogger
def markdownLoadeAndSplite(_file_name):
    loader = UnstructuredMarkdownLoader(_file_name)
    _docs = loader.load()
    return markdown_splitter.split_documents(_docs)


@declogger
def doclist2docs(_doclist):
    documents = []
    for _filename in _doclist:
        # 並列でやりたいね
        for _doc in markdownLoadeAndSplite(_filename):
            documents.append(_doc)
    return documents


@declogger
def get_markdown_files(directory_path: str) -> list:
    """
    指定したディレクトリパスから再帰的にMarkdownファイルを取得し、リストに格納して返す関数。

    Args:
        directory_path (str): 検索を開始するディレクトリのパス。

    Returns:
        list: 再帰的に取得されたMarkdownファイルのパスのリスト。
    """
    # 指定されたディレクトリパスから再帰的にすべてのMarkdownファイルを取得
    markdown_files = glob.glob(os.path.join(directory_path, '**', '*.md'), recursive=True)
    return markdown_files


@declogger
def createDocuments(_doc_dir):
    _doclist = get_markdown_files(_doc_dir)
    documents = doclist2docs(_doclist)
    return documents
