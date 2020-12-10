from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.toolbar import MDToolbar

from app import *
from database import *


# ======================================================App Screen=======================
class MainScreen(Screen):
    pass


class MDToolbar():
    pass


# ======================================================Screen Manager=======================


class WindowManager(ScreenManager):
    def populate(self):
        print("WM populate")
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

    def clear_account_screen(self):
        if self.children[1].name != "add_account":
            self.remove_widget(self.children[1])


class ContentNavigationDrawer(GridLayout):
    pass


# =======================================================Home========================


class HomeScreen(Screen):
    def populate(self):
        layout = BoxLayout(orientation='vertical')
        rv = RV()
        aa_btn = GoAddAccount()

        layout.add_widget(rv)
        layout.add_widget(aa_btn)

        self.add_widget(layout)


class HomeToolbar(MDToolbar):
    pass


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
        self.account_name = an

    def populate(self):
        layout = GridLayout(cols=1)  # Change to Float Layout

        allocations = GridLayout(cols=1)
        self.load_tabs(allocations)

        home_button = AccountGoHome()

        account_info = GridLayout(cols=1, size_hint_y=1, id='summary')
        account_info.add_widget(Label(text='Account summary'))

        layout.add_widget(allocations)
        layout.add_widget(account_info)
        layout.add_widget(home_button)
        self.add_widget(layout)

    def load_tabs(self, layout: GridLayout):
        if layout.children:
            layout.clear_widgets()

        allocations = get_allocations(get_account_no(self.account_name))

        if not allocations:
            lab = Label(text='There are no allocations')  # adjust size
            layout.add_widget(lab)
        else:
            tab_bar = MDTabs(id='tabs')

            for allocation in allocations:
                t = Tab(text=allocation['name'])
                tab_bar.add_widget(t)
            layout.add_widget(tab_bar)


class AccountToolbar(MDToolbar):
    pass


class Tab(FloatLayout, MDTabsBase):
    pass


class Account(GridLayout):
    pass


class AccountGoHome(Button):
    pass


# =======================================================Allocation=================================

class AllocationGrid(GridLayout):
    def set_btn_color(self):
        for child in self.children:
            child.reset_color()


class AddAllocationSubmit(Button):
    pass
