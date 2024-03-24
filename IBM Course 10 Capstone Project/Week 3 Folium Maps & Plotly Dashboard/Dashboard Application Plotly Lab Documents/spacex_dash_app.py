# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
launch_sites_custom = []
launch_sites_custom.append({'label': 'All Locations', 'value': 'All Locations'})
for item in spacex_df["Launch Site"].value_counts().index:
    launch_sites_custom.append({'label': item, 'value': item})

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                # Create the dropdown menu options
                                dcc.Dropdown(id='site-dropdown', options=launch_sites_custom, value='All Locations', placeholder="Select a Location here", searchable=True), 
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        1000: '1000',
                                                        2000: '2000',
                                                        3000: '3000',
                                                        4000: '4000',
                                                        5000: '5000',
                                                        6000: '6000',
                                                        7000: '7000',
                                                        8000: '8000',
                                                        9000: '9000',
                                                        10000: '10000'},
                                                value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site_custom):
    if selected_site_custom == 'All Locations':
        pie_fig_custom = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches for All Locations')
    else:
        filtered_df_custom = spacex_df[spacex_df['Launch Site'] == selected_site_custom]
        pie_fig_custom = px.pie(filtered_df_custom, names='class', title=f'Success vs Failed launches for {selected_site_custom}')
    return pie_fig_custom


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site_custom, payload_range_custom):
    if selected_site_custom == 'All Locations':
        filtered_df_custom = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range_custom[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range_custom[1])]
        scatter_fig_custom = px.scatter(filtered_df_custom, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                 title='Payload vs Launch Success for All Locations')
    else:
        filtered_df_custom = spacex_df[(spacex_df['Launch Site'] == selected_site_custom) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range_custom[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range_custom[1])]
        scatter_fig_custom = px.scatter(filtered_df_custom, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                 title=f'Payload vs Launch Success for {selected_site_custom}')
    return scatter_fig_custom


# Run the app
if __name__ == '__main__':
    app.run_server()
