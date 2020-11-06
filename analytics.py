from database import *
import math as m


def net(account_id):
    # shows the net available money in an account
    account = get_account(account_id)
    gross = account['balance']

    allocated = 0

    for allocation in get_allocations(account_id):
        allocated += allocation['balance']

    return gross - allocated


def balances(account_id):
    return [allocation['balance'] for allocation in get_allocations(account_id)]


def symbols(account_id):
    return [allocation['name'][0] for allocation in get_allocations(account_id)]


def bar(account_id):
    # shows a bar to represent savings and how they are distributed within an account
    free = net(account_id)
    allocations = balances(account_id)
    chars = symbols(account_id)
    nums = percent_account(account_id)
    p = []  # chars for % free of account

    for a in range(len(allocations)):
        p.append(chars[a] * int(nums[a]))

    p.sort(key=len)
    p.append(int(free / get_account(account_id)['balance'] * 100) * '$')

    for x in range(len(p)):
        print(p[x], end="")

    print('\n')

    for item in p:
        for l in item:
            if l == item[0]:
                print('|')
    print()


def percent_account(account_id):
    # calcs what percent of the account an allocation makes up
    allocations = balances(account_id)
    account = get_account(account_id)['balance']

    return [(allocation / account) * 100
            if (allocation / account) * 100 >= 1
            else m.ceil((allocation / account) * 100)
            for allocation in allocations]


def percent_goal(a_name):
    # calcs what percent of the goal the allocation has in its balance
    allocation = get_allocation(a_name)
    return (allocation['balance'] / allocation['goal']) * 100
