USE hospital_analytics;

-- Create departments table
CREATE TABLE IF NOT EXISTS departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    total_beds INT NOT NULL,

    CONSTRAINT fk_department_hospital
        FOREIGN KEY (hospital_id)
        REFERENCES hospitals(hospital_id),

    CONSTRAINT unique_hospital_department
        UNIQUE (hospital_id, department_name)
);

-- Insert department records
INSERT INTO departments (
    hospital_id,
    department_name,
    total_beds
)
SELECT
    h.hospital_id,
    d.department,
    d.department_bed_capacity
FROM department_availability d
INNER JOIN hospitals h
    ON d.hospital_name_department = h.hospital_name
ON DUPLICATE KEY UPDATE
    total_beds = VALUES(total_beds);

-- Verify department records
SELECT
    h.hospital_name,
    d.department_name,
    d.total_beds
FROM departments d
INNER JOIN hospitals h
    ON d.hospital_id = h.hospital_id
ORDER BY h.hospital_name;

-- Check total departments
SELECT COUNT(*) AS total_departments
FROM departments;