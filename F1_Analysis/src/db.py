"""Database engine setup for F1 Analysis.

This module creates a SQLAlchemy engine using the `DATABASE_F1`
environment variable. Other modules import `engine` to run SQL
queries against the F1 dataset.
"""

import os
from sqlalchemy import create_engine

# Create a SQLAlchemy engine from the `DATABASE_F1` environment
# variable (e.g. a connection string). The engine is imported
# by other modules to execute read-only queries.
engine = create_engine(os.getenv("DATABASE_F1"), future=True)