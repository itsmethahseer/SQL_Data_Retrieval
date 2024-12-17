# Chat-Based Data Retrieval using LLM and SQL

This project is a chat-based application that allows users to query a Postgres database in natural language and view the retrieved data in a tabular format. The application leverages **Google's Gemini LLM** to convert user queries into SQL statements, execute them on the database, and display results in an interactive UI using **Gradio**. The application is deployed using **FastAPI**.

## Key Features
- **Natural Language Queries:** Users can input queries in plain English.
- **SQL Query Generation:** The LLM generates SQL queries dynamically based on user input.
- **Postgres Integration:** Executes the generated SQL on a Postgres database.
- **Tabular Results:** The queried data is displayed in a clean, tabular format.
- **Interactive UI:** Gradio-based UI for a user-friendly experience.
- **FastAPI Backend:** API endpoints for query handling and data retrieval.

---

## Architecture Overview

The project is structured into two main components:

1. **Backend (FastAPI):** Handles model implementation, database connection, and query execution.
   - File: `pipeline.py`
   - Responsibilities:
     - Connect to the Postgres database.
     - Use the Gemini model to generate SQL queries.
     - Execute the queries and fetch results.
     - Expose endpoints to interact with the backend.

2. **Frontend (Gradio):** Provides a simple chat-based UI for users.
   - File: `main.py`
   - Responsibilities:
     - Build a Gradio interface for user interaction.
     - Fetch results from the FastAPI backend and display them in tabular form.

---

## Project Structure

```bash
project-root/
├── pipeline.py      # Backend: Model implementation, DB connection, FastAPI endpoints
├── main.py          # Frontend: Gradio UI implementation
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## Installation

### Prerequisites
- **Python 3.8+**
- **PostgreSQL Database**
- **Uvicorn** (ASGI server for FastAPI)

### Steps

1. **Clone the repository:**
   ```bash
   git clone 
   cd your_project_name
   ```

2. **Set up the environment:**
   Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database Connection:**
   Update the database connection details in `pipeline.py`:
   ```python
   DB_CONFIG = {
       'host': 'your_db_host',
       'port': 'your_db_port',
       'database': 'your_db_name',
       'user': 'your_db_user',
       'password': 'your_db_password'
   }
   ```

4. **Run the FastAPI Backend:**
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn pipeline:app --reload
   ```
   The API will be available at: `http://localhost:8000`

5. **Launch the Gradio UI:**
   Run the `main.py` file:
   ```bash
   python main.py
   ```
   The Gradio UI will be available in your browser.

---

## Usage

1. **Run the Application:** Follow the steps above to launch the FastAPI backend and Gradio UI.
2. **Access the Gradio Interface:** Open the Gradio URL displayed in the terminal.
3. **Ask Questions:** Type a query in natural language (e.g., *"Show me all employees in the Sales department"*).
4. **View Results:** The data will be fetched from the database and displayed in tabular format.

---

## Example Flow
1. User enters: **"List all customers who made purchases in August."**
2. The LLM generates the SQL query:
   ```sql
   SELECT * FROM customers WHERE purchase_date BETWEEN '2023-08-01' AND '2023-08-31';
   ```
3. The query is executed on the Postgres database.
4. Results are displayed in the Gradio UI.

## Tech Stack
- **Backend:** FastAPI
- **LLM:** Google Gemini
- **Database:** PostgreSQL
- **Frontend:** Gradio
- **Deployment:** Uvicorn

---

## Future Improvements
- Add authentication and authorization.
- Support for multiple database backends.
- Implement caching for frequently asked queries.
- Add error handling for invalid SQL or natural language inputs.

---

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you'd like to change.

## Contact
For any questions or feedback:
- **Name:** Thahseer
- **Email:** [your_email@example.com](mailto:zacthahseer123@gmail.com)
- **GitHub:** [https://github.com/your_username](https://github.com/itsmethahseer)

---

**Enjoy querying your database effortlessly with natural language! 🚀**

