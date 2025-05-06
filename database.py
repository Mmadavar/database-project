import oracledb
from datetime import datetime

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

def addClient(first: str, last: str, income: str, id: int = None):
    cursor = connection.cursor()

    if id is None:
        id = cursor.execute(
            'SELECT max(client_id) FROM Client'
        ).fetchone()[0]
    
    if id is None:
        id = 1
    else:
        id += 1
    
    cursor.execute(
        'INSERT INTO Client VALUES (:id, :first, :last, :income)', [id, first, last, income]
    )

    connection.commit()

def getClient(client_id: int):
    cursor = connection.cursor()
    res = cursor.execute('SELECT * FROM Client WHERE client_id = :id', id=client_id).fetchone()
    return res

def getClients():
    return connection.cursor().execute(
        'SELECT * FROM client ORDER BY client_id ASC'
    ).fetchall()

def updateClient(client_id: int, first: str, last: str, income: float):
    connection.cursor().execute(
        'UPDATE Client SET first_name=:first, last_name=:last, income=:income WHERE client_id=:id',
        [first, last, income, client_id]
    )
    connection.commit()

def deleteClient(client_id: int):
    connection.cursor().execute(
        'DELETE FROM Client WHERE client_id = :id', id=client_id
    )
    connection.commit()

def getAutoLoan(vin: str):
    return connection.cursor().execute(
        'SELECT * FROM Auto_Loan WHERE VIN = :vin', vin=vin
    ).fetchone()

def getAutoLoans():
    if userid is not None:
        return connection.cursor().execute(
            'SELECT VIN, client_id, Year_made, Make, Model FROM Auto_Loan WHERE client_id = :id ORDER BY VIN ASC', id=userid
        )
    else:
        return connection.cursor().execute(
            'SELECT VIN, client_id, Year_made, Make, Model FROM Auto_Loan order by VIN ASC'
        ).fetchall()

def addAutoLoan(
        client_id: int, VIN: str, loan_amount: float, interest_rate: float, start_date: datetime, 
        end_date: datetime, num_payments: int, make: str, model: str, amount_paid: float, year_made: int
):
    connection.cursor().execute(
        'INSERT INTO Auto_Loan VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)',
        [client_id, VIN, loan_amount, interest_rate, start_date, end_date, num_payments, make, model, amount_paid, year_made ]
    )
    connection.commit()

def updateAutoLoan(
        client_id: int, VIN: str, loan_amount: float, interest_rate: float, start_date: datetime, 
        end_date: datetime, num_payments: int, make: str, model: str, amount_paid: float, year_made: int
):
    connection.cursor().execute(
        'UPDATE Auto_Loan SET client_id=:1, loan_amount=:2, interest_rate=:3, start_date=:4, end_date=:5, \
            number_of_payments=:6, make=:7, model=:8, amount_paid=:9, year_made=:10 WHERE vin=:11',
        [client_id, loan_amount, interest_rate, start_date, end_date, num_payments, make, model, amount_paid, year_made, VIN]
    )
    connection.commit()

def deleteAutoLoan(vin: str):
    connection.cursor().execute(
        'DELETE FROM Auto_Loan WHERE vin=:vin', vin=vin
    )
    connection.commit()

def getPersonalLoan(loan_id: int):
    return connection.cursor().execute(
        'SELECT * FROM Personal_Loan WHERE loan_id = :id', id=loan_id
    ).fetchone()

def getPersonalLoans():
    if userid is not None:
        return connection.cursor().execute(
            'SELECT loan_id, client_id, loan_amount FROM Personal_Loan WHERE client_id = :id', id=userid
        ).fetchall()
    else:
        return connection.cursor().execute(
            'SELECT loan_id, client_id, loan_amount FROM Personal_Loan'
        ).fetchall()
    
def addPersonalLoan(client_id: int, loan_purpose: str, loan_amount: str, 
                    interest_rate: float, amount_paid: float, start_date: datetime, 
                    end_date: datetime, number_of_payments: int, loan_id: int | None = None):
    if loan_id is None:
        loan_id = connection.cursor().execute(
            'SELECT max(loan_id) FROM Personal_Loan'
        ).fetchone()[0]
    
    if loan_id is None:
        loan_id = 1
    else:
        loan_id += 1
    
    connection.cursor().execute(
        'INSERT INTO Personal_Loan VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)',
        [client_id, loan_id, loan_purpose, loan_amount, interest_rate, amount_paid, 
         start_date, end_date, number_of_payments]
    )

    connection.commit()

def updatePersonalLoan(client_id: int, loan_purpose: str, loan_amount: str, 
                    interest_rate: float, amount_paid: float, start_date: datetime, 
                    end_date: datetime, number_of_payments: int, loan_id: int):
    connection.cursor().execute(
        'UPDATE Personal_Loan SET client_id=:1, Loan_Purpose=:2, Loan_Amount=:3, Interest_Rate=:4, \
            Amount_paid=:5, Start_Date=:6, End_Date=:7, Num_Of_Payments=:8 WHERE loan_id=:9',
            [client_id, loan_purpose, loan_amount, interest_rate, amount_paid,
             start_date, end_date, number_of_payments, loan_id]
    )
    connection.commit()

def deletePersonalLoan(loan_id: int):
    connection.cursor().execute(
        'DELETE FROM Personal_Loan WHERE loan_id = :loan_id', loan_id = loan_id
    )
    connection.commit()

def getStudentLoan(loan_id: int):
    return connection.cursor().execute(
        'SELECT * FROM Student_Loan WHERE loan_id = :id', id=loan_id
    ).fetchone()

def getStudentLoans():
    if userid is not None:
        return connection.cursor().execute(
            'SELECT loan_id, client_id, monthly_payment FROM Student_Loan WHERE client_id = :id', id=userid
        ).fetchall()
    else:
        return connection.cursor().execute(
            'SELECT loan_id, client_id, monthly_payment FROM Student_Loan'
        ).fetchall()

def addStudentLoan(client_id: int, loan_term: int, disbursement_date: datetime,
                   repayment_start_date: datetime, repayment_end_date: datetime,
                   monthly_payment: float, grace_period: int, loan_type: str,
                   loan_id: int | None = None):
    
    if loan_id is None:
        loan_id = connection.cursor().execute(
            'SELECT max(loan_id) FROM Student_Loan'
        ).fetchone()[0]

    if loan_id is None:
        loan_id = 1
    else:
        loan_id += 1

    connection.cursor().execute(
        'INSERT INTO Student_Loan VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)',
        [client_id, loan_id, loan_term, disbursement_date, repayment_start_date,
         repayment_end_date, monthly_payment, grace_period, loan_type]
    )
    connection.commit()

def updateStudentLoan(client_id: int, loan_term: int, disbursement_date: datetime,
                   repayment_start_date: datetime, repayment_end_date: datetime,
                   monthly_payment: float, grace_period: int, loan_type: str,
                   loan_id: int):
    connection.cursor().execute(
        'UPDATE Student_Loan SET client_id=:1, loan_term=:2, disbursement_date=:3, \
        Repayment_Start_Date=:4, Repayment_End_Date=:5, Monthly_Payment=:6, \
        Grace_Period=:7, Loan_type=:8 WHERE loan_id=:9',
        [client_id, loan_term, disbursement_date, repayment_start_date,
         repayment_end_date, monthly_payment, grace_period, loan_type, loan_id]
    )
    connection.commit()

def deleteStudentLoan(loan_id: int):
    connection.cursor().execute(
        'DELETE FROM Student_Loan WHERE loan_id = :loan_id', loan_id = loan_id
    )
    connection.commit()

def getMortgage(house_address: str):
    return connection.cursor().execute(
        'SELECT * FROM Mortgage WHERE house_address = :addr', addr=house_address
    ).fetchone()

def getMortgages():
    if userid is not None:
        return connection.cursor().execute(
            'SELECT house_address, client_id FROM Mortgage WHERE client_id = :cid', cid=userid
        ).fetchall()
    else:
        return connection.cursor().execute(
            'SELECT house_address, client_id FROM Mortgage'
        ).fetchall()

def deleteMortgage(house_address: str):
    connection.cursor().execute(
    'DELETE FROM Mortgage WHERE house_address = :addr', addr=house_address
    )
    connection.commit()

def addMortgage(client_id: int, house_address: str, house_area: float, num_bedrooms: int,
                house_price: float, loan_amount: float, interest_rate: float, amount_paid: float, start_date: datetime,
                num_payments: int, end_date: datetime):
    connection.cursor().execute(
        'INSERT INTO Mortgage VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)',
        [client_id, house_address, house_area, num_bedrooms, house_price, loan_amount,
         interest_rate, amount_paid, start_date, num_payments, end_date,]
    )
    connection.commit()

def updateMortgage(client_id: int, house_address: str, house_area: float, num_bedrooms: int,
                house_price: float, loan_amount: float, interest_rate: float, amount_paid: float, start_date: datetime,
                num_payments: int, end_date: datetime):
    connection.cursor().execute(
        'UPDATE Mortgage SET client_id=:1, house_area=:2, \
        num_bedrooms=:3, house_price=:4, loan_amount=:5, interest_rate=:6, \
        amount_paid=:7, start_date=:8, num_payments=:9, end_date=:10 \
        WHERE house_address=:11',
        [client_id, house_area, num_bedrooms, house_price, loan_amount,
         interest_rate, amount_paid, start_date, num_payments, end_date,
         house_address]
    )
    connection.commit()

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
            Amount_paid float(2),
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
    
    connection.commit()