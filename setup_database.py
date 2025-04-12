"""
Database initialization script for Sea Ice Preservation Simulator.

Run this script once to set up the database schema and 
initialize default data.
"""

from utils.database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")