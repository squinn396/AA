from database import *
import plotly.express as px
import plotly.graph_objs as go

goal = 1000
balance = 450

groups = ["Deposited", "Remaining"]
amounts = [balance, goal-balance]


def allocation_pie(allocation):
    df = get_allocations(account_id=1)
    p = px.pie(df, values="balance", names="name", title="Account Allocations", plot_bgcolor="black")
    p.show()

    print(df)


if __name__ == "__main__":
    allocation_pie(1)

