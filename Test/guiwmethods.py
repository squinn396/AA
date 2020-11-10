from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from app import *
from database import *


class WindowManager(ScreenManager):
    def populate(self):
        self.add_home()

        aas = AddAccountScreen()
        self.add_widget(aas)

    def add_home(self):
        hs = HomeScreen()
        hs.populate()

        self.add_widget(hs)

    def clear_home(self):
        print(self.children[1])
        self.remove_widget(self.children[1])

    def add_account_screen(self, account_name):
        a = AccountScreen()
        a.build(account_name)

        self.add_widget(a)

        print('Account Screen Created!')


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
    def build(self, button_text):
        header = Label(text=button_text)

        allocations = Allocations(button_text)

        home_button = GoHome()

        self.add_widget(header)
        self.add_widget(allocations)

        if self.children[0] == []:
            btn = Button(text='No allocations for this account')
            self.add_widget(btn)

        self.add_widget(home_button)

class AddAccountScreen(Screen):
    na_name = ObjectProperty(None)
    na_balance = ObjectProperty(None)

    def add_a(self):
        add_account(self.na_name.text, self.na_balance.text)
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
            self.data = [{'text': allocation} for allocation in get_allocations(get_account_no(self.account_name))]

        else:
            self.data = []


class Account(GridLayout):
    def build(self, button_text):
        header = Label(text=button_text)
        self.add_widget(header)
        print(get_allocations(get_account_no(button_text)))


# navigation


class GoAddAccount(Button):
    pass


class GoHome(Button):
    pass


class RVButton(Button):
    pass


# app


class MethodApp(App):
    create_account_table()
    create_allocation_table()

    def build(self):
        wm = WindowManager()

        wm.populate()
        print(wm.children)

        return wm


def run():
    if __name__ == "__main__":
        MethodApp().run()


run()
