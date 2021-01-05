import os
import plotly.express as px
import plotly.graph_objs as go
import psutil

from database import *

goal = 1000
balance = 450

groups = ["Deposited", "Remaining"]
amounts = [balance, goal - balance]


def account_pie(account: str):
    df = get_allocations(get_account_no(account))
    if df:
        layout = go.Layout(plot_bgcolor="#000")

        p = px.pie(df, values="balance")  # , names="name", title="Account Allocations")
        p.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
        #p.show()

        print(df)

        png_name = f"{account}.png"

        if not os.path.exists("account_pies"):
            os.mkdir("account_pies")
        p.write_image(f"account_pies/{png_name}")


if __name__ == "__main__":
    account_pie("Savings")
