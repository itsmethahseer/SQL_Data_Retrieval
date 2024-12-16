import json
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import google.generativeai as genai
from google.generativeai import GenerationConfig, GenerativeModel
from dotenv import load_dotenv
import os
load_dotenv(".env",override=True)


# Initialize FastAPI app
app = FastAPI()

# PostgreSQL database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT'))  # Convert port to integer
}

# Pydantic model for request body
class QueryRequest(BaseModel):
    query: str

# Function to execute SQL queries
def execute_query(query):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return str(e)

# Function to generate SQL query using Gemini API
def extract_invoice_details(base64_data, prompt):
    try:
        logging.info("Gemini API call starting")

        # Configure Gemini API
        genai.configure(api_key=os.getenv('API_KEY'))  # Ensure API_KEY is set in the environment

        # Prepare generation configuration
        generation_config = GenerationConfig(
            response_mime_type="application/json",
            temperature=0,
            top_k=10,
            top_p=0.01,
        )

        system_instruction = (
            """You are a skilled SQL Query Expert. Analyze the database schema and user query, 
            and generate an optimized SQL query to retrieve the requested data.
            in the following format {"optimized_query":"string""}"""
        
        )

        # Initialize the Gemini model
        model = GenerativeModel(
            model_name='gemini-1.5-pro',
            generation_config=generation_config,
            system_instruction=system_instruction,
        )

        # Perform the Gemini API call
        response = model.generate_content([system_instruction, {"mime_type": "text/plain", "data": base64_data}, prompt])
        logging.info("Response successfully returned from Gemini")

        # Extract and return the text response
        response_json = json.loads(response.text)
        print(response_json)
        sql_query = response_json.get("optimized_query")

        if not sql_query:
            raise ValueError("Gemini API did not generate a valid SQL query.")

        return sql_query
    except Exception as e:
        logging.error(f"Error in Gemini API call: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

# FastAPI route to handle queries
@app.post("/query")
async def handle_query(request: QueryRequest):
    user_query = request.query
    base64_schema = "SGVsbG8gdGhpcyBpcyBhIHNjaGVtYSBwbGFjZWhvbGRlci4="

    # Step 1: Generate SQL query using Gemini API
    sql_query = extract_invoice_details(base64_schema, user_query)
    print(sql_query)

    # Step 2: Execute the SQL query
    results = execute_query(sql_query)

    if isinstance(results, str):  # If an error occurred
        raise HTTPException(status_code=500, detail=results)

    # Step 3: Return results
    return {"query": sql_query, "results": results}