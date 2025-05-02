import oracledb

SERVER = 'h3oracle.ad.psu.edu'
SERVICE_NAME = 'orclpdb.ad.psu.edu'
PORT = 1521

connection = None
userid = None

def connect(username: str, password: str):
    dsn_tns = oracledb.makedsn(SERVER, PORT, service_name=SERVICE_NAME)
    global connection
    connection = oracledb.connect(user=username, password=password, dsn = dsn_tns)

def setUserId(id: int):
    global userid
    userid = id

def addClient(first: str, last: str, income: str):
    pass

def dropTables():
    cursor = connection.cursor()

    table_names = ['Client', 'Auto_Loan', 'Personal_Loan', 'Student_Loan', 'Mortgage']

    table_names.reverse()

    for table in table_names:
        print(f'Dropping table "{table}"')
        try:
            cursor.execute(
                f'DROP TABLE {table}'
            )
        except Exception as e:
            print(f'Table "{table}" does not exist, skipping.')
            print(e)

def createTables():
    cursor = connection.cursor()

    cursor.execute(
        '''create table Client (
        client_id int, 
        first_name varchar(20), 
        last_name varchar(20), 
        income float, 
        primary key (client_id))''')

    cursor.execute(
        '''create table Auto_Loan (
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
        )''')
    
    cursor.execute(
        '''Create table Personal_Loan (
            client_id int,
            loan_id int,
            Loan_Purpose varchar2(50),
            Loan_Amount float(2),
            Interest_Rate float(2),
            Amount_piad float(2),
            Start_Date DATE,
            End_Date DATE,
            Num_Of_Payments Integer,
            PRIMARY KEY(loan_id),
            foreign key (client_id) references Client(client_id)
        )''')

    cursor.execute(
        '''create table Student_Loan (
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
        )''')

    cursor.execute(
        '''create table Mortgage (
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
        )''')