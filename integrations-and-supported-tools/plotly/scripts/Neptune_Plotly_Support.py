# Import necessary libraries
import neptune
import plotly.express as px

# Initialize Neptune and create a new run
run = neptune.init_run(api_token=neptune.ANONYMOUS_API_TOKEN, project="common/plotly-support")

# Create a sample chart
df = px.data.iris()
plotly_fig = px.scatter_3d(df, x="sepal_length", y="sepal_width", z="petal_width", color="species")

# Log interactive image to Neptune
run["interactive_img"].upload(plotly_fig)

# Tracking will stop automatically once script execution is complete
