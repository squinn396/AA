from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import NavigationLayout

from objects import *


class GUIApp(MDApp):
    create_account_table()
    create_allocation_table()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        """Screen:
            Toolbar:
            NavigationLayout:
                WindowManager: (it's a ScreenManager)
                    Home:
                    AddAccount:
                MDNavigationDrawer:
                    ContentNavigationDrawer:
                """

        #wm = WindowManager()

        #wm.populate()

        ms = MainScreen()

        print(ms.children[0].children[1])
        ms.children[0].children[1].populate()

        return ms


def run():
    if __name__ == "__main__":
        GUIApp().run()


run()
