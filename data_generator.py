import pandas as pd
import random
from faker import Faker
from datetime import datetime

fake = Faker('pt_PT')

def generate_data():
    data = []
    for _ in range(100000):
        customer_id= fake.unique.random_int(min=1, max=9999999)
        name = fake.name()
        email = fake.unique.email()
        phone_number = fake.phone_number()
        address = fake.address().replace('\n', ', ')
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
        registration_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
        plan = random.choice(['Basic', 'Standard', 'Premium'])
        status = random.choice(['Active', 'Inactive', 'Pending'])
        date_of_churn = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d') if status == 'Inactive' else None
        employee_id = fake.random_int(min=1, max=10000)      
                
        data.append({
            'customer_id': customer_id,
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'address': address,
            'date_of_birth': date_of_birth,
            'registration_date': registration_date,
            'plan': plan,
            'status': status,
            'date_of_churn': date_of_churn,
            'employee_id': employee_id
        })
    
    return pd.DataFrame(data)

df= generate_data()
df.to_csv('customer_data.csv', index=False, encoding='utf-8')
print("Data generated and saved to customer_data.csv")