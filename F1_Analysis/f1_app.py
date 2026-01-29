"""Streamlit app for F1 analysis.

This file defines the Streamlit UI and loads helper functions
from `src` to provide interactive visualizations for Teams,
Drivers and Decades.
"""

import streamlit as st
from src.teams import *
from src.drivers import *
from src.decades import *
import plotly.express as px


teams_tab, drivers_tab, decades_tab = st.tabs(["Teams", "Drivers", "Decades"])


# Teams tab UI
with teams_tab:
    
    @st.cache_data
    def load_teams():
        df = get_pos_by_year_teams()
        return df
    
    @st.cache_data
    def load_teams_avgs():
        df = get_avg_pos_by_team()
        return df
    
    @st.cache_data
    def load_teams_dnfs():
        df = get_counts_DNFs_byTeam()
        return df
    
    @st.cache_data
    def load_teams_pit_stops():
        df = get_pit_stops()
        return df
    
    @st.cache_data
    def load_wins_by_prix():
        df = get_wins_by_prix()
        return df

    df_teams = load_teams()
    df_avgs = load_teams_avgs()
    df_dnfs = load_teams_dnfs()
    df_pit_stops = load_teams_pit_stops()
    df_wins_prix = load_wins_by_prix()
    
    
    st.title("Teams Section")
    team = st.multiselect("Teams", df_teams["Team"].sort_values(ascending=True).unique(), default="Ferrari")
    
    filtered = df_teams[df_teams["Team"].isin(team)]
    filtered_avgs = df_avgs[df_avgs["Team"].isin(team)]
    filtered_dnfs = df_dnfs[df_dnfs["Team"].isin(team)]
    filtered_stops = df_pit_stops[df_pit_stops["Team"].isin(team)]
    filtered_wins_prix = df_wins_prix[df_wins_prix["Team"].isin(team)]
    
    titles = filtered["Standing"][filtered["Standing"]==1].count()
    points = f"{filtered['Total_points'].sum():,}"
    races = filtered_avgs["Amount_of_Races"]
    avg_pos = filtered_avgs["AvgPos"]
    
    st.header("Historically", text_alignment="center")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Titles", titles)
    col2.metric("Points", points)
    col3.metric("Races", races)
    col4.metric("Average Position", avg_pos)
    
    chart_df = (
        filtered.groupby(["Anio", "Team"], as_index=False)["Total_points"].sum()
    )

    st.line_chart(chart_df, x="Anio", y="Total_points", x_label="Year", y_label="Points")
    
    st.divider()
    
    st.header("Top 5 causes of DNF", text_alignment="center")
    
    df_chart_dnfs = filtered_dnfs.groupby(["Team", "Status"], as_index=False)["dnf_counts"].sum().sort_values(by='dnf_counts', ascending=False).head(5)
    st.bar_chart(df_chart_dnfs, x="Status", y="dnf_counts", x_label="Count", y_label="Cause", horizontal=True, sort="dnf_counts")
    
    points2 = filtered['Total_points'].max()
    year = filtered["Anio"][filtered["Total_points"] == points2]
    pos = filtered["Standing"][filtered["Total_points"] == points2]
    wins = filtered["Total_wins"][filtered["Total_points"] == points2]
    podiums = filtered["podiums"][filtered["Total_points"] == points2]
    
    st.divider()
    
    st.header("Best year", text_alignment="center")
    
    col5, col6, col7, col8, col9 = st.columns(5)
    col5.metric("Year", year)
    col6.metric("Position", pos)
    col7.metric("Points", points2)
    col8.metric("Wins", wins)
    col9.metric("Podiums", podiums)
    
    st.divider()
    
    st.header("Top 15 avg of pit stop duration by circuit", text_alignment="center")
    
    df_stops = filtered_stops.groupby(["Race", "Team"], as_index=False)["Duration_ms"].mean().sort_values(by="Duration_ms")
    st.bar_chart(df_stops.head(15), x="Race", y="Duration_ms", x_label="Duration (s)", y_label="Circuit", horizontal=True)
    
    st.divider()
    
    st.header("Historical Win Distribution Top 10", text_alignment='center')
    
    fig_ = px.bar(
        filtered_wins_prix.head(10), 
        x="Wins", 
        y="Grand_Prix",
        orientation='h',
        title="Top 10 Circuits by its Wins",
    )
    st.plotly_chart(fig_, width='stretch')
    
    st.subheader(f"Most Successful Circuit: {filtered_wins_prix["Grand_Prix"].iloc[0]}", text_alignment='center')
    
    col14, col15 = st.columns(2)

    col14.metric("Wins", int(filtered_wins_prix["Wins"].iloc[0]))
    col15.metric("Races", filtered_wins_prix["Total_races"].iloc[0])
    
    st.divider()
    
    st.header("Download CSV", text_alignment="center")
    
    csv1 = filtered.to_csv(index=False).encode('utf-8')
    csv2 = df_avgs.to_csv(index=False).encode('utf-8')
    csv3 = filtered_dnfs.to_csv(index=False).encode('utf-8')
    csv4 = filtered_stops.to_csv(index=False).encode('utf-8')
    csv5 = filtered_wins_prix.to_csv(index=False).encode('utf-8')
    
    col10, col11, col12, col13, col16 = st.columns(5)
    
    col10.dataframe(filtered)
    col10.download_button("Download Yearly Standings", csv1, "yearly_standings.csv", "text/csv")
    
    col11.dataframe(df_avgs)
    col11.download_button("Download Historical Avgs", csv2, "historical_avgs.csv", "text/csv")
    
    col12.dataframe(filtered_dnfs)
    col12.download_button("Download Historical DNFs Causes", csv3, "historical_dnfs_causes.csv", "text/csv")
    
    col13.dataframe(filtered_stops)
    col13.download_button("Download Historical Pit Stops Duration", csv4, "historical_stops_durations.csv", "text/csv") 
    
    col16.dataframe(filtered_wins_prix)
    col16.download_button("Download Historical Wins by Prix", csv4, "historical_wins_by_prix.csv", "text/csv")  
    
# Drivers tab UI
with drivers_tab:
    st.title("Drivers Section")
    
    @st.cache_data
    def load_drivers_avg():
        df = get_avg_pos_by_driver()
        return df
    
    @st.cache_data
    def load_drivers_wins_points_laps():
        df = get_wins_points_by_driver()
        return df
    
    @st.cache_data
    def load_drivers_standings():
        df = get_pos_by_year()
        return df
    
    @st.cache_data
    def load_podium_streaks():
        df = get_podium_streaks()
        return df
    
    @st.cache_data
    def load_points_by_circuit():
        df = get_points_races_by_circuit()
        return df
    
    
    df_drivers_avgs = load_drivers_avg()
    df_drivers_standings = load_drivers_standings()
    df_drivers_points_laps = load_drivers_wins_points_laps()
    df_drivers_streaks = load_podium_streaks()
    df_drivers_points_circuits = load_points_by_circuit()
    
    driver = st.multiselect("Drivers", df_drivers_avgs["Driver"].sort_values(ascending=True).unique(), default="Lewis Hamilton")
    
    df_filtered = df_drivers_points_laps[df_drivers_points_laps["Driver"].isin(driver)]
    df_filtered_standings = df_drivers_standings[df_drivers_standings["Driver"].isin(driver)]
    df_drivers_avg_filtered = df_drivers_avgs[df_drivers_avgs["Driver"].isin(driver)]
    df_drivers_circuits_filtered = df_drivers_points_circuits[df_drivers_points_circuits["Driver"].isin(driver)]
    df_streaks_filtered = df_drivers_streaks[df_drivers_streaks["Driver"].isin(driver)]
    
    st.header("Historically", text_alignment="center")
    
    points_drivers, titles_drivers, races_drivers, laps_drivers, wins_drivers, avg_pos_metric = st.columns(6)
    
    points_ = df_filtered['Total_Points']
    titles_ = df_filtered_standings["Standings"][df_filtered_standings["Standings"]==1].count()
    races_ = df_drivers_avg_filtered["Amount_of_Races"]
    laps_ = df_filtered["Amount_of_Laps"]
    wins_ = df_filtered["Wins"]
    pos_ = df_drivers_avg_filtered["AvgPos"]
    
    
    points_drivers.metric("Points", int(points_.iloc[0]))
    titles_drivers.metric("Titles", titles_)
    races_drivers.metric("Races", races_)
    laps_drivers.metric("Laps", int(laps_.iloc[0]))
    wins_drivers.metric("Wins", int(wins_.iloc[0]))
    avg_pos_metric.metric("Avg Pos", pos_)
    
    st.line_chart(df_filtered_standings, x="Anio", y="Total_points", x_label="Year", y_label="Points")
    
    st.divider()
    
    st.header("Points by circuit", text_alignment="center")
    
    most_points = df_drivers_circuits_filtered["Total_Points"].max()
    circuit = df_drivers_circuits_filtered["Grand_Prix"][df_drivers_circuits_filtered["Total_Points"]==most_points]
    times_raced = df_drivers_circuits_filtered["Total_Races"][df_drivers_circuits_filtered["Total_Points"]==most_points]
    avgpos_circuit = df_drivers_circuits_filtered["Avgpos"][df_drivers_circuits_filtered["Total_Points"]==most_points]
    wons = df_drivers_circuits_filtered["Wins"][df_drivers_circuits_filtered["Total_Points"]==most_points]
    
    st.subheader(f"Dominant Circuit: {circuit.iloc[0]}", text_alignment="center")
    
    total_points, times, avgposition, r_won = st.columns(4)
    
    total_points.metric("Points", int(most_points))
    times.metric("Total Races", times_raced)
    avgposition.metric("Avg Position", int(avgpos_circuit.iloc[0]))
    r_won.metric("Wins", int(wons.iloc[0]))
    
    df_chart_drivers = df_drivers_circuits_filtered.groupby(["Driver", "Grand_Prix"], as_index=False)["Total_Points"].mean().sort_values(by="Total_Points", ascending=True).reset_index(drop=True)
    figura = px.bar(data_frame=df_chart_drivers.tail(10), x="Total_Points", y="Grand_Prix", orientation="h", color_discrete_sequence=["lightblue"])
    st.plotly_chart(figure_or_data=figura, width="stretch")
    
    st.divider()
    
    st.header("Best Year", text_alignment="center")
    
    puntos_year = df_filtered_standings["Total_points"].max()
    anio = df_filtered_standings["Anio"][df_filtered_standings["Total_points"]==puntos_year]
    vic = df_filtered_standings["Total_wins"][df_filtered_standings["Total_points"]==puntos_year]
    pct = df_filtered_standings["pctWin"][df_filtered_standings["Total_points"]==puntos_year]
    stan = df_filtered_standings["Standings"][df_filtered_standings["Total_points"]==puntos_year]
    
    puntosm, aniom, vicm, pctm, stanm = st.columns(5)
    
    aniom.metric("Year", anio)
    puntosm.metric("Points", puntos_year)
    vicm.metric("Wins", vic)
    pctm.metric("Pct of Win", pct)
    stanm.metric("Position", stan)
    
    st.divider()
    
    
    
    st.header("Podium Streaks", text_alignment="center")

    st.subheader("Podium Streaks vs. Total Wins", text_alignment="center")


    fig = px.bar(
        df_streaks_filtered, 
        x=["podium_streak", "total_wins"], 
        y="Period", 
        barmode="group",
        title="Domain Analysis by Period",
        labels={"value": "Amount", "variable": "Metric", "Period": "Period"},
        color_discrete_map={
            "podium_streak": "#00E1FF",
            "total_wins": "#FFFFFF"
        },
    )
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Largest Streak", text_alignment="center")
    
    l_period, l_streak, l_wins = st.columns(3, gap='xlarge')
    
    l_period.metric("Period", df_streaks_filtered["Period"].iloc[0], width=600)
    l_streak.metric("Podiums", df_streaks_filtered["podium_streak"].iloc[0], width=600)
    l_wins.metric("Wins", int(df_streaks_filtered["total_wins"].iloc[0]), width=600)
    
    st.divider()
    
    st.header("Download CSV", text_alignment="center")
    
    df1, df2, df3, df4, df5 = st.columns(5)
    
    csv1_ = df_drivers_avgs.to_csv(index=False).encode('utf-8')
    csv2_ = df_drivers_standings.to_csv(index=False).encode('utf-8')
    csv3_ = df_drivers_points_laps.to_csv(index=False).encode('utf-8')
    csv4_ = df_drivers_streaks.to_csv(index=False).encode('utf-8')
    csv5_ = df_drivers_points_circuits.to_csv(index=False).encode('utf-8')
    
    df1.dataframe(df_drivers_avgs)
    df1.download_button("Download Drivers Avgs", csv1_, "drivers_avgs.csv", "text/csv")
    
    df2.dataframe(df_drivers_standings)
    df2.download_button("Download Drivers Standings", csv2_, "drivers_standigs.csv", "text/csv")
    
    df3.dataframe(df_drivers_points_laps)
    df3.download_button("Download Drivers Historical Info", csv3_, "drivers_historical.csv", "text/csv")
    
    df4.dataframe(df_drivers_streaks)
    df4.download_button("Download Drivers Podium Streaks", csv4_, "drivers_streaks.csv", "text/csv")
    
    df5.dataframe(df_drivers_points_circuits)
    df5.download_button("Download Drivers Points by Circuit", csv5_, "drivers_points_circuits.csv", "text/csv")
    
# Decades tab UI
with decades_tab:
    st.title("Decades Section")
    
    @st.cache_data
    def load_ranking_drivers_decade():
        df = get_top_drivers_by_decade()
        return df
    
    @st.cache_data
    def load_best_driver_by_decade():
        df = get_bestdriver_by_decade()
        return df
    
    @st.cache_data
    def load_best_team_decade():
        df = get_best_teamby_decade()
        return df
    
    
    df_drivers_decade = load_ranking_drivers_decade()
    df_best_driver_decade = load_best_driver_by_decade()
    df_best_team_decade = load_best_team_decade()
    
    decade = st.selectbox("Decade", options=df_drivers_decade["Decade"].sort_values(ascending=True).unique(), index=0)
    
    filtered_drivers_decade = df_drivers_decade[df_drivers_decade["Decade"]==decade]
    filtered_best_team = df_best_team_decade[df_best_team_decade["Decade"]==decade]
    
    st.header("Best Drivers", text_alignment='center')
    st.subheader(f"King of the Decade: {filtered_drivers_decade["Driver"].iloc[0]}", text_alignment='center')
    
    d2, d3, d4, d5 = st.columns(4)

    d2_d = int(filtered_drivers_decade["Total_Points"].iloc[0])
    d3_d = int(filtered_drivers_decade["Wins"].iloc[0])
    d4_d = filtered_drivers_decade["Total_Races"].iloc[0]
    d5_d = filtered_drivers_decade["Pct_of_Wins"].iloc[0]
   
    d2.metric("Points", d2_d)
    d3.metric("wins", d3_d)
    d4.metric("Races", d4_d)
    d5.metric("Pct of Win", d5_d)
    
    df_drivers_chart = filtered_drivers_decade.sort_values(by="Total_Points", ascending=True)
    
    fig_d = px.bar(
        data_frame=df_drivers_chart.tail(10), 
        x="Total_Points", 
        y="Driver",
        orientation='h',
        labels={"Total_Points": "Points", "Driver": "Driver"},
        title="Drivers' Ranking by Decade",
        color_discrete_sequence=["lightblue"],
    )
    st.plotly_chart(fig_d, width='stretch')
    
    
    st.divider()
    
    st.header("Best Teams", text_alignment='center')
    st.subheader(f"Decade's Winningest Team: {filtered_best_team["Team"].iloc[0]}", text_alignment='center')
    
    d6, d7, d8, d9 = st.columns(4)
    
    d6_d = int(filtered_best_team["Total_Points"].iloc[0])
    d7_d = int(filtered_best_team["Wins"].iloc[0])
    d8_d = filtered_best_team["Total_Races"].iloc[0]
    d9_d = filtered_best_team["Pct_of_Wins"].iloc[0]
    
    d6.metric("Points", d6_d)
    d7.metric("wins", d7_d)
    d8.metric("Races", d8_d)
    d9.metric("Pct of Win", d9_d)
    
    df_teams_chart = filtered_best_team.sort_values(by="Total_Points", ascending=True)
    fig_t = px.bar(
        data_frame=df_teams_chart.tail(10), 
        x="Total_Points", 
        y="Team",
        orientation='h',
        labels={"Total_Points": "Points", "Team": "Team"},
        title="Teams' Ranking by Decade",
        color_discrete_sequence=["lightblue"],
    )
    st.plotly_chart(fig_t, width='stretch')
    
    st.divider()
    
    st.header("Best Drivers by Decade", text_alignment='center')

    top_wins_row = df_best_driver_decade.loc[df_best_driver_decade['Wins'].idxmax()]
 
    top_races_row = df_best_driver_decade.loc[df_best_driver_decade['Total_Races'].idxmax()]

    top_pct_row = df_best_driver_decade.loc[df_best_driver_decade['Pct_of_Wins'].idxmax()]

    top_points_row = df_best_driver_decade.loc[df_best_driver_decade['Total_Points'].idxmax()]
    
    st.subheader("Era Leaders & Records", text_alignment='center')

    cl1, cl2 = st.columns(2)
    cl3, cl4 = st.columns(2)

    cl1.metric(
            label=f"Most Victories ({int(top_wins_row['Wins'])})", 
            value=f"{top_wins_row['Driver_Name']} {top_wins_row['Driver_Surname']}"
        )

    cl2.metric(
            label=f"Most Races ({int(top_races_row['Total_Races'])} GPs)", 
            value=f"{top_races_row['Driver_Name']} {top_races_row['Driver_Surname']}"
        )

    cl3.metric(
            label=f"Highest Win % ({top_pct_row['Pct_of_Wins']}%)", 
            value=f"{top_pct_row['Driver_Name']} {top_pct_row['Driver_Surname']}"
        )

    cl4.metric(
            label=f"Most Points ({int(top_points_row['Total_Points'])})", 
            value=f"{top_points_row['Driver_Name']} {top_points_row['Driver_Surname']}"
        )
        
    st.divider()
    
    st.subheader("Hall of Fame: Kings of Each Decade", text_alignment='center')
    
    df_display = df_best_driver_decade.rename(columns={
        'Decade': 'Decade',
        'Driver_Name': 'Name',
        'Driver_Surname': 'Surname',
        'Total_Points': 'Total Points',
        'Wins': 'Wins',
        'Total_Races': 'Races',
        'Pct_of_Wins': '% Wins'
    })

    
    df_display['Driver'] = df_display['Name'] + " " + df_display['Surname']

    df_final = df_display[['Decade', 'Driver', 'Wins', 'Races', '% Wins', 'Total Points']]

    st.dataframe(
        df_final,
        column_config={
            "Decade": st.column_config.NumberColumn(format="%d"),
            "% Wins": st.column_config.ProgressColumn(
                "Wins (%)",
                help="Percentage of wins out of total races",
                format="%.2f",
                min_value=0,
                max_value=100,
            ),
            "Wins": st.column_config.NumberColumn(
                "Wins",
                help="Total victories in the decade",
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.divider()
    
    st.header("Download CSV", text_alignment='center')
    
    ddf1, ddf2, ddf3 = st.columns(3)
    
    dcsv1_ = df_drivers_decade.to_csv(index=False).encode('utf-8')
    dcsv2_ = df_best_driver_decade.to_csv(index=False).encode('utf-8')
    dcsv3_ = df_best_team_decade.to_csv(index=False).encode('utf-8')
    
    ddf1.dataframe(df_drivers_decade)
    ddf1.download_button("Download Drivers Standings by Decade", csv1_, "drivers_standings_decade.csv", "text/csv")
    
    ddf2.dataframe(df_best_driver_decade)
    ddf2.download_button("Download Best Driver by Decade", csv2_, "best_driver_decade.csv", "text/csv")
    
    ddf3.dataframe(df_best_team_decade)
    ddf3.download_button("Download Teams Standings by Decade", csv3_, "teams_standings_decade.csv", "text/csv")
    