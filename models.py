from pydantic import BaseModel
from typing import Any, List, Optional, Dict, Union

# Input/output models for perception layer:

class PerceptionInput(BaseModel):
    query: str



class PerceptionResult(BaseModel):
   query: str
   intent: Optional[str] 
   entities: Optional[List[str]]  # Assuming entities is a list of dictionaries
   geography: Optional[str]
   

# input/output models for memory layer:

class MemoryInput(BaseModel):
    iteration: int
    function_name: str
    arguments: Dict[str, Any]   
    result: Any


class MemoryResult(BaseModel):
    memory: str
    


# input/output models for decision layer:

class DecisionInput(BaseModel):
    user_input: str
    memory: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class DecisionResult(BaseModel):
    output: str
    context: Optional[Dict[str, Any]] = None    


# input/output models for action (tool execution) layer:

class ExecuteToolInput(BaseModel):
    session : Any
    tools: List[Any]
    response: str

class ExecuteToolResult(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Union[str, List[str], Dict[str, Any]]
    raw_result: Any


class ParseFunctionInput(BaseModel):
     response: str

class ParseFunctionResult(BaseModel):
    output:tuple[str,Dict[str, Any]]