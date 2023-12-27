import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_resource
def load_data():
    team_competion_rate = pd.read_csv('reports/teams/team_completion_rate.csv')
    team_event_competion_rate = pd.read_csv('reports/teams/team_event_completion_rate.csv')
    team_spri_competion_rate = pd.read_csv('reports/teams/sprint_team_completion_rate.csv')


    return team_competion_rate, team_event_competion_rate, team_spri_competion_rate

team_competion_rate, team_event_competion_rate, team_spri_competion_rate = load_data()

st.title('Team Selection')
selected_team = st.selectbox('Select Team', team_competion_rate['name'].unique())
if selected_team:


    st.title('Team {}'.format(selected_team))


    given_col, completed_col, rate_col = st.columns(3)
    given_col.metric( "Given",f"{team_competion_rate[team_competion_rate['name'] == selected_team]['total_given'].values[0]}")
    completed_col.metric("Completed", f"{team_competion_rate[team_competion_rate['name'] == selected_team]['total_completed'].values[0]}")
    rate_col.metric("Completion Rate (%)",f"{team_competion_rate[team_competion_rate['name'] == selected_team]['completion_rate'].values[0].round(2)}")


    # Filter data for "oNabu"
    filtered_data_sprint = team_spri_competion_rate[team_spri_competion_rate["name"] == selected_team]

    # Create a Plotly line chart
    fig_sprint = px.line(filtered_data_sprint, x="name.1", y="completion_rate", title="Team Completion Rate", markers=True)

    # Update layout with width and height
    fig_sprint.update_layout(
        xaxis_title="Sprint",
        yaxis_title="Completion Rate (%)",
        legend_title="Legend",
        font=dict(size=12),
        width=1000,  # Width in pixels
        height=800   # Height in pixels
    )
    st.subheader("Team Sprint Completion Rate")
    st.plotly_chart(fig_sprint)

