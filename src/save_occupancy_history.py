import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from datetime import datetime

# MySQL database configuration
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "hospital_analytics"


def get_database_engine():
    if not DB_PASSWORD:
        raise ValueError(
            "MYSQL_PASSWORD is not set. "
            "Add it to your PyCharm environment variables."
        )

    database_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=3306,
        database=DB_NAME,
    )

    return create_engine(database_url)


def test_connection():
    engine = get_database_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM hospitals")
        )

        total_hospitals = result.scalar()

        print("MySQL connection successful!")
        print("Total hospitals:", total_hospitals)


def save_history(df):
    engine = get_database_engine()

    # One timestamp for the entire simulation cycle
    recorded_at = datetime.now()

    query = text("""
        INSERT INTO bed_occupancy_history
        (department_id, recorded_at, occupied_beds,
         available_beds, simulated_event)

        SELECT
            d.department_id,
            :recorded_at,
            :occupied_beds,
            :available_beds,
            :simulated_event
        FROM departments d
        JOIN hospitals h
            ON d.hospital_id = h.hospital_id
        WHERE h.hospital_name = :hospital_name
          AND d.department_name = :department_name
    """)

    with engine.begin() as connection:
        # Verify that every simulated department exists in MySQL
        result = connection.execute(text("""
            SELECT h.hospital_name, d.department_name
            FROM departments d
            JOIN hospitals h ON d.hospital_id = h.hospital_id
        """))

        database_departments = set(result.fetchall())

        simulation_departments = set(
            zip(df["hospital_name_department"], df["department"])
        )

        missing = simulation_departments - database_departments

        if missing:
            raise ValueError(
                f"Departments missing from MySQL: {missing}"
            )
        for _, row in df.iterrows():
            connection.execute(

                query,
                {
                    "recorded_at": recorded_at,
                    "occupied_beds": int(row["occupied_beds"]),
                    "available_beds": int(row["available_beds"]),
                    "simulated_event": row["simulated_event"],
                    "hospital_name": row["hospital_name_department"],
                    "department_name": row["department"],
                },
            )

    print("Occupancy history saved to MySQL!")

if __name__ == "__main__":
    test_connection()

