import uuid
import time
from fastapi import APIRouter, Depends, HTTPException
from nexus_agent.api.dependencies import get_nexus_agent
from nexus_agent.agent.agent import NexusLangChainAgent
from nexus_agent.api.schemas.chat import ChatCompletionRequest, ChatCompletionResponse

router = APIRouter()

@router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: ChatCompletionRequest,
    agent: NexusLangChainAgent = Depends(get_nexus_agent)
):
    try:
        # Get last user message
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        user_input = request.messages[-1].content
        
        # Call Agent
        response = agent.process_message(
            user_input=user_input,
            session_id=request.session_id,
            user_id=request.user
        )
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)

        # Construct response
        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4()}",
            created=int(time.time()),
            model=agent.model,
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.content,
                    "tool_calls": response.tool_calls
                },
                "finish_reason": "stop"
            }],
            nexus_metadata={
                "session_id": response.session_id,
                "duration": response.duration
            }
        )
    except Exception as e:
        # Re-raise HTTP exceptions to preserve status codes
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
