from fastapi import APIRouter, Depends, HTTPException, Query, Body
from nexus_agent.api.dependencies import get_nexus_agent
from nexus_agent.agent.agent import NexusLangChainAgent
from typing import Dict, List, Optional

router = APIRouter()

@router.post("/", response_model=Dict[str, str])
async def create_session(
    user_id: Optional[str] = Body(None, embed=True),
    agent: NexusLangChainAgent = Depends(get_nexus_agent)
):
    if not agent.session_manager:
        raise HTTPException(status_code=501, detail="Memory not enabled")
    session_id = agent.session_manager.create_session(user_id=user_id)
    return {"session_id": session_id}

@router.get("/{session_id}", response_model=Dict)
async def get_session(
    session_id: str,
    agent: NexusLangChainAgent = Depends(get_nexus_agent)
):
    if not agent.session_manager:
        raise HTTPException(status_code=501, detail="Memory not enabled")
    session = agent.session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/{session_id}/history", response_model=List[Dict])
async def get_session_history(
    session_id: str,
    limit: Optional[int] = Query(None, ge=1, le=100),
    agent: NexusLangChainAgent = Depends(get_nexus_agent)
):
    if not agent.session_manager:
        raise HTTPException(status_code=501, detail="Memory not enabled")
    return agent.session_manager.get_conversation_history(session_id, limit)
