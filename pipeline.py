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

load_dotenv(".env", override=True)

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

def get_table_names(db_config):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    table_names = cur.fetchall()
    conn.close()
    return [table[0] for table in table_names]

table_names = get_table_names(DB_CONFIG)

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
def generate_sql_query(user_query, table_names):
    try:
        # Configure Gemini API
        genai.configure(api_key=os.getenv('API_KEY'))

        # Prepare generation configuration
        generation_config = GenerationConfig(
            response_mime_type="application/json",
            temperature=0,
            top_k=10,
            top_p=0.01,
        )

        table_names_str = ", ".join(table_names)  # Convert list to a comma-separated string

        prompt = f"""
        You are a skilled SQL Query Expert. Analyze the database schema and user query, 
        and generate an optimized SQL query to retrieve the requested data.

        User Query: {user_query}

        You have access to the following tables: {table_names_str}.
        You can find the keywords in the user query to match with one of the tables.

        You may find multiple tables in the schema. You need to search accurately to check whether any table matches the name or context in the user query.

        ### Example:
        - User Query: `please give me the top 3 person's age`
        Then "person" will be a table in the schema and "age" will be a column. 
        Generate the query like: `SELECT Age FROM person LIMIT 3;`.

        **Important Note:**
        Always include a delimiter (e.g., semicolon) at the end of the SQL query. If it is missing, the query cannot be executed.

        Please return the output in the following JSON format:
        {{"optimized_query": "string"}}
        """

        print(prompt)
        # Initialize the Gemini model
        model = GenerativeModel(
            model_name='gemini-1.5-pro',
            generation_config=generation_config)

        # Perform the Gemini API call
        response = model.generate_content(prompt)
        logging.info("Response received from Gemini")

        # Print the raw response (for debugging)
        logging.debug(f"Raw response: {response.text}")

        # Extract and return the text response
        response_json = json.loads(response.text)
        sql_query = response_json.get("optimized_query")

        if not sql_query:
            raise ValueError("LLM API did not generate a valid SQL query.")

        return sql_query
    except Exception as e:
        logging.error(f"Error in Gemini API call: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

# FastAPI route to handle queries
@app.post("/query")
async def handle_query(request: QueryRequest):
    user_query = request.query

    # Step 1: Generate SQL query using Gemini API
    sql_query = generate_sql_query(user_query,table_names)

    # Step 2: Execute the SQL query
    results = execute_query(sql_query)
    print("results",results)
    if isinstance(results, str):  # If an error occurred
        raise HTTPException(status_code=500, detail=results)

    # Step 3: Return results
    return {"query": sql_query, "results": results}