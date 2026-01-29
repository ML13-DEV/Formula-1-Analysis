"""Team- and pit-stop related queries for the F1 Analysis project.

Provides convenience functions that return pandas DataFrames
produced by executing SQL queries through the shared `engine`.
"""

import pandas as pd
from .db import engine
import datetime as dt

def get_pit_stops():
    """Return pit stop details for races.

    Output columns include `Year_race`, `Race`, `Driver`, `Team`,
    `Lap_Stop`, `Num_Stop`, `Duration_ms` (seconds), and `Finish_Pos`.
    The function also converts the milliseconds column to seconds.
    """
    query = """select r.year as Year_race, r.name as Race, d.driverId as Driver_Id, CONCAT(d.forename, " ", d.surname) as Driver, c.constructorId as Cons_Id, 
        c.name as Team, ps.lap as Lap_Stop,
        ps.stop as Num_Stop, ps.milliseconds as Duration_ms, r2.positionOrder as Finish_Pos
        from races r
        join pit_stops ps on r.raceId = ps.raceId 
        join drivers d on ps.driverId = d.driverId 
        join results r2 on d.driverId = r2.driverId and r.raceId = r2.raceId 
        join constructors c on r2.constructorId = c.constructorId;
    """
    df = pd.read_sql(query, engine)
    df["Duration_ms"] = pd.to_timedelta(df["Duration_ms"], unit='ms').dt.total_seconds()
    return df

def get_avg_pos_by_team():
    """Return average finish position by team and number of races.

    Columns: `Team`, `AvgPos`, `Amount_of_Races`.
    """
    query = """select c.name as Team, ROUND(AVG(r.positionOrder),2) as AvgPos, COUNT(*) as Amount_of_Races
                from results r
                join constructors c
                on r.constructorId = c.constructorId
                group by c.name
                order by AvgPos;
            """
    df = pd.read_sql(query, engine)
    return df

def get_counts_DNFs_byTeam():
    """Return top DNF causes per team per year (top 5 per team-year).

    Columns include `Year_race`, `Team`, `Status`, `dnf_counts`, `rank_dnfs`.
    """
    query = """with counts_of_dnfs as (
            select r2.year as Year_race, c.name as Team, s.status as Status, COUNT(r.statusId) as dnf_counts
            from results r
            join constructors c on r.constructorId = c.constructorId
            join status s on r.statusId = s.statusId
            join races r2 on r.raceId = r2.raceId
            where r.statusId > 1 and s.status not like "+%%"
            group by r2.year, c.constructorId, s.status
            ),
            ranked as (
                    select *, row_number() over (partition by Year_race, Team order by dnf_counts desc) as rank_dnfs
                    from counts_of_dnfs
                )
            select Year_race, Team, Status, dnf_counts, rank_dnfs from ranked
            where rank_dnfs <= 5
            order by Year_race, Team, rank_dnfs asc;
        """
    df = pd.read_sql(query, engine)
    return df

def get_pos_by_year_teams():
    """Return constructor standings per year including points and wins.

    Columns include `Anio`, `Team`, `Total_wins`, `Total_points`, `podiums`, `Standing`.
    """
    query = """
        with pos_by_year as (
        select r.year as Anio, c.name as Team, MAX(cs.wins) as Total_wins, MAX(cs.points) as Total_points,
        SUM(case
                when r2.positionOrder <= 3 then 1
                else 0
            end) as podiums
        from constructors c 
        join constructor_standings cs on c.constructorId = cs.constructorId 
        join races r on cs.raceId = r.raceId 
        join results r2 on r.raceId = r2.raceId and c.constructorId = r2.constructorId 
        group by r.year, c.name
        ),
        ranked as (select *, row_number() over (partition by Anio order by Total_points desc) as Standing
        from pos_by_year)
        select * from ranked;
    """
    df = pd.read_sql(query, engine)
    return df

def get_results_by_decade_team():
    """Return team performance metrics aggregated by decade.

    Includes `Decade`, `Team`, `Wins`, `Total_Races` and `Pct_of_Wins`.
    """
    query ="""
                 with winners_by_decade as (
                    select FLOOR(r2.year/10) * 10 as Decade,
                    c.name as Team,
                    SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins,
                    COUNT(r.constructorId) as Total_Races
                    from races r2
                    join results r on r2.raceId = r.raceId
                    join constructors c on r.constructorId = c.constructorId
                    group by Decade, Team
                    having Wins > 0
                    order by Decade asc, Wins desc),
                    ranked as (
                        select *, ROUND(Wins*100/Total_Races, 2) as Pct_of_Wins, row_number() over (partition by Decade order by Wins desc) as rank_decade
                        from winners_by_decade
                    )
                select * from ranked order by Decade asc, rank_decade asc;
            """
    df = pd.read_sql(query, engine)
    return df

def get_wins_by_prix():
    """Return number of wins per team by Grand Prix (circuit).

    Columns: `Team`, `Grand_Prix`, `Wins`, `Total_races`.
    """
    query = """
            select c.name as Team, r2.name as Grand_Prix, SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins, COUNT(r.raceId) as Total_races
            from results r
            join constructors c on r.constructorId = c.constructorId 
            join races r2 on r.raceId = r2.raceId
            group by c.name, r2.name
            order by c.name, Wins desc;
    """
    df = pd.read_sql(query, engine)
    return df
