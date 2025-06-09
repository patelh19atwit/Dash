import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
df = pd.read_csv('AirQuality2005_2011.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Air Quality Dashboard", style={'textAlign': 'center'}),

    html.Label("Select County:"),
    dcc.Dropdown(
        id='county-dropdown',
        options=[{'label': c, 'value': c} for c in df['County'].unique()] if not df.empty else [],
        value=df['County'].iloc[0] if not df.empty else None
    ),

    html.Br(),

    html.Div([
        dcc.Graph(id='concentration-bar')
    ])
])

# Callbacks
@app.callback(
    Output('concentration-bar', 'figure'),
    [Input('county-dropdown', 'value')]
)
def update_graphs(selected_county):
    if df.empty or selected_county is None:
        # Return empty figure if no data
        empty_fig = px.bar(title="No data available")
        return empty_fig
    
    # Filter data by selected county
    filtered_df = df[df['County'] == selected_county]
    
    if filtered_df.empty:
        empty_fig = px.bar(title=f"No data available for {selected_county}")
        return empty_fig

    # Bar chart: Average concentration by year
    # Group by year
    yearly_avg = filtered_df.groupby('Year')['Concentration'].mean().reset_index()
    
    fig = px.bar(
        yearly_avg,
        x='Year',
        y='Concentration',
        title=f"Average Air Quality Concentration by Year in {selected_county}",
        labels={
            'Year': 'Year',
            'Concentration': 'Concentration (µg/m³)'
        },
        color='Concentration',
        color_continuous_scale='Viridis'
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        showlegend=False
    )

    return fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)