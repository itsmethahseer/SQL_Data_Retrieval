import gradio as gr
import requests
import pandas as pd

def query_api(query):
    """Send a query to the API and return the results."""
    response = requests.post("http://localhost:8000/query", json={"query": query})
    response.raise_for_status()  # Raise an exception for bad status codes
    response_json = response.json()  # Parse the JSON response
    print('response json', response_json)
    
    # Extract the query and results
    query = response_json["query"]
    results = response_json["results"]
    
    # Convert the results to a DataFrame
    df = pd.DataFrame(results)
    
    return query, df

with gr.Blocks() as demo:
    with gr.Row():
        query_input = gr.Textbox(label="Enter your SQL query")
        submit_button = gr.Button("Submit")

    output_text = gr.Textbox(label="SQL Query")
    output_table = gr.Dataframe()

    submit_button.click(fn=query_api, inputs=query_input, outputs=[output_text, output_table])

demo.launch()
