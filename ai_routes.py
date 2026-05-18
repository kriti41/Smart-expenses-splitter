import json
import ollama
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app.schemas.ai_schema import AIExpenseSchema

# Clean, local router instance initialization
router = APIRouter()

# ==========================================
# CORE INFERENCE LOGIC
# ==========================================
def parse_expense(text: str) -> dict | None:
    """
    Uses a local LLM via Ollama to extract structured expense information
    and validates it strictly using an imported Pydantic Schema.
    """
    prompt = f"""You are a strict data extraction API. 
Your job is to read the provided text and extract information into the exact JSON schema defined below.

Schema:
{{
    "description": "string",
    "amount": number,
    "payer": "string",
    "participants": ["string"]
}}

Text to extract from:
"{text}"
"""
    try:
        response = ollama.chat(
            model="tinyllama",
            format="json",  
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result_text = response["message"]["content"].strip()
        parsed_json = json.loads(result_text)
        validated_data = AIExpenseSchema(**parsed_json)
        
        return validated_data.model_dump()

    except (json.JSONDecodeError, ValidationError) as e:
        print(f"[AI PARSE ERROR] Extraction or validation failed: {str(e)}")
        return None
    except Exception as e:
        print(f"[SYSTEM ERROR] Unexpected failure: {str(e)}")
        return None


# ==========================================
# FASTAPI ENDPOINTS
# ==========================================
@router.get("/")
def test_ai():
    """Simple health-check endpoint for the AI module."""
    return {
        "success": True,
        "message": "AI route layer initialized successfully"
    }


@router.post("/parse-expense")
def ai_parse_expense(text_input: str):
    """
    Accepts raw conversational text and returns a strictly validated 
    expense structure using a local LLM engine.
    """
    extracted_data = parse_expense(text_input)
    
    if not extracted_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="AI engine failed to parse text into a structurally valid expense configuration."
        )
        
    return extracted_data