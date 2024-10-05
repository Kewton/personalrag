from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.schemas.neo4j_schema import Neo4jSchema
from app.core.knowledgeGraph import KnowledgeGraph
from app.core.knowledgeExtractor import KnowledgeExtractor
from app.core.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

router = APIRouter()

@router.post("/updateneo4j")
def update_neo4j(request: Neo4jSchema):
    try:
        text = request.message
        print(text)
        KnowledgeGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD).do(text)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")


@router.post("/summarygraph")
def summarygraph(request: Neo4jSchema):
    try:
        text = request.message
        print(text)
        resutlt = KnowledgeExtractor(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD).do(text)
        print(resutlt)
        return resutlt
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")