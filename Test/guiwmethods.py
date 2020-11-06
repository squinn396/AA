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

    def refresh_home(self):
        self.remove_widget(self.HomeScreen())
        self.add_home()


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
        self.add_widget(header)


class Account(GridLayout):
    def build(self, button_text):
        header = Label(text=button_text)
        self.add_widget(header)
        print(get_allocations(get_account_no(button_text)))


class AddAccountScreen(Screen):
    na_name = ObjectProperty(None)
    na_balance = ObjectProperty(None)

    def add_a(self):
        add_account(self.na_name.text, self.na_balance.text)
        print(self.na_name.text, self.na_balance.text)
        self.na_name.text = ""
        self.na_balance.text = ""


class RV(RecycleView):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': account} for account in view_accounts2()]


class RVButton(Button):
    def build_screen(self, account_name):
        AS = Account()
        Account.build(AS, button_text=account_name)


class GoAddAccount(Button):
    pass


class GoHome(Button):
    pass


class MethodApp(App):
    create_account_table()
    create_allocation_table()

    def build(self):
        wm = WindowManager()

        wm.populate()

        return wm


def run():
    if __name__ == "__main__":
        MethodApp().run()


run()
