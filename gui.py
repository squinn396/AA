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

        layout = GridLayout(cols=1)

        header = GridLayout(cols=1, size_hint=(.2, .2))
        account = Label(text=account_name)
        balance = Label(text=f"${str(get_account(get_account_no(account_name))['balance'])}")
        header.add_widget(account)
        header.add_widget(balance)

        # allocations = Allocations(account_name)
        home_button = AccountGoHome()

        layout.add_widget(header)

        ag = GridLayout(cols=1)
        layout.add_widget(ag)

        allocations = get_allocations(get_account_no(account_name))
        print(allocations)

        if not allocations:
            g = GridLayout(cols=1)
            lab = Label(text='There are no allocations')
            b = AddAllocationGrid()

            g.add_widget(lab)
            g.add_widget(b)
            ag.add_widget(g)
        else:
            for allocation in allocations:
                g = GridLayout(cols=1)
                b = ARVButton(text=allocation['name'])

                g.add_widget(b)
                ag.add_widget(g)

        layout.add_widget(home_button)

        a.add_widget(layout)

        self.add_widget(a)

        print('Account Screen Created!')

    def clear_account_screen(self):
        if self.children[1].name != "add_account":
            self.remove_widget(self.children[1])

    def add_allocation_screen(self, allocation_name: str):
        al = AllocationScreen(allocation_name)

        al_info = get_allocation(allocation_name)

        header = GridLayout(Label(text=str(al_info)), cols=1)

        go_ac = AllocationGoAccount()

        al.add_widget(header)
        al.add_widget(go_ac)

        self.add_widget(al)

        print('Allocation screen has been created.')


# screens


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


class AccountScreen(Screen):
    def __init__(self, an):
        super().__init__()
        self.an = an


class AllocationScreen(Screen):
    pass


# screen widgets
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': account} for account in view_accounts2()]


class ARV(RecycleView):
    def __init__(self, account_name, **kwargs):
        super(ARV, self).__init__(**kwargs)
        if get_allocations(get_account_no(self.account_name)):
            self.data = [{'text': allocation['name']} for allocation in
                         get_allocations(get_account_no(account_name))]

        else:
            self.data = []


class AllocationGrid(GridLayout):
    g = 0

    @staticmethod
    def gen(account):
        num = 0
        allocations = get_allocations(get_account_no(account))
        while True:
            yield allocations[num]
            num += 1

    def get_parent(self):
        return self.parent


class Account(GridLayout):
    pass


# navigation


class GoAddAccount(Button):
    pass


class AccountGoHome(Button):
    pass


class AddAccountGoHome(Button):
    pass


class AllocationGoAccount(Button):
    pass


class RVButton(Button):
    pass


class ARV(Button):
    pass


class ARVButton(Button):
    pass


class AddAllocationGrid(GridLayout):
    def make_info(self):
        self.clear_widgets()
        an = Label(text="Allocation Name")
        an_t = TextInput(id="allocation_name")
        ab = Label(text="Balance")
        ab_t = TextInput(id="allocation_balance")

        self.add_widget(an)
        self.add_widget(an_t)
        self.add_widget(ab)
        self.add_widget(ab_t)




# app


class GUIApp(App):
    create_account_table()
    create_allocation_table()

    def build(self):
        wm = WindowManager()

        wm.populate()

        return wm


def run():
    if __name__ == "__main__":
        GUIApp().run()


run()
