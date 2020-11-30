from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from app import *
from database import *

# ======================================================Screen Manager=======================


class WindowManager(ScreenManager):
    def populate(self):
        self.add_home_screen()

        aas = AddAccountScreen()
        self.add_widget(aas)

    def add_home_screen(self):
        hs = HomeScreen()
        hs.populate()

        self.add_widget(hs)

    def clear_home_screen(self):
        self.remove_widget(self.children[1])

    def add_account_screen(self, account_name: str):
        a = AccountScreen(an=account_name)
        a.populate()

        self.add_widget(a)

        print('Account Screen Created!')

    def clear_account_screen(self):
        if self.children[1].name != "add_account":
            self.remove_widget(self.children[1])


# =======================================================Home========================


class HomeScreen(Screen):
    def populate(self):
        layout = BoxLayout(orientation='vertical')
        welcome = Label(text='Welcome', size_hint_y=0.2)
        rv = RV()
        aa_btn = GoAddAccount()

        layout.add_widget(welcome)
        layout.add_widget(rv)
        layout.add_widget(aa_btn)

        self.add_widget(layout)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': account} for account in view_accounts2()]


class RVButton(Button):
    pass


class GoAddAccount(Button):
    pass


# =====================================================AddAccount==============


class AddAccountScreen(Screen):
    na_name = ObjectProperty(str)
    na_balance = ObjectProperty(float)

    def add_a(self):
        if self.na_name.text == "":
            empty_name = Popup(title='Unnamed Account', size_hint=(0.4, 0.2))
            empty_name.open()
        else:
            if self.na_balance.text == "":
                self.na_balance = 0
            add_account(name=self.na_name.text, balance=self.na_balance.text)

        print(f'{self.na_name.text} created with a balance of ${self.na_balance.text}')
        self.na_name.text = ""
        self.na_balance.text = ""


class AddAccountGoHome(Button):
    pass


# =======================================================Account====================================


class AccountScreen(Screen):
    def __init__(self, an):
        super().__init__()
        self.an = an

    def populate(self):
        layout = GridLayout(cols=1)  # Change to Float Layout

        header = GridLayout(cols=1, size_hint=(.2, .2), id='header')
        account = Label(text=self.an)
        balance = Label(text=f"${str(get_account(self.an)['balance'])}")

        header.add_widget(account)
        header.add_widget(balance)

        layout.add_widget(header)

        # allocations = Allocations(account_name)
        home_button = AccountGoHome()
        add_allocation_grid = AddAllocationGrid()

        allocations_grid = AllocationGrid(rows=1, size_hint_y=.2)

        allocations = get_allocations(get_account_no(self.an))
        print(allocations)

        if not allocations:
            lab = Label(text='There are no allocations')  # adjust size
            allocations_grid.add_widget(lab)
        else:
            hb = AllocationButton(text='Home', background_color=[0, 1, 0, 1], id='home')
            allocations_grid.add_widget(hb)  # this is a confusing name, change
            for allocation in allocations:
                b = AllocationButton(text=allocation['name'])
                allocations_grid.add_widget(b)

        account_info = GridLayout(cols=1, size_hint_y=1)
        account_info.add_widget(Label(text='Allocation summary'))

        layout.add_widget(allocations_grid)
        layout.add_widget(account_info)
        layout.add_widget(add_allocation_grid)
        layout.add_widget(home_button)
        self.add_widget(layout)


class Account(GridLayout):
    pass


class AccountGoHome(Button):
    pass


# =======================================================Allocation=================================

class AllocationGrid(GridLayout):
    def set_btn_color(self):
        for child in self.children:
            child.reset_color()


class AllocationButton(Button):
    def reset_color(self):
        self.background_color = [1, 1, 1, 1]


class AddAllocationGrid(GridLayout):
    def __init__(self):
        super(AddAllocationGrid, self).__init__()
        self.an_t = None
        self.ab_t = None
        self.ag_t = None
        # self.parent_account = self.p

    def make_info(self):
        self.clear_widgets()

        layout = GridLayout(cols=2)
        an = Label(text="Allocation Name")
        self.an_t = TextInput(id="allocation_name")
        ab = Label(text="Balance")
        self.ab_t = TextInput(id="allocation_balance")
        ag = Label(text="Goal")
        self.ag_t = TextInput(id="allocation_goal")
        submit = AddAllocationSubmit()

        layout.add_widget(an)
        layout.add_widget(self.an_t)
        layout.add_widget(ab)
        layout.add_widget(self.ab_t)
        layout.add_widget(ag)
        layout.add_widget(self.ag_t)
        self.add_widget(layout)
        self.add_widget(submit)

    def create(self):
        add_allocation(name=self.an_t.text, goal=self.ag_t.text, balance=self.ab_t.text,
                       account_id=get_account_no("Test"))


class AddAllocationSubmit(Button):
    pass

