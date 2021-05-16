import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Load data into cache for speed/cost pruposes
@st.cache
def get_data():
    path = "df_streamlit.csv"
    return pd.read_csv(path)
df = get_data()

#Introduce the dashboard
st.header("Productivity Dashboard")
st.subheader("Productivity charts, filters by department and team")
st.markdown("Garment manufacturing means sewing, cutting, making, processing, repairing, finishing, assembling, or otherwise preparing any garment or any article of wearing apparel or accessories designed or intended to be worn by any individual, including, but not limited to, clothing, hats, gloves, handbags, hosiery, ties, scarfs, and belts, for sale or resale by any person or any persons contracting to have those operations performed and other operations and practices in the apparel industry as may be identified in regulations of the Department of Industrial Relations consistent with the purposes of this part.")


#Put a header in Sidebar
st.sidebar.header('Display productivity by department')

#Put a selectbox in Sidebar
department = st.sidebar.selectbox("Select a department", df.department.unique())

#Adapt output, regarding Sidebar's Selectbox
if department=='sewing':
    df_sewing = df[df['department'] == 'sewing']
    teams = df_sewing[['team', 'actual_productivity']].groupby('team').mean()
    teams = teams.sort_values('actual_productivity', ascending=False).reset_index()
    figs1 = px.bar(teams, x="team"
                 , y="actual_productivity"
                # , color='actual_productivity'
                 , template='plotly_dark')

    figs2 = px.histogram(df_sewing, x="date"
                    , y="actual_productivity"
                    , color='team'
                    , template="plotly_dark")

    figs1.update_layout(title='AVG Team Productivity (Sewing dep)', title_x=0.5)
    figs2.update_layout(title='Productivity by Teams', title_x=0.5)
    st.plotly_chart(figs1)
    st.plotly_chart(figs2)

    team_s = st.sidebar.selectbox("Choose a team", df.team.unique())

    st.header('Display data by teams')
    st.markdown("Now we have seen the average team productivity by department and teams' productivity evolution overtime, let's isolate each team to see how well they manage to fit to their targeted productivity.")
    if team_s >= 1:
        df_team_s = df_sewing[df_sewing['team'] == team_s]

        # If the condition is respected, then display Actual productivit Vs Time
        figt1 = px.line(df_team_s, x="date"
                        , y="actual_productivity"
                        , template="plotly_dark")

        # Add a second line : Targeted Productivity Vs Time
        figt1.add_scatter(x=df_team_s['date']
                          , y=df_team_s['targeted_productivity']
                          , mode='lines'
                          , name='targeted productivity')

        # Update Charts' Layout
        figt1.update_layout(title='Actual Vs Targeted Productivity', title_x=0.5)

        # Display chart with plotly
        st.plotly_chart(figt1)

#Adapt output, regarding Sidebar's Selectbox (Team)
if department=='finishing':
    df_finishing = df[df['department'] == 'finishing']
    teamf = df_finishing[['date','team', 'actual_productivity']].groupby('team').mean()
    teamf = teamf.sort_values('actual_productivity', ascending=False).reset_index()
    figf1 = px.bar(teamf, x="team"
                 , y="actual_productivity"
                 #, color='actual_productivity'
                 , template='plotly_dark')

    figf2 = px.histogram(df_finishing, x="date"
                    , y="actual_productivity"
                    , color='team'
                    , template="plotly_dark")

    figf1.update_layout(title='AVG Team Productivity (Finishing dep)', title_x=0.5)
    figf2.update_layout(title='Productivity by Teams', title_x=0.5)

    st.plotly_chart(figf1)
    st.plotly_chart(figf2)

    team_f = st.sidebar.selectbox("Choose a team", df.team.unique())

    st.header('Display data by teams')
    st.markdown("Now we have seen the average team productivity by department and teams' productivity evolution overtime, let's isolate each team to see how well they manage to fit to their targeted productivity.")

    # Adapt output, regarding Sidebar's Selectbox (Team)
    if team_f >= 1:
        df_team_f = df_finishing[df_finishing['team'] == team_f]

        # If the condition is respected, then display Actual productivity Vs Time
        figt1 = px.line(df_team_f, x="date"
                        , y="actual_productivity"
                        , template="plotly_dark")

        # Add a second line : Targeted Productivity Vs Time
        figt1.add_scatter(x=df_team_f['date']
                          , y=df_team_f['targeted_productivity']
                          , mode='lines'
                          , name='targeted productivity')

        # Update Charts' Layout
        figt1.update_layout(title='Actual Vs Targeted Productivity', title_x=0.5)

        # Display chart with plotly
        st.plotly_chart(figt1)

checkbox = st.checkbox('Display Raw Data')

if checkbox:
    st.dataframe(df)
