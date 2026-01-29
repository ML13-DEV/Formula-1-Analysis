"""Helpers to query F1 statistics aggregated by decade.

This module provides functions that return DataFrames with
aggregated statistics (points, wins, races) grouped by decade
for drivers and teams.
"""

import pandas as pd
from .db import engine

def get_top_drivers_by_decade():
    """Return a DataFrame of top drivers per decade.

    The DataFrame includes columns such as `Decade`, `Driver`,
    `Total_Points`, `Wins` and `Total_Races`, ordered by decade
    and ranking within the decade.
    """
    query = """with winners_by_decade as (
            select FLOOR(r2.year/10) * 10 as Decade,
            CONCAT(d.forename, " ", d.surname) as Driver,
            SUM(r.points) as Total_Points,
            SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins,
            COUNT(distinct r.raceId) as Total_Races
            from races r2
            join results r on r2.raceId = r.raceId
            join drivers d on r.driverId = d.driverId
            group by Decade, d.driverId
            having Total_Points > 0),
            ranked as (
                select *, ROUND(Wins*100/Total_Races, 2) as Pct_of_Wins, row_number() over (partition by Decade order by Total_Points desc) as rank_decade
                from winners_by_decade
            )
        select * from ranked -- where rank_decade <= 5
        order by Decade asc, rank_decade asc;
        """
    
    df = pd.read_sql(query, engine)
    return df

def get_bestdriver_by_decade():
    """Return the best driver for each decade based on wins.

    The result contains one row per decade with the driver who
    recorded the most wins in that decade.
    """
    query = """with winners_by_decade as (
                select FLOOR(r2.year/10) * 10 as Decade,
                d.forename as Driver_Name,
                d.surname as Driver_Surname,
                SUM(r.points) as Total_Points,
                SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins,
                COUNT(r.driverId) as Total_Races
                from races r2
                join results r on r2.raceId = r.raceId
                join drivers d on r.driverId = d.driverId
                group by Decade, Driver_Name
                having Wins > 0
                order by Decade asc, Wins desc),
                ranked as (
                    select *, ROUND(Wins*100/Total_Races, 2) as Pct_of_Wins, row_number() over (partition by Decade order by Wins desc) as rank_decade
                    from winners_by_decade
                )
            select * from ranked where rank_decade = 1
            order by Decade asc, rank_decade asc;"""
    
    df = pd.read_sql(query, engine)
    return df

def get_best_teamby_decade():
    """Return teams aggregated by decade with points and wins.

    The DataFrame includes `Decade`, `Team`, `Total_Points`,
    `Wins`, `Total_Races` and a percentage of wins for the decade.
    """
    query = """with winners_by_decade as (
                select FLOOR(r2.year/10) * 10 as Decade,
                c.constructorId,
                c.name as Team,
                SUM(r.points) as Total_Points,
                SUM(case when r.positionOrder = 1 then 1 else 0 end) as Wins,
                COUNT(distinct r.raceId) as Total_Races
                from races r2
                join results r on r2.raceId = r.raceId
                join constructors c on r.constructorId = c.constructorId
                group by Decade, c.constructorId
                having Wins > 0
                order by Decade asc, Wins desc),
                ranked as (
                    select *, ROUND(Wins*100/Total_Races, 2) as Pct_of_Wins, row_number() over (partition by Decade order by Total_Points desc) as rank_decade
                    from winners_by_decade
                )
            select * from ranked 
            order by Decade asc, rank_decade asc;
            """
    df = pd.read_sql(query, engine)
    return df  


