import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

# Simulated commit data, will be replaced by database later
commit_history = [
    {"repo": "Cobol2XML", "commit_date": "2023-12-01", "commit_message": "Initial commit", "commit_author": "julianbass"}, 
    {"repo": "fhir-data-pipes", "commit_date": "2023-12-02", "commit_message": "Added feature for data transformation", "commit_author": "johndoe"}, 
    {"repo": "Dubbo", "commit_date": "2023-12-03", "commit_message": "Refactored utility classes", "commit_author": "janedoe"}, 
    {"repo": "Cobol2XML", "commit_date": "2023-12-04", "commit_message": "Fixed parsing bug", "commit_author": "julianbass"},
    {"repo": "Dubbo", "commit_date": "2023-12-05", "commit_message": "Added new API endpoints", "commit_author": "janedoe"}
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
def commits_by_author():
    authors = ["Author1", "Author2", "Author3"]
    commits = [10, 15, 5]

    # Create a pie chart
    fig = go.Figure(data=[go.Pie(labels=authors, values=commits)])
    return pio.to_html(fig, full_html=True)

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

# 4. Commits Histogram
def commits_histogram():
    dates = [commit["commit_date"] for commit in commit_history]

    # Create a histogram
    fig = go.Figure(data=[go.Histogram(x=dates)])
    fig.update_layout(title="Commits by Day", xaxis_title="Date", yaxis_title="Number of Commits")
    return pio.to_html(fig, full_html=True)




