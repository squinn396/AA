from kivymd.app import MDApp
from objects import *


class GUIApp(MDApp):
    create_account_table()
    create_allocation_table()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        wm = WindowManager()

        wm.populate()

        return wm


def run():
    if __name__ == "__main__":
        GUIApp().run()


run()
