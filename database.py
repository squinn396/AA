import sqlite3


# CREATE DATABASE
def create_account_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts(
        account_id INTEGER PRIMARY KEY, 
        name TEXT UNIQUE, 
        balance REAL)""")

    connection.commit()
    connection.close()


def create_allocation_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Allocations(
        allocation_id INTEGER PRIMARY KEY, 
        name TEXT, 
        goal REAL, 
        balance REAL,
        account_id INTEGER, 
        FOREIGN KEY (account_id) REFERENCES Accounts(account_id))""")

    connection.commit()
    connection.close()


# ADDING

def add_account(name, balance):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Accounts(name, balance) VALUES(?, ?)', (name, balance))

    connection.commit()
    connection.close()


def add_allocation(name, goal, balance, account_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Allocations(name, goal, balance, account_id) VALUES(?, ?, ?, ?)',
                   (name, goal, balance, account_id))

    connection.commit()
    connection.close()


# RETRIEVING

def get_all_accounts():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Accounts')
    accounts = [{'account_id': row[0], 'name': row[1], 'balance': row[2]} for row in cursor.fetchall()]

    connection.close()

    return accounts


def get_account(account_no):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Accounts WHERE account_id = ?', [account_no])
    account = [{'account_id': row[0], 'name': row[1], 'balance': row[2]} for row in cursor.fetchall()][0]

    connection.close()

    return account


def get_allocation(allocation_name=None, allocation_id=None):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    if allocation_name != None:
        cursor.execute('SELECT * FROM Allocations WHERE name = ?', (allocation_name,))
        allocation = \
            [{'allocation_id': row[0], 'name': row[1], 'goal': row[2], 'balance': row[3], 'account_id': row[4]} for row
             in
             cursor.fetchall()][0]



    elif allocation_id:
        cursor.execute('SELECT * FROM Allocations WHERE allocation_id = ?', (allocation_id,))
        allocation = \
            [{'allocation_id': row[0], 'name': row[1], 'goal': row[2], 'balance': row[3], 'account_id': row[4]} for row
             in
             cursor.fetchall()][0]

    connection.close()

    return allocation


def get_allocations(account_no):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('Select * FROM Allocations WHERE account_id = ?', (account_no,))
    allocations = [{'allocation_id': row[0], 'name': row[1], 'goal': row[2], 'balance': row[3], 'account_id': row[4]}
                   for row in cursor.fetchall()]

    connection.close()
    return allocations


def get_account_no(name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT account_id FROM Accounts WHERE name = ?', (name,))
    account_no = cursor.fetchone()

    connection.close()
    # print(account_no)
    if account_no == None:
        a = None
    else:
        a = account_no[0]
    return a


# EDITING

def account_deposit(name, amount):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE name = ?', (amount, name))
    connection.commit()

    connection.close()
    info = get_account(get_account_no(name))
    print(f'{info["name"]}: ${info["balance"]}')


def allocation_deposit(name, amount):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE Allocations SET balance = balance + ? WHERE name = ?', (amount, name))
    connection.commit()

    connection.close()

    a = [al for al in get_allocations(get_allocation(name)['account_id']) if al['name'] == name][0]
    print(a)
    print(f"{a['name']}: ${a['balance']}")


def change_goal(name, new_goal):
    pass


# REMOVING

def delete_account(name):
    id = get_account_no(name)

    allocation_ids = [x['allocation_id'] for x in get_allocations(id)]
    for allocation in allocation_ids:
        delete_allocation(allocation)

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Accounts WHERE name = ?', (name,))
    connection.commit()

    connection.close()


def delete_allocation(a_id):
    a = get_allocation(allocation_id=a_id)

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Allocations WHERE allocation_id = ?', (a_id,))
    connection.commit()

    connection.close()

    print(f"{a['name']} deleted!")
# CALCULATION
