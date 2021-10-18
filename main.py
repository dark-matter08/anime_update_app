from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

class ScreenManagement(ScreenManager):
    pass

class MainWindow(MDScreen):
    def refresh_callback(self, *args):
        print("Refreshing...")


class AddUrlScreen(MDScreen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"

if __name__ == "__main__":
    app = MainApp()
    app.run()
