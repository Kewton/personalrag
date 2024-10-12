from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.schemas.graphrag.neo4j_message import Neo4jMessage
from app.core.neo4j.analyzeAndStoreKnowledge import AnalyzeAndStoreKnowledge
from app.core.neo4j.extractKnowledgeAndSummalize import ExtractKnowledgeAndSummalize
from app.core.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog


router = APIRouter()


@router.post("/updateneo4j")
def update_neo4j(request: Neo4jMessage):
    try:
        text = request.message
        print(text)
        AnalyzeAndStoreKnowledge(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD).do(text)
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")


@router.post("/summarygraph")
def summarygraph(request: Neo4jMessage):
    try:
        text = request.message
        print(text)
        resutlt = ExtractKnowledgeAndSummalize(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD).do(text)
        print(resutlt)
        return resutlt
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")