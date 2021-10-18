from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineAvatarIconListItem, ImageLeftWidget

class ScreenManagement(ScreenManager):
    pass

class MainWindow(MDScreen):
    def refresh_callback(self, *args):
        print("Refreshing...")

# new class
class CustomListItem(OneLineAvatarIconListItem):
    def delete_item(self, text):
        """Delete list item"""
        self.parent.remove_widget(self)

# modify AddUrlScreen
class AddUrlScreen(MDScreen):
    def add_url(self, text):
        """Add the url to list"""
        self.ids.linklist.add_widget(CustomListItem(text=text)) # new line
        self.ids.linkinput.focus = True
        self.ids.linkinput.text = ''
        # removed print line

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
