import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import json


# Simulated commit data, will be replaced by database later
commit_history = [
    {"repo": "Cobol2XML", "commit_date": "2023-12-01", "commit_message": "Initial commit", "commit_author": "julianbass", "file_sizes": [200, 500, 120, 300, 50]}, 
    {"repo": "fhir-data-pipes", "commit_date": "2023-12-02", "commit_message": "Added feature for data transformation", "commit_author": "johndoe", "file_sizes": [1000, 2000, 1500, 500]},
    {"repo": "Dubbo", "commit_date": "2023-12-03", "commit_message": "Refactored utility classes", "commit_author": "janedoe", "file_sizes": [300, 400, 700, 100, 200, 300]},
    {"repo": "Cobol2XML", "commit_date": "2023-12-04", "commit_message": "Fixed parsing bug", "commit_author": "julianbass", "file_sizes": [600, 250, 400]},
    {"repo": "Dubbo", "commit_date": "2023-12-05", "commit_message": "Added new API endpoints", "commit_author": "janedoe", "file_sizes": [800, 1000, 600]},
]

# 1. Commits Per Repository
def commits_per_repo():
    repo_counts = {}
    for commit in commit_history:
        repo_counts[commit["repo"]] = repo_counts.get(commit["repo"], 0) + 1
    repos = list(repo_counts.keys())
    counts = list(repo_counts.values())
    
    # Create a bar chart
    fig = go.Figure(data=[go.Bar(x=repos, y=counts)])
    fig.update_layout(title="Commits per Repository", xaxis_title="Repository", yaxis_title="Number of Commits")
    
    # Convert to HTML
    return pio.to_html(fig, full_html=True)

# 2. Commits By Author

#Generate plots from commit counts by author
def generate_plots(data):

    # Create raw plots used to generate a pie chart
    fig = px.pie(
        data_frame=data,
        names="author",  # Use 'author' as the label
        values="commit_count",  # Use 'count' as the value
        title="Author Commit Distribution"
    )

    return fig.to_json()


# 3. Commits Heatmap
def commits_heatmap():
    repo_names = list(set(commit["repo"] for commit in commit_history))
    commit_dates = list(set(commit["commit_date"] for commit in commit_history))
    heatmap_data = []
    for repo in repo_names:
        row = []
        for date in commit_dates:
            count = sum(1 for commit in commit_history if commit["repo"] == repo and commit["commit_date"] == date)
            row.append(count)
        heatmap_data.append(row)
    
    # Create a heatmap
    fig = px.imshow(
        heatmap_data,
        x=commit_dates,
        y=repo_names,
        labels=dict(x="Commit Date", y="Repository", color="Number of Commits"),
        color_continuous_scale="Viridis",
        title="Commits Over Time by Repository"
    )
    return pio.to_html(fig, full_html=True)

def generate_histogrammm(data):
    # Check if data contains the required fields
    # if "Date" not in data or "Commits" not in data:
    #     raise ValueError("Data must contain 'Date' and 'Commits' fields")

    # # Ensure data has values for x and y axes
    # if not data["Date"] or not data["Commits"]:
    #     raise ValueError("Date and Commits arrays must not be empty")

    # Create the histogram
    fig = px.histogram(
        data_frame=data,
        x="Date",               # x-axis: dates (will be automatically binned)
        y="Commits",            # y-axis: aggregate commit counts
        title="Commits Histogram",
        histfunc="sum"          # Sum the commits for each bin
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Date",          # X-axis label
        yaxis_title="Number of Commits",  # Y-axis label
        bargap=0.1,                 # Reduce gap between bars
    )

    # Return the figure as JSON for the frontend
    return fig.to_json()



# 4. Commits Histogram
def generate_histogram(histogram_type, repo_name=None):
    if histogram_type == "commits":
        # Commits Histogram
        dates = [["commit_date"] for commit in commit_history]
        fig = go.Figure(data=[go.Histogram(x=dates)])
        fig.update_layout(
            title="Commits by Day",
            xaxis_title="Date",
            yaxis_title="Number of Commits"
        )
    elif histogram_type == "file_sizes":
        # File Size Histogram
        if not repo_name:
            return "<h1>Error: 'repo_name' is required for file size histogram</h1>"
        repo_data = next((repo for repo in commit_history if repo["repo"] == repo_name), None)
        if not repo_data:
            return f"<h1>Repository '{repo_name}' not found</h1>"
        file_sizes = repo_data["file_sizes"]
        fig = go.Figure(data=[go.Histogram(x=file_sizes, nbinsx=10)])
        fig.update_layout(
            title=f"File Size Distribution in {repo_name}",
            xaxis_title="File Size (KB)",
            yaxis_title="Number of Files"
        )
    else:
        return "<h1>Error: Invalid histogram type. Use 'commits' or 'file_sizes'.</h1>"

    # Convert the figure to HTML
    return pio.to_html(fig, full_html=True)






def generate_barPlots(data):

    # Create raw plots used to generate a pie chart
    fig = px.bar(
        data_frame=data,
        x="Name",  # Column for the x-axis (repository name)
        y="LineCount",  # Column for the y-axis (line count)
        title="Line Count by repo name"
    )

    return fig.to_json()