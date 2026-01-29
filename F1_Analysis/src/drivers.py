"""Driver-related queries for the F1 Analysis project.

Each function returns a pandas DataFrame produced by executing
an SQL query via the shared `engine` in `src.db`.
"""

import pandas as pd
from .db import engine

def get_avg_pos_by_driver():
    """Return average finishing position per driver.

    Columns: `driverId`, `Driver`, `AvgPos`, `Amount_of_Races`.
    """
    query = """select d.driverId, CONCAT(d.forename, " ", d.surname) as Driver, ROUND(AVG(r.positionOrder),2) as AvgPos, COUNT(r.raceId) as Amount_of_Races
                from results r
                join drivers d
                on r.driverId = d.driverId
                group by d.driverId
                order by AvgPos asc;
            """
    df = pd.read_sql(query, engine)
    return df

def get_wins_points_by_driver():
    """Return wins, total points and laps completed for each driver.

    Columns include `Driver`, `Wins`, `Total_Points`, `Amount_of_Laps`.
    """
    query = """select d.driverId, CONCAT(d.forename, " ", d.surname) as Driver,
        SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins,
        SUM(r.points) as Total_Points,
        SUM(r.laps) as Amount_of_Laps,
        COUNT(DISTINCT r.raceId) AS Races_Started
        from drivers d
        join results r on d.driverId = r.driverId
        group by d.driverId, d.surname
        order by Total_Points desc;
    """
    df = pd.read_sql(query, engine)
    return df

def get_pos_by_year():
    """Return driver standings per year including total points and wins.

    Columns: `Anio`, `Driver`, `Total_wins`, `Total_points`, `pctWin`, `Standings`.
    """
    query = """with pos_by_year as (
                select r.year as Anio, d.driverId, CONCAT(d.forename, " ", d.surname) as Driver, 
                MAX(ds.wins) as Total_wins, MAX(ds.points) as Total_points, ROUND((MAX(ds.wins)/COUNT(r.raceId)),2) as pctWin
                from drivers d 
                join driver_standings ds on d.driverId  = ds.driverId  
                join races r on ds.raceId = r.raceId
                group by r.year, d.driverId
                ),
                ranked as (select *, row_number() over (partition by Anio order by Total_points desc) as Standings
                from pos_by_year)
                select * from ranked;
        """
    df = pd.read_sql(query, engine)
    return df

def get_podium_streaks():
    """Return drivers with longest podium streaks.

    The query computes consecutive podium periods and returns
    `Driver`, `Period`, `podium_streak`, and `total_wins`.
    """
    query = """with podiums as (
                select d.driverId, d.forename, d.surname, r.year, r.round,
                case
                    when r2.positionOrder <= 3 then 1
                    else 0
                end as is_podium,
                case
                    when r2.positionOrder = 1 then 1
                    else 0
                end as win
                from drivers d
                join results r2 on d.driverId = r2.driverId
                join races r on r2.raceId = r.raceId
            ),
            flags as (
                select *, lag(is_podium) over (partition by driverId order by year, round) as prev_podiums
                from podiums
            ),
            streaks as (
                select *,
                case
                    when is_podium = 1 and (prev_podiums = 0 or prev_podiums is null)
                    then 1
                    else 0
                end as new_streak
                from flags
                
            ),
            grouped as (
                select *,
                sum(new_streak) over (partition by driverId order by year, round) as id_streak
                from streaks
            )
            select CONCAT(forename," ",surname) as Driver, CONCAT(MIN(year),"-", MAX(year)) as Period, COUNT(*) as podium_streak, SUM(win) as total_wins from grouped
            where is_podium = 1
            group by driverId, id_streak
            order by podium_streak desc;"""
    df = pd.read_sql(query, engine)
    return df

def get_points_races_by_circuit():
    """Return points and races per driver grouped by circuit.

    Columns include `Driver`, `Grand_Prix`, `Total_Points`, `Total_Races`, `Avgpos`, `Wins`.
    """
    query = """select d.driverId, CONCAT(d.forename, " ", d.surname) as Driver,  r2.name as Grand_Prix,
        SUM(r.points) as Total_Points, COUNT(r.driverId) as Total_Races, ROUND(AVG(r.positionOrder),2) as Avgpos, 
        SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins
        from drivers d
        join results r on d.driverId = r.driverId
        join races r2 on r.raceId = r2.raceId
        group by d.driverId, grand_prix
        order by d.driverId, Total_Points desc;
    """
    df = pd.read_sql(query, engine)
    return df


