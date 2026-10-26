USE hospital_analytics;

-- Create hospitals table
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_name VARCHAR(150) NOT NULL UNIQUE
);

-- Insert unique hospital names
INSERT IGNORE INTO hospitals (hospital_name)
SELECT DISTINCT hospital_name_department
FROM department_availability
WHERE hospital_name_department IS NOT NULL;

-- Verify hospital records
SELECT * FROM hospitals;