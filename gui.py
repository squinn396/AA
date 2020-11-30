from objects import *


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
