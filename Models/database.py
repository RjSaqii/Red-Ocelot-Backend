import psycopg2
from psycopg2.extras import RealDictCursor

def execute_query(query: str, params: list = None):
    """
    Executes a query with optional placeholders and variables.

    Args:
        query (str): The SQL query with placeholders (e.g., %s).
        params (list): The variables to bind to the query placeholders.

    Returns:
        list: The query result as a list of {attributes: value} dictionaries.
    """
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            dbname="HackCamp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Execute the query with parameters
        cursor.execute(query, params)

        # Fetch and format the results
        rows = cursor.fetchall()
        print(rows)
        formatted_results = [{key: value} for row in rows for key, value in row.items()]
        connection.close()
        return formatted_results

    except Exception as e:
        # Log or raise the error as needed
        print(f"Database error: {e}")
        return None

    # finally:
    #     # Ensure the connection is closed
    #     if connection:
    #         connection.close()

def getRepoNamesData():
    return execute_query("SELECT name FROM repositories")

def getAuthors(authorName):

    query = """ 
        SELECT DISTINCT
            author 
        FROM 
            commits 
        WHERE repository_id = (
            SELECT id
            FROM repositories
            WHERE name = %s
        )
"""
    # query.replace("?", authorName)
    print("----")
    print(authorName)
    print("----")
    print(query)
    param = (authorName,)
    return execute_query(query,param)

def getAuthorCommitsByRepoName(repoNames):

    query = """ 
        SELECT 
            author, 
			COUNT(*) AS commit_count
        FROM 
            commits 
        WHERE repository_id = (
            SELECT id
            FROM repositories
            WHERE name = 'fhir-data-pipes'
        )
		GROUP BY 
		author
		ORDER BY commit_count DESC
"""
    # query.replace("?", authorName)
    print("----")
    print(repoNames)
    print("----")
    print(query)
    param = (repoNames,)
    return execute_query(query,param)


