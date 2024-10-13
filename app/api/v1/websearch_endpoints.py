from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.schemas.websearch.duckduckgo_search import DdgsText, Response2md
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog
from app.utils.html_operation import html_to_markdown
from duckduckgo_search import DDGS
import json
import requests


router = APIRouter()


@router.post("/websearch/keyword")
def websearch_keyword(request: DdgsText):
    try:
        # クエリ
        with DDGS() as ddgs:
            results = list(ddgs.text(
                keywords=request.keywords,      # 検索ワード
                region=request.region,       # リージョン 日本は"jp-jp",指定なしの場合は"wt-wt"
                safesearch='off',     # セーフサーチOFF->"off",ON->"on",標準->"moderate"
                timelimit=None,       # 期間指定 指定なし->None,過去1日->"d",過去1週間->"w",
                                    # 過去1か月->"m",過去1年->"y"
                max_results=request.max_results         # 取得件数
            ))
        return {"result": results}
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")


@router.post("/websearch/url")
def websearch_url(request: Response2md):
    try:
        url = request.url  # 取得したいURLを指定
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text

            # 関数を使ってHTMLをMarkdownに変換
            markdown_content = html_to_markdown(html_content)
            #with open('output.md', 'w', encoding='utf-8', newline='\n') as f:
            #    f.write(markdown_content)

        return {"result": markdown_content}
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")