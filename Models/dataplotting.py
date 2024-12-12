import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd

# Commits By Author Pie Chart Plots
def generate_plots_pie_chart(data):
    # Generate a pie chart showing the distribution of commits by author.
    fig = px.pie(
        data_frame=data,
        names="author",  # Use 'author' as the label for the pie slices.
        values="commit_count",  # Use 'commit_count' as the value for each slice.
        title="Author Commit Distribution"
    )
    return fig.to_json()  # Return the chart as JSON for rendering.

# Commits Histogram between date range plots
def generate_histogram_plots(data):
    # Create a histogram to display commits over a range of dates
    fig = px.histogram(
        data_frame=data,
        x="Date",                  # Dates on the x-axis
        y="Commits",               # Commit counts on the y-axis
        title="Commits Histogram",
        histfunc="sum"             # Aggregate commit counts
    )

    # Update layout to avoid automatic date binning
    fig.update_layout(
        xaxis=dict(
            title="Date",
            type="category"  # Treat each date group as a distinct category
        ),
        yaxis_title="Number of Commits",
        bargap=0.1  # Reduce gap between bars
    )

    return fig.to_json()  # Return the figure as JSON

# Bar chart plots showing line counts by repo name
def generate_bar_plots(data):
    # Create a bar chart to show the line counts by repository name
    fig = px.bar(
        data_frame=data,
        x="Name",  # Repository name on the x-axis
        y="LineCount",  # Line count on the y-axis
        title="Line Count by Repository Name"
    )
    return fig.to_json()  # Return the figure as JSON

# Bubble chart plots showing repository activity
def generate_bubble_chart_plots(data):
    if not data:
        raise ValueError("No data available for the bubble chart.")  # Handle empty data.

    # Extract data for the bubble chart
    repository_names = data["repository_name"]
    commit_counts = data["commit_count"]
    watcher_counts = data["watcher_count"]
    fork_counts = data["fork_count"]

    # Calculate bubble sizes based on fork counts, with a minimum size.
    min_size = 20
    scale_factor = 100 / max(fork_counts) if max(fork_counts) > 0 else 1  # Avoid divide by zero.
    fork_counts = [max(min_size, size * scale_factor) for size in fork_counts]

    # Create a scatter plot for the bubble chart.
    fig = px.scatter(
        x=watcher_counts,  # Watcher counts on the x-axis.
        y=commit_counts,  # Commit counts on the y-axis.
        size=fork_counts,  # Bubble size based on fork counts.
        text=repository_names,  # Repository names as text labels.
        labels={"x": "Number of Watchers", "y": "Number of Commits"},  # Axis labels.
        title="Commits vs. Watchers Bubble Chart",
    )
    fig.update_traces(textposition='top center')  # Adjust text position for readability.
    fig.update_layout(template="plotly_white")  # Apply a white template for the chart.
    return fig.to_json()  # Return the figure as JSON.

# Generates a pie chart showing commit contributions by each author.
def generate_author_plots(data):
    # Input:
    # - data (dict): Contains keys 'Author' and 'Commit Count'.
    # Output:
    # - Returns the pie chart as a JSON representation.
    fig = px.pie(
        values=data["Commit Count"],  # Commit counts for the pie slices.
        names=data["Author"],        # Author names as labels.
        title="Commit Contributions by Author"
    )
    return fig.to_json()

# Creates a bar chart to display file names and their corresponding line counts.
def generate_author_barchart_plots(data):
    # Input:
    # - data (dict): Contains "File Name" and "Line Count".
    # Output:
    # - Returns the bar chart as a JSON representation.
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["File Name"],       # File names on the x-axis.
            y=data["Line Count"],      # Line counts on the y-axis.
            marker_color="blue",       # Bar color.
            text=data["Line Count"],   # Display line counts on the bars.
            textposition="auto"        # Position text automatically.
        )
    )

    fig.update_layout(
        title="Line Count by File Name",  # Chart title.
        xaxis_title="File Name",          # Label for the x-axis.
        yaxis_title="Line Count",         # Label for the y-axis.
        template="plotly_white"           # Use a clean white template.
    )

    return fig.to_json()

# Generates a histogram showing commit counts over a period of time.
def generate_author_histogram_plots(data):
    # Input:
    # - data (dict): Contains "Commit Dates" and "Commit Counts".
    # Output:
    # - Returns the histogram as a JSON representation.
    fig = px.histogram(
        data_frame=data,
        x="Commit Dates",          # Dates for the x-axis bins.
        y="Commit Counts",         # Commit counts for the y-axis.
        title="Commits Over Time", # Chart title.
        labels={"Commit Dates": "Dates", "Commit Counts": "Number of Commits"}
    )
    return fig.to_json()

