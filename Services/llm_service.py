"""
    First Setup of Google Generative AI Service

    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh\nbash Miniconda3-latest-MacOSX-arm64.sh\n
    conda create -n gemini python=3.11\nconda activate gemini\npip install google-generativeai\n
    export GOOGLE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    pip install google-generativeai\n
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 1. Configuration
genai.configure(api_key=api_key)
generation_config = genai.GenerationConfig(
    temperature=0.5,
    max_output_tokens=1000,
    top_p=1,
    top_k=1
)

# Trip planning prompt template
TRIP_PLANNING_PROMPT = """
You are an AI agent that helps users plan trips. Your job is to extract key parameters from their query.
If the query is related to planning a trip, return a JSON with the following fields:
- source 
- destination
- weather_preference
- travel_dates (if mentioned)
- hotel_preferences (if mentioned)
- any other relevant info

If the query is NOT about planning a trip or some data is missing, respond with a message saying:
"This AI agent is designed specifically to help plan trips. Please ask something like 'Plan a trip to CA on a sunny day'. or 
"Please provide a complete trip planning query with source, destination, and any other relevant details."

IMPORTANT: Return ONLY the JSON object without any markdown formatting, code blocks, or additional text. 
Your response should be a valid JSON string that can be directly parsed.

Example queries:
- "Plan a trip to California on a sunny day"
- "Book a flight from New York to San Francisco on a sunny weekend"
- "Find hotels in Paris for a family trip next month"
- "What are the best sunny days to visit Florida in December?"
- "I want to travel from London to Tokyo in the spring"
- "Book a hotel in Miami for next weekend"
- "Plan a trip to New York for a family vacation in July"
- "What are the best sunny days to visit Florida in December?"

User query: "{query}"
"""

# 2. Function to process user query and generate content
# query: str
# Returns: 
"""
    For Success Case:
    {
        "status": "success",
        "data": {
            "source": "New York"
            "destination": "California",
            "weather_preference": "sunny",
            "travel_dates": "weekend",
            "hotel_preferences": null,
            "other_info": "family trip",
        }
    }

    For Case other than trip planning:
    {
        "status": "success",
        "data": "This AI agent is designed specifically to help plan trips. Please ask something like 'Plan a trip to CA on a sunny day'."
    }
"""
def process_query(query: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
        prompt = TRIP_PLANNING_PROMPT.format(query=query)
        response = model.generate_content([prompt])

        # Clean up the response text and try to parse as JSON
        response_text = response.text.strip()
        if response_text.startswith('```'):
            # Remove ```json and ``` markers
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        try:
            parsed = json.loads(response_text)
            return json.dumps({"status": "success", "data": parsed}, indent=4)
        except json.JSONDecodeError:
            return json.dumps({"status": "success", "data": response_text}, indent=4)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=4)