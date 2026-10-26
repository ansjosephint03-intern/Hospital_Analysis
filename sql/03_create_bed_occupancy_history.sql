USE hospital_analytics;

-- Create historical occupancy table
CREATE TABLE IF NOT EXISTS bed_occupancy_history (
    history_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    recorded_at DATETIME NOT NULL,
    occupied_beds INT NOT NULL,
    available_beds INT NOT NULL,
    simulated_event VARCHAR(30),

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- Verify the table structure
DESCRIBE bed_occupancy_history;

-- Check historical records
SELECT *
FROM bed_occupancy_history
ORDER BY recorded_at DESC;