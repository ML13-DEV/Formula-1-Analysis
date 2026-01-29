"""f1lib package: helpers to read F1 data as DataFrames."""
from .decades import *
from .drivers import *
from .teams import *

__all__ = [
    "get_top_drivers_by_decade",
    "get_bestdriver_by_decade",
    "get_races_by_decade",
    "get_avg_pos_by_driver",
    "get_wins_points_by_driver",
    "get_podium_streaks",
    "get_pit_stops",
    "get_avg_pos_by_team",
    "get_counts_DNFs_byTeam",
    "get_pos_by_year_teams",
]
