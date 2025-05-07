Poetry is required to run this project: https://python-poetry.org

Install dependencies:
`poetry install`

Run program:
`poetry run python3 main.py`

Before running the database tables have to be created manually

```sql
create table Client (
client_id int, 
first_name varchar(20), 
last_name varchar(20), 
income float, 
primary key (client_id));

create table Auto_Loan (
client_id int,
VIN varchar(17),
Loan_Amount float,
Interest_Rate float,
Start_Date TIMESTAMP,
End_Date TIMESTAMP,
Number_Of_Payments Integer,
Make varchar(50),
Model varchar(50),
Amount_Paid float,
Year_made int,
PRIMARY KEY(VIN),
foreign key (client_id) references Client(client_id)
);

Create table Personal_Loan (
client_id int,
loan_id int,
Loan_Purpose varchar2(50),
Loan_Amount float(2),
Interest_Rate float(2),
Amount_paid float(2),
Start_Date DATE,
End_Date DATE,
Num_Of_Payments Integer,
PRIMARY KEY(loan_id),
foreign key (client_id) references Client(client_id)
);

create table Student_Loan (
client_id int,
loan_id int,
loan_term varchar(50),
disbursement_date DATE,
Repayment_Start_Date DATE,
Repayment_End_Date DATE,
Monthly_Payment float(2),
Grace_Period Integer,
Loan_type varchar(50),
Primary Key (loan_id),
foreign key (client_id) references Client(client_id)
);

create table Mortgage (
client_id int,
house_address varchar(50),
house_area float(2),
num_bedrooms Integer,
house_price float(2),
loan_amount float(2),
interest_rate float(2),
amount_paid float(2),
start_date DATE,
num_payments Integer,
end_date DATE,
PRIMARY KEY (house_address),
foreign key (client_id) references Client(client_id)
);
```
