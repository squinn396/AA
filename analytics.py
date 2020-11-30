from database import *
import math as m


def net(account_name):
    # shows the net available money in an account
    account = get_account(account_name)
    gross = account['balance']

    allocated = 0

    for allocation in get_allocations(account_name):
        allocated += allocation['balance']

    return gross - allocated


def balances(account_name):
    return [allocation['balance'] for allocation in get_allocations(account_name)]


def percent_account(account_name):
    # calcs what percent of the account an allocation makes up
    allocations = balances(account_name)
    account = get_account(account_name)['balance']

    return [(allocation / account) * 100
            if (allocation / account) * 100 >= 1
            else m.ceil((allocation / account) * 100)
            for allocation in allocations]


def percent_goal(a_name):
    # calcs what percent of the goal the allocation has in its balance
    allocation = get_allocation(a_name)
    return (allocation['balance'] / allocation['goal']) * 100
