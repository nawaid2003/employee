-- SQL Server Table Creation Script
-- Run in SQL Server Management Studio

-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'EmployeeDB')
BEGIN
    CREATE DATABASE EmployeeDB;
END

-- Use the database
USE EmployeeDB;

-- Create employees table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U')
BEGIN
    CREATE TABLE employees (
        ID INT PRIMARY KEY,
        Name NVARCHAR(100) NOT NULL,
        Email NVARCHAR(100) NOT NULL,
        Department NVARCHAR(50) NOT NULL,
        Designation NVARCHAR(50) NOT NULL
    );
END

-- Create index on Department
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_employees_Department' AND object_id = OBJECT_ID('employees'))
BEGIN
    CREATE INDEX IX_employees_Department ON employees(Department);
END

-- Optional: Insert sample data
-- DELETE FROM employees;
-- INSERT INTO employees (ID, Name, Email, Department, Designation) VALUES
-- (1, 'John Doe', 'john.doe@example.com', 'IT', 'Software Engineer'),
-- (2, 'Jane Smith', 'jane.smith@example.com', 'HR', 'HR Manager'),
-- (3, 'Bob Johnson', 'bob.johnson@example.com', 'Finance', 'Accountant'),
-- (4, 'Alice Brown', 'alice.brown@example.com', 'IT', 'DevOps Engineer'),
-- (5, 'Charlie Wilson', 'charlie.wilson@example.com', 'Marketing', 'Marketing Coordinator');

-- Verify table creation
SELECT * FROM employees;