import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



def create_radar_chart():
    # Sample data
    data = {
        "userId": [
            # Existing data
            "22078751-34f0-4ed5-806f-78b5e36b4f35", "a920844e-c0a0-4073-963d-311ed32cbda5",
            "c2d14093-e4c1-4d28-a9dc-9d9c3470dcf2", "e3d2c650-ec45-40f0-83f7-05159519c2fc",
            "e3d2c650-ec45-40f0-83f7-05159519c2fc", "8793280a-4391-407d-971d-fed93d99205c",
            "8793280a-4391-407d-971d-fed93d99205c", "59e51cd4-40d9-4856-bbb6-2d740d510df8",
            "59e51cd4-40d9-4856-bbb6-2d740d510df8", "f987c2cc-3cab-4610-b2df-afc30e43b02c",
            # New data
            "22078751-34f0-4ed5-806f-78b5e36b4f35", "a920844e-c0a0-4073-963d-311ed32cbda5",
            "e3d2c650-ec45-40f0-83f7-05159519c2fc", "8793280a-4391-407d-971d-fed93d99205c",
        ],
        "fullName": [
            # Existing data
            "Yiğit Ağalar", "Vorn", "Umut Arısoy", "Özgür Tellal", "Özgür Tellal", 
            "Ozgur Tellal", "Ozgur Tellal", "ozgur tellal", "ozgur tellal", "Emin Uzer",
            # New data
            "Yiğit Ağalar", "Vorn", "Özgür Tellal", "Ozgur Tellal",
        ],
        "name": [
            # Existing data
            "Review", "Review", "Review", "Planning", "Review",
            "Planning", "Review", "Planning", "Review", "Planning",
            # New data
            "Design", "Design", "Design", "Design",
        ],
        "total_given": [
            # Existing data
            1, 1, 3, 3, 5, 3, 10, 3, 4, 3,
            # New data
            2, 4, 3, 5,
        ],
        "total_completed": [
            # Existing data
            1, 0, 0, 0, 1, 0, 6, 0, 2, 0,
            # New data
            2, 3, 2, 4,
        ],
        "completion_rate": [
            # Existing data
            100.0, 60.0, 60.0, 60.0, 60.0, 60.0, 40.0, 40.0, 60.0, 40.0,
            # New data
            100.0,100.0, 100, 80.0,
        ]
    }


    df = pd.DataFrame(data)

    # Selecting a specific individual from the data providedÜ
    selected_individual = "Özgür Tellal"

    # Filtering the data for the selected individual
    individual_data = df[df['fullName'] == selected_individual]

    # Grouping by event type ('name') and calculating mean completion rate
    grouped_data = individual_data.groupby('name').mean().reset_index()

    # Creating the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=grouped_data['completion_rate'],
        theta=grouped_data['name'],
        fill='toself',
        name='Completion Rate'
    ))

    #fig.add_trace(go.Scatterpolar(
    #    r=grouped_data['total_completed'],
    #    theta=grouped_data['name'],
    #    fill='toself',
    #    name='Completed'
    #))


    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]

            )),
            
        title=f"Performance of {selected_individual} on Different Events",
        showlegend=True,

    )

    # Note: Due to the execution environment limitations, the plot may not be displayed here. 
    # Please run this code in your local Python environment to view the plot.
    return fig


def main():

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

if __name__ == "__main__":
    main()