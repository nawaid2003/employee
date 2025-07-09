import pandas as pd

data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', 'Diana Prince', 'Peter Parker', 'Mary Johnson', 'David Miller', 'Sarah Connor'],
    'Email': ['john.doe@example.com', 'jane.smith@example.com', 'bob.johnson@example.com', 'alice.brown@example.com', 'charlie.wilson@example.com', 'diana.prince@example.com', 'peter.parker@example.com', 'mary.johnson@example.com', 'david.miller@example.com', 'sarah.connor@example.com'],
    'Department': ['IT', 'HR', 'Finance', 'IT', 'Marketing', 'HR', 'IT', 'Finance', 'Marketing', 'IT'],
    'Designation': ['Software Engineer', 'HR Manager', 'Accountant', 'DevOps Engineer', 'Marketing Coordinator', 'Recruiter', 'Web Developer', 'Financial Analyst', 'Content Creator', 'Data Scientist']
}
df = pd.DataFrame(data)
df.to_excel('employees.xlsx', index=False)
print('Sample Excel file created: employees.xlsx')