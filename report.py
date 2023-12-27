import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



def create_radar_chart():
    # Sample data
    data = {
        "fullName": [
            "Yiğit Ağalar", "Vorn", "Umut Arısoy", "Özgür Tellal", "Özgür Tellal", 
            "Ozgur Tellal", "Ozgur Tellal", "ozgur tellal", "ozgur tellal", "Emin Uzer",
            "Yiğit Ağalar", "Vorn", "Özgür Tellal", "Ozgur Tellal",
        ],
        "name": [
            "Review", "Review", "Review", "Planning", "Review",
            "Planning", "Review", "Planning", "Review", "Planning",
            "Design", "Design", "Design", "Design",
        ],
        "total_given": [
            1, 1, 3, 3, 5, 3, 10, 3, 4, 3, 2, 4, 3, 5,
        ],
        "total_completed": [
            1, 0, 0, 0, 1, 0, 6, 0, 2, 0, 2, 3, 2, 4,
        ],
        "completion_rate": [
            100.0, 60.0, 60.0, 60.0, 60.0, 60.0, 40.0, 40.0, 60.0, 40.0,
            100.0, 100.0, 100, 80.0,
        ]
    }

    df = pd.DataFrame(data)

    # Selecting a specific individual from the data provided
    selected_individual = "Özgür Tellal"

    # Filtering the data for the selected individual
    individual_data = df[df['fullName'] == selected_individual]

    # Grouping by event type ('name') and calculating mean for only numeric columns
    numeric_cols = ['total_given', 'total_completed', 'completion_rate']
    grouped_data = individual_data.groupby('name')[numeric_cols].mean().reset_index()

    # Creating the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=grouped_data['completion_rate'],
        theta=grouped_data['name'],
        fill='toself',
        name='Completion Rate'
    ))

    # Updating layout with dynamic title
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"Performance of {selected_individual} on Different Events"
    )

    return fig



st.set_page_config(layout='wide')
@st.cache_resource
def load_data():
    advice_comp_rate = pd.read_csv('reports/people/advice_completion_rate.csv')
    average_quiz_score = pd.read_csv('reports/people/average_quiz_score.csv')
    event_competion_rate = pd.read_csv('reports/people/event_completion_rate.csv')


    return advice_comp_rate, average_quiz_score, event_competion_rate

advice_comp_rate, average_quiz_score, event_competion_rate = load_data()

st.title('Overall People Completion Rate')


# Creating the bar chart using Plotly
avg_complete_fig = go.Figure(data=[
    go.Bar(name='Completion Rate', x=advice_comp_rate['fullName'], y=advice_comp_rate['completion_rate'])
])

# Update layout
avg_complete_fig.update_layout(
    title='Advice Completion Rate',
    xaxis=dict(title='Full Name'),
    yaxis=dict(title='Completion Rate (%)'),
    legend=dict(x=0.01, y=0.99),
    legend_title_text='Legend',
    font=dict(size=14)
)

st.plotly_chart(avg_complete_fig,use_container_width=True)


# Creating the bar chart using Plotly
avg_quiz_fig = go.Figure(data=[
    go.Bar(name='Quiz Score', x=average_quiz_score['fullName'], y=average_quiz_score['avg_success_score'])
])

# Update layout
avg_quiz_fig.update_layout(
    title='Average Quiz Score',
    xaxis=dict(title='Full Name'),
    yaxis=dict(title='Average Quiz Score'),
    legend=dict(x=0.01, y=0.99),
    legend_title_text='Legend',
    font=dict(size=14)
)

# Show the figure
st.plotly_chart(avg_quiz_fig,use_container_width=True)

st.header("EXAMPLE")
example_radar_chart = create_radar_chart()
st.plotly_chart(example_radar_chart,use_container_width=True)
