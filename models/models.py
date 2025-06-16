from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class CodeState(BaseModel):
    Flow : str = Field(description="It contains a detail start to end implementation for the project")
    Directory: Dict[str, Any] = Field(description="It contains the present directory structure of the project")
    ProjectStatus: str = Field(description="It contains the current status of the project how much it completed")


