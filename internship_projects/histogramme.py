import pandas as pd
import plotly.express as px

# Load data from CSV file
data = pd.read_csv('./application_export.csv')

# Extract the relevant columns
tmp_frame = data[['application', 'user_count']]

# Create a histogram
fig = px.histogram(tmp_frame, x='application', y='user_count', 
                   category_orders={'application': tmp_frame['application'].unique()})

# Add labels and title
fig.update_layout(
    title='Software Usage by Tonies',
    xaxis_title='Application',
    yaxis_title='User Count'
)

# Show the plot
fig.show()