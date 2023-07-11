import streamlit as st
import plotly.graph_objects as go

def pie_chart(labels, values):
    # Create pie chart figure
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Set layout options
    fig.update_layout(title='Total Time Distribution')

    # Render the chart using st.plotly_chart
    #st.plotly_chart(fig)
    return fig
