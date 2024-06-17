import sqlite3
from typing import List, Dict

# SQLite database file path
DB_FILE = 'repository_analysis.db'

def create_connection(db_file: str) -> sqlite3.Connection:
    """
    Create a database connection to the SQLite database specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        raise ValueError(f"Error connecting to database: {e}")

def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create necessary tables in the database if they don't exist
    """
    try:
        cursor = conn.cursor()

        # Create analysis_results table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repository_url TEXT NOT NULL,
                class_name TEXT,
                function_name TEXT,
                endpoint TEXT
            )
        """)

        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Error creating tables: {e}")

def store_analysis_result(repo_url: str, analysis_result: Dict[str, List[str]]) -> None:
    """
    Store the analysis results (classes, functions, endpoints) in the database
    """
    try:
        conn = create_connection(DB_FILE)
        create_tables(conn)

        cursor = conn.cursor()

        for class_name in analysis_result.get('classes', []):
            cursor.execute("INSERT INTO analysis_results (repository_url, class_name) VALUES (?, ?)",
                           (repo_url, class_name))

        for function_name in analysis_result.get('functions', []):
            cursor.execute("INSERT INTO analysis_results (repository_url, function_name) VALUES (?, ?)",
                           (repo_url, function_name))

        for endpoint in analysis_result.get('endpoints', []):
            cursor.execute("INSERT INTO analysis_results (repository_url, endpoint) VALUES (?, ?)",
                           (repo_url, endpoint))

        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Error storing analysis result in database: {e}")
    finally:
        if conn:
            conn.close()

def query_analysis_results(repo_url: str) -> List[Dict[str, str]]:
    """
    Query analysis results from the database for a given repository URL
    """
    try:
        conn = create_connection(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM analysis_results WHERE repository_url=?", (repo_url,))
        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = {
                'class_name': row[2],
                'function_name': row[3],
                'endpoint': row[4]
            }
            results.append(result)

        return results
    except sqlite3.Error as e:
        raise ValueError(f"Error querying analysis results from database: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    # Example repository URL
    repo_url = "https://github.com/username/repository"

    try:
        # Example analysis result
        analysis_result = {
            'classes': ['ClassA', 'ClassB'],
            'functions': ['functionA', 'functionB'],
            'endpoints': ['/api/get_data', '/api/post_data']
        }

        # Store analysis result in database
        store_analysis_result(repo_url, analysis_result)
        print("Analysis result stored in the database.")

        # Query analysis results from database
        query_results = query_analysis_results(repo_url)
        print("Query results from the database:")
        for result in query_results:
            print(result)
    
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
