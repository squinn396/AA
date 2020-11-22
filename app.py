from analytics import *

"""
need to be able to:
    create allocations within an account
    return allocation goal and balance
    return net account balance
    visual display of balances
"""

clear = """



$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$




"""


# HOME SCREEN
def home():
    create_account_table()
    create_allocation_table

    choice = int(input(
        """$$$ Welcome to your funds allocations app, would you like to: $$$\n1) View accounts \n2) Add account \n3) Delete account \n4) Quit\n\n"""))
    if choice not in [1, 2, 3, 4]:
        print('\nInvalid input: enter a number corresponding to one of the menu choices', clear)
        home()

    elif choice == 1:
        view_accounts()

    elif choice == 2:
        add_account_info()

    elif choice == 3:
        delete_account_info()

    elif choice == 4:
        return


# CREATING

def add_account_info():
    print(clear)
    name = input('New Account Name: ')
    balance = float(input('Balance of new Account: '))

    confirm = input(f'Confirm creation of {name} with a balance of ${balance}? (Y/n): ')

    if confirm != 'n':
        add_account(name, balance)

        yn = input('Do you want to add any fund allocations to this account? (Y/n): ')

        if yn != 'n':
            parent_account = get_account(get_account_no(name))
            print(clear)
            print(f"{parent_account['name']}: ${parent_account['balance']}")
            add_allocation_info(pa_name=parent_account['name'], pa_no=parent_account['account_id'])

        print('Account created!', clear)
    input()
    print(clear)
    home()


def add_allocation_info(pa_name, pa_no):
    print(f'New Allocation for {pa_name} account:\n')
    name = input('Name for new allocation:\t')
    goal = int(input('Goal for new allocation:\t'))
    dp = int(input('Initial deposit for new allocation:\t'))

    t = False

    yn = input(f'Are you taking the deposit from the balance of {pa_name}? (Y/n): ')

    confirm = input(f'Create {name} with goal of ${goal} and balance of ${dp}? (Y/n):\t')

    if confirm == 'n':
        add_allocation_info()
    else:
        if yn == 'n':
            account_deposit(pa_name, dp)
        add_allocation(name=name, goal=goal, balance=dp, account_id=pa_no)
        print('Allocation created!')


# VIEWING
def view_accounts2():
    accounts = [account['name'] for account in get_all_accounts()]
    return accounts


def view_accounts():
    accounts = get_all_accounts()
    print(clear)
    if accounts == []:
        print(f'THERE ARE NO ACCOUNTS')
    else:
        for account in accounts:
            print(account)
    print(clear)
    yn = input('Do you want to access any of your accounts? (Y/n):\t')

    if yn != 'n':
        account_page(accounts)
    else:
        input()
        home()


def account_page(accounts_list):
    select = int(input('Enter the account number corresponding to the account you want to access:\t'))
    if select in [account['account_id'] for account in accounts_list]:
        account = get_account(select)
        print(account)
        allocations = get_allocations(select)
        name = account['name']
        id = account['account_id']
        net_value = net(id)
        choice = 0

        def prompt():
            print(f'{name}\t\t${account["balance"]}\t\t Account Number: {id}')
            for allocation in allocations:
                print(
                    f'\t{allocation["name"]}\t\t${allocation["balance"]} of ${allocation["goal"]} goal\tid:{allocation["allocation_id"]}\n')
            print(f'\n1) Deposit\t2) Create Allocation\t3) Delete Allocation\t4) Quit')
            return int(input())

        while choice not in [1, 2, 3, 4]:
            choice = prompt()

        if choice == 1:  # DEPOSIT
            print(clear)
            dp = int(input('How much do you want to deposit?:\t$'))
            location = input('Where do you want you want to deposit your savings (name of allocation or account)?:\t')
            if location == name:
                account_deposit(location, dp)
                print('Transaction deposited!')
            elif location in [allocation['name'] for allocation in allocations]:
                q = input(f'Are you taking the deposit from {name}? (Y/n):\t')
                if q == 'n':
                    account_deposit(name, dp)
                allocation_deposit(location, dp)
                input('Transaction deposited!')
                print(clear)
            else:
                raise ValueError('Invalid entry for deposit.')

        elif choice == 2:  # CREATE ALLOCATION
            add_allocation_info(name, id)

        elif choice == 3:  # DELETE ALLOCATION
            prompt = 'Enter the allocation number corresponding to the allocation you want to delete:\t'
            target = int(input(prompt))
            if target not in [x['allocation_id'] for x in allocations]:
                print('Invalid input\n', prompt)
            else:
                delete_allocation(target)
                input()
                print(clear)


        elif choice == 4:  # QUIT
            home()
        input()
        home()
    else:
        raise ValueError('The value you entered is not a valid account number')
        view_accounts()


# DELETE

def delete_account_info():
    name = input('Enter the name of the account you want deleted (enter 0 to quit):\t')

    if name not in [account['name'] for account in get_all_accounts()] and name != '0':
        print('Name not recognized, try again!')
    elif name == '0':
        input()
        print(clear)
        home()
    else:
        delete_account(name)
        input(f'{name} deleted!\n')
        input()
        print(clear)
        home()

if __name__ == "__main__":
    home()