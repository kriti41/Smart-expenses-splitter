import json
import ollama
from pydantic import ValidationError
from app.schemas.ai_schema import AIExpenseSchema

# ==========================================
# 1. CORE PARSING FUNCTION
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
        # Query Ollama with strict JSON formatting enforced
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

        # Step A: Parse raw text string into a native Python dict
        parsed_json = json.loads(result_text)

        # Step B: Validate structural/type integrity using the clean external schema layer
        validated_data = AIExpenseSchema(**parsed_json)
        
        print("[SUCCESS] Data matches structural requirements.")
        # Return as a clean Python dictionary
        return validated_data.model_dump()

    except json.JSONDecodeError:
        print("\n[JSON ERROR] LLM returned text that could not be parsed as valid JSON.")
        print(f"Raw Output: {result_text}\n")
        return None
    except ValidationError as e:
        print("\n[VALIDATION FAILED] JSON structure did not match Pydantic expectations.")
        print(e.json())
        return None
    except Exception as e:
        print(f"\n[SYSTEM ERROR] An unexpected error occurred: {str(e)}\n")
        return None


# ==========================================
# 2. TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    print("--- AI EXPENSE PARSER WITH PYDANTIC VALIDATION ---")
    
    example_text = "I paid 2400 for dinner split equally between me, Aman and Priya"
    print(f"Input Text: '{example_text}'")
    print("Processing with tinyllama...\n")

    extracted_data = parse_expense(example_text)

    print("\n--- FINAL RESULTS ---")
    if extracted_data:
        print(json.dumps(extracted_data, indent=4))
    else:
        print("Failed to extract valid data.")