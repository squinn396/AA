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


class HomeScreen(Screen):
    pass


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


class WindowManager(ScreenManager):
    pass


class RV(RecycleView):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': account} for account in view_accounts2()]


class RVButton(Button):
    def build_screen(self, account_name):
        AS = Account()
        Account.build(AS, button_text=account_name)


class GUIApp(App):
    create_account_table()
    create_allocation_table()

    def build(self):
        wm = WindowManager()
        return wm


def run():
    if __name__ == "__main__":
        GUIApp().run()

run()
