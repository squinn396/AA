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

    def add_account_screen(self, account_name):
        a = AccountScreen()

        layout = GridLayout(cols=1)

        header = GridLayout(cols=1, size_hint=(.2, .2))
        account = Label(text=account_name)
        balance = Label(text=f"${str(get_account(get_account_no(account_name))['balance'])}")
        header.add_widget(account)
        header.add_widget(balance)

        allocations = Allocations(account_name)
        home_button = GoHome()

        layout.add_widget(header)
        layout.add_widget(allocations)
        layout.add_widget(home_button)

        a.add_widget(layout)

        self.add_widget(a)

        print('Account Screen Created!')

    def clear_account_screen(self):
        if self.children[1].name != "add_account":
            self.remove_widget(self.children[1])


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


class AccountScreen(Screen):
    pass


class AddAccountScreen(Screen):
    na_name = ObjectProperty(str)
    na_balance = ObjectProperty(float)

    def add_a(self):
        if self.na_name.text == "":
            empty_name = Popup(title='Unnamed Account', size_hint=(0.4, 0.2))
            empty_name.open()

        print(self.na_name.text, self.na_balance.text)
        self.na_name.text = ""
        self.na_balance.text = ""


# screen widgets


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': account} for account in view_accounts2()]


class Allocations(RecycleView):
    def __init__(self, account_name, **kwargs):
        super(Allocations, self).__init__(**kwargs)
        self.account_name = account_name
        if get_allocations(get_account_no(self.account_name)):
            self.data = [{'text': allocation['name']} for allocation in
                         get_allocations(get_account_no(self.account_name))]

        else:
            self.data = []


class Account(GridLayout):
    pass


# navigation


class GoAddAccount(Button):
    pass


class GoHome(Button):
    pass


class GoHomeAA(Button):
    pass


class RVButton(Button):
    pass


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
