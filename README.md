# Hospital Bed Occupancy Forecasting and Monitoring System

## Project Overview

This project is a Python-based hospital bed occupancy forecasting and monitoring system designed to support hospital resource planning.

It combines machine learning, simulated live occupancy updates, an interactive Streamlit dashboard, and MySQL-based historical data storage.

The system helps users monitor departmental bed availability, identify potential capacity risks, and explore occupancy trends.

**Note:** Live updates are simulated. This project is a demonstration system and is not connected to operational hospital information systems.

## Key Features

- **7-Day Occupancy Forecasting:** Uses XGBoost regression to predict future departmental bed occupancy.
- **Capacity Risk Prediction:** Uses XGBoost classification to estimate the probability of occupancy exceeding a defined threshold.
- **Explainable AI:** Uses SHAP to interpret factors influencing model predictions.
- **Interactive Dashboard:** Displays hospital capacity, department availability, forecasts, and risk alerts using Streamlit.
- **Live Simulation:** Simulates patient admissions and discharges to update bed availability.
- **MySQL Integration:** Automatically stores timestamped simulated occupancy records.
- **Historical SQL Analysis:** Supports analysis of ICU occupancy trends and departments frequently reaching full capacity.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | XGBoost, Scikit-learn |
| Explainability | SHAP |
| Visualization | Matplotlib, Streamlit |
| Database | MySQL |
| Database Connectivity | SQLAlchemy, PyMySQL |
| Development | PyCharm, MySQL Workbench |

## Project Structure

```text
bed_occupancy/
├── data/
├── models/
├── notebooks/
├── outputs/
├── sql/
│   ├── 01_create_hospitals_table.sql
│   ├── 02_create_departments_table.sql
│   ├── 03_create_bed_occupancy_history.sql
│   └── 04_historical_occupancy_analysis.sql
├── src/
│   ├── combine.py
│   ├── features.py
│   ├── train.py
│   ├── rollup.py
│   ├── explain.py
│   ├── simulate_live.py
│   └── save_occupancy_history.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Machine Learning Pipeline

### 1. Data Preparation

Hospital and departmental occupancy datasets are combined and cleaned.

The preprocessing pipeline prepares relevant features for forecasting, including:

- Historical occupancy measurements
- Rolling occupancy statistics
- Admission and discharge patterns
- Department bed capacity
- Other available contextual variables

### 2. Occupancy Forecasting

An XGBoost regression model estimates departmental occupancy over a seven-day forecasting horizon.

In the project's recorded evaluation, the regression model achieved:

| Metric | Result |
|---|---:|
| MAE | 4.895 |
| RMSE | 7.211 |
| R² | 0.744 |

These results describe the model's evaluation on the project's test dataset and should not be interpreted as independently validated hospital deployment performance.

### 3. Capacity Risk Prediction

An XGBoost classification model estimates the probability of departments exceeding the project's occupancy-risk threshold.

The predictions support risk categorization and alert generation.

### 4. Model Explainability

SHAP is used to examine how individual features contribute to the model's predictions.

This helps make the forecasting results more interpretable.

## Streamlit Dashboard

The dashboard provides an interactive interface for monitoring hospital and departmental occupancy.

It includes:

- Hospital-level capacity overview
- Department-level bed availability
- Occupancy forecasts
- Capacity risk indicators
- Simulated live updates

The simulation periodically updates occupied and available beds using randomly generated admission and discharge events.

These updates are for demonstration purposes and do not represent real patient transactions.

## MySQL Database Integration

The project uses a relational MySQL database named `hospital_analytics`.

### Database Tables

**1. `hospitals`**

Stores hospital identifiers and names.

**2. `departments`**

Stores department identifiers, hospital relationships, department names, and bed capacities.

**3. `bed_occupancy_history`**

Stores historical simulated occupancy snapshots, including:

- Department identifier
- Simulation timestamp
- Occupied beds
- Available beds
- Simulated event

The tables use primary keys and foreign keys to maintain relationships between hospitals, departments, and occupancy records.

### Automatic Historical Storage

The Python simulation updates the latest CSV outputs and saves historical occupancy records to MySQL.

Each successful simulation cycle stores one snapshot for all 68 departments.

Unlike the latest-state CSV files, the historical table retains earlier simulation snapshots for subsequent analysis.

### Historical SQL Analysis

SQL queries are used to:

- Retrieve ICU occupancy history
- Identify departments frequently reaching full capacity
- Validate occupied and available bed counts
- Verify completeness of saved simulation snapshots

## Installation and Setup

### 1. Clone the Repository

Clone the project repository and open the folder in your preferred Python development environment.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

Create a MySQL database named:

```sql
CREATE DATABASE IF NOT EXISTS hospital_analytics;
```

Run the SQL setup scripts in the `sql` folder in numerical order.

**Database setup prerequisite:** The hospital and department setup scripts use an imported `department_availability` source table. This source table must be prepared before running those scripts.

### 4. Configure Database Credentials

The database connection uses environment variables.

Set `MYSQL_PASSWORD` to your local MySQL password.

If your MySQL username differs from `root`, set `MYSQL_USER` accordingly.

Do not commit passwords, credentials, or private configuration files to GitHub.

### 5. Run the Dashboard

From the project directory, execute:

```bash
streamlit run dashboard.py
```

The dashboard runs locally and displays simulated occupancy updates.

For automatic MySQL history storage, ensure the MySQL service is running and the required environment variables are available to the Streamlit process.

## Data Validation

The project includes SQL checks to verify:

- Occupied beds are non-negative.
- Available beds are non-negative.
- Occupied beds do not exceed department capacity.
- Occupied and available beds sum to total department capacity.
- Stored simulation snapshots contain the expected 68 distinct departments.

These checks validate stored records but do not guarantee that every scheduled simulation cycle was executed successfully.

## Limitations

- Live occupancy updates are simulated rather than obtained from hospital systems.
- Forecasting results depend on the dataset and assumptions used during model development.
- The system is intended for academic demonstration and exploratory resource planning.
- The database integration does not currently guarantee recovery of simulation cycles that fail before successful storage.

## Future Enhancements

Potential improvements include:

- Historical occupancy trend visualizations using MySQL data
- Database-backed dashboard analytics
- Improved simulation error handling and recovery
- Deployment to a hosted environment
- Integration with authorized hospital information systems

## Conclusion

This project demonstrates an integrated workflow combining data processing, machine learning, explainable AI, interactive visualization, Python-based simulation, and relational database management.

It provides a practical example of using predictive analytics and historical data storage to explore hospital bed capacity and resource-planning challenges.
