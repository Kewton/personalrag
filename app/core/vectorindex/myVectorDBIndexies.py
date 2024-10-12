from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import faiss
import numpy as np
from app.core.config import INDEX_SAVE_DIR, MODEL_DOWNLOAD_DIR
import json


def normalize_vectors(vectors):
    """ ベクトルを正規化する関数 """
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


class LoadVectorDBIndex:
    def __init__(self, _modelname):
        self.model = _modelname
        self.storage_path = os.path.join(INDEX_SAVE_DIR, _modelname)
        self.model_path = os.path.join(MODEL_DOWNLOAD_DIR, _modelname)
        self.setindex()
        self.setindex_cosinesimilarity()

    def reload(self):
        self.setindex()
        self.setindex_cosinesimilarity()

    def setindex(self):
        try:
            self.index = FAISS.load_local(
                self.storage_path,
                embeddings=HuggingFaceEmbeddings(model_name=self.model_path),
                allow_dangerous_deserialization=True
            )
            self.indexstatus = True
            return True
        except Exception as e:
            print(e)
            self.indexstatus = False
            return False

    def setindex_cosinesimilarity(self):
        if not self.indexstatus:
            return False

        # コサイン類似度を使用するために、内積（Inner Product）を使用するインデックスを作成
        dimension = self.index.index.d  # 既存インデックスの次元数を取得
        new_index = faiss.IndexFlatIP(dimension)  # 内積ベースのインデックスを作成

        # 既存のベクトルを正規化してから新しいインデックスに追加
        stored_vectors = self.index.index.reconstruct_n(0, self.index.index.ntotal)
        normalized_vectors = normalize_vectors(stored_vectors)
        new_index.add(normalized_vectors)

        # 正規化されたインデックスを持つFAISSインスタンスを再作成
        self.index.index = new_index

        # インデックスのメトリックを確認
        index_metric = self.index.index.metric_type
        self._metric = ""
        if index_metric == faiss.METRIC_L2:
            self._metric = "This index uses Euclidean distance (L2 distance)."
        elif index_metric == faiss.METRIC_INNER_PRODUCT:
            self._metric = "This index uses Cosine similarity (via Inner Product)."
        else:
            self._metric = "Unknown metric type."
        return True

    def similarity_search_with_score(self, _question, _k=5):
        results = self.index.similarity_search_with_score(_question, k=_k)

        _context = []
        for _document, score in results:
            _context.append(
                {
                    "source": _document.metadata["source"],
                    "metric": self._metric,
                    "score": float(score),
                    "page_content": _document.page_content
                }
            )
        response = {
            "input_query": _question,
            "similarity_search_result": _context
        }
        #response = json.dumps(response, ensure_ascii=False, indent=4)
        #print(response)
        return response


class MyVectorDBIndexies:
    def __init__(self):
        self.models = {}

    def reload(self, _modelname):
        model = self.models.get(_modelname)
        if model is None:
            self.models[_modelname] = LoadVectorDBIndex(_modelname)
            return self.models[_modelname].indexstatus
        else:
            model.reload()
            return model.indexstatus

    def getindexstatus(self, _modelname):
        model = self.models.get(_modelname)
        if model is None:
            return False
        else:
            return model.indexstatus

    def similarity_search_with_score(self, _modelname, _question, _k=5):
        model = self.models.get(_modelname)
        if model is None:
            return "error_1"
        else:
            if model.indexstatus:
                return model.similarity_search_with_score(_question, _k=5)
            else:
                if model.reload():
                    return model.similarity_search_with_score(_question, _k=5)
                else:
                    return "error_2"


MyVectorDB = MyVectorDBIndexies()
