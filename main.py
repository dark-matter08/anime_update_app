from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen

class ScreenManagement(ScreenManager):
    pass

class MainWindow(MDScreen):
    def refresh_callback(self, *args):
        print("Refreshing...")


class AddUrlScreen(MDScreen):
    def add_url(self, text):
        """Add the url to list and save the url in shelve file"""
        self.ids.linkinput.focus = True
        self.ids.linkinput.text = ''
        print(text)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.root.transition= CardTransition() # new line

    #define methods to switch between screens
    def open_settings_screen(self):
        """open setting window"""
        self.root.current = 'addurl'
        self.root.transition.direction = 'down'

    # new method
    def return_to_main_window(self):
        self.root.current = 'mainscreen'
        self.root.transition.direction = 'up'


if __name__ == "__main__":
    app = MainApp()
    app.run()
