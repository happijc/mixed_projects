import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to find the top 50 most used applications by the employees
def top_used_apps(data):
    # Filtering the dataframe to extract only necessary rows and columns
    tmp = data[data['user_count'] >= 200]
    new_frame = tmp[['application', 'user_count', 'created_at_utc']].nlargest(50, 'user_count')
    return new_frame

# Function to draw the pie chart
def drawing_stat(data):
    # Extracting the applications and user counts
    applications = data['application']
    user_counts = data['user_count']

    # Colors for the pie chart
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(data)))

    # Creating the pie chart
    fig, ax = plt.subplots()
    ax.pie(user_counts, labels=applications, colors=colors, startangle=140,
           autopct=lambda p: '{:.2f}'.format(p * sum(user_counts) / 100),
           wedgeprops={"linewidth": 1, "edgecolor": "white"})

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')
    plt.show()

def main():
    #CSV-File location in the repository
    x = './application_export.csv'
    
    # Load the CSV file
    data = pd.read_csv(x)   
    
    # Get the top used applications
    top_apps = top_used_apps(data)

    # Draw the pie chart
    drawing_stat(top_apps)
    
main()