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
        #print(rows)
        #formatted_results = [{key: value} for row in rows for key, value in row.items()]
        connection.close()
        return rows

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
    #print("----")
    #print(authorName)
    #print("----")
    #print(query)
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
            WHERE name = %s
        )
		GROUP BY 
		author
		ORDER BY commit_count DESC
"""
    # query.replace("?", authorName)
    #print("----")
    #print(repoNames)
    #print("----")
    #print(query)
    param = (repoNames,)
    return execute_query(query,param)



def getFilesDetailsBYRepoName(repoNames):

    query = """ 
    SELECT f.name,f.functional_line_count
    FROM files f
    JOIN branches b ON f.branch_id = b.id
    JOIN repositories r ON b.repository_id = r.id
    WHERE f.is_directory = 'false' AND r.name = %s;
"""
    
    param = (repoNames,)
    return execute_query(query,param)


def getCommitsPerDay(repoNames, startdate, enddate):

    query = """ 
    SELECT 
        DATE(date) AS commit_date,
        COUNT(*) AS commit_count
    FROM 
        commits
    WHERE 
        repository_id IN (SELECT id FROM repositories WHERE name = %s)
        AND DATE(date) BETWEEN %s AND %s
    GROUP BY 
        DATE(date)
    ORDER BY 
        commit_date;

"""
    
    param = (repoNames,startdate,enddate)
    return execute_query(query,param)

def getBubbleChartData():
    query = """
    SELECT 
        r.name AS repository_name,
        COUNT(c.id) AS commit_count,
        r.watchers AS watcher_count,
        r.forks_count AS fork_count
    FROM 
        commits c
    INNER JOIN 
        repositories r ON c.repository_id = r.id
    GROUP BY 
        r.id, r.name, r.watchers, r.forks_count
    ORDER BY 
        commit_count DESC;
    """
    
    return execute_query(query)
