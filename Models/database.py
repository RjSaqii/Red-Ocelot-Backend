# Imports necessary libraries for database interaction and visualization.
import psycopg2
from psycopg2.extras import RealDictCursor
import plotly.graph_objects as go

# Executes an SQL query with optional parameters.
def execute_query(query: str, params: list = None):
    try:
        # Connects to the PostgreSQL database.
        connection = psycopg2.connect(
            dbname="HackCamp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        # Creates a cursor for executing the query and fetching results as dictionaries.
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)  # Executes the SQL query.
        rows = cursor.fetchall()  # Fetches all rows returned by the query.
        connection.close()  # Closes the database connection.
        return rows  # Returns the fetched rows.
    except Exception as e:
        # Handles any exceptions during database operations.
        print(f"Database error: {e}")
        return None

# Fetches repository names from the database.
def getRepoNamesData():
    # Query to fetch all repository names from the `repositories` table.
    # The result includes a single column, `name`, which lists repository names.
    return execute_query("SELECT name FROM repositories")

# Retrieves distinct authors for a given repository name.
def getAuthors(authorName):
    # Query to fetch all unique authors who have made commits in a specific repository.
    # The repository is identified using its name.
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
    param = (authorName,)  # Parameter to replace the placeholder %s with the repository name.
    return execute_query(query, param)

# Fetches the number of commits by each author for a given repository.
def getAuthorCommitsByRepoName(repoNames):
    # Query to fetch authors and their commit counts for a specific repository.
    # The query counts the number of commits grouped by each author.
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
    param = (repoNames,)  # Parameter to replace the placeholder %s with the repository name.
    return execute_query(query, param)

# Fetches file details for a repository, filtered by functional line count.
def getFilesDetailsBYRepoName(repoNames, no_of_lines):
    # Query to fetch file details (name and functional line count) for a repository.
    # - Joins the `files`, `branches`, and `repositories` tables to link files to their repositories.
    # - Filters to exclude directory files (`is_directory = 'false'`).
    # - Filters files within the repository that have a functional line count <= specified limit.
    query = """
    SELECT f.name, f.functional_line_count
    FROM files f
    JOIN branches b ON f.branch_id = b.id
    JOIN repositories r ON b.repository_id = r.id
    WHERE f.is_directory = 'false' 
    AND r.name = %s 
    AND f.functional_line_count <= %s;
    """
    param = (repoNames, no_of_lines)  # Parameters: repository name and max functional line count.
    return execute_query(query, param)

# Fetches commits per day for a repository within a date range, filtered by a maximum commit count.
def getCommitsPerDay(repoNames, startdate, enddate, max_no_of_commits):
    # Query to fetch the number of commits made each day for a specific repository within a date range.
    # - Groups commits by day and counts them.
    # - Filters commits to the given repository name and date range.
    # - Includes only days with commit counts <= specified maximum.
    # - Orders the results by date.
    query = """ 
    SELECT 
        DATE(date) AS commit_date,
        COUNT(*) AS commit_count
    FROM 
        commits
    WHERE 
        repository_id IN (SELECT id FROM repositories WHERE name = %s)
        AND DATE(date) BETWEEN DATE(%s) AND DATE(%s)
    GROUP BY 
        DATE(date)
    HAVING 
        COUNT(*) <= %s
    ORDER BY 
        commit_date;
    """
    # Parameters: repository name, start date, end date, and max commits per day.
    param = (repoNames, startdate, enddate, max_no_of_commits)
    return execute_query(query, param)

# Fetches data for generating a bubble chart showing repository activity.
def getBubbleChartData():
    # Query to fetch data for a bubble chart:
    # - Includes repository name, commit count, watcher count, and fork count.
    # - Counts the number of commits for each repository.
    # - Groups by repository attributes to aggregate data for each repository.
    # - Orders the results by commit count in descending order.
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

# Generates a bar chart for visualizing line counts per file.
def generate_author_bar_chart(data):
    fig = go.Figure(
        data=[
            go.Bar(
                x=data["File Name"],  # File names on the x-axis.
                y=data["Line Count"],  # Line counts on the y-axis.
                text=data["Line Count"],  # Display line count values on the bars.
                textposition='auto'  # Automatically position the text.
            )
        ]
    )
    fig.update_layout(
        title="Line Count per File",  # Title of the bar chart.
        xaxis_title="File Name",      # Label for the x-axis.
        yaxis_title="Line Count"      # Label for the y-axis.
    )
    return fig.to_plotly_json()
