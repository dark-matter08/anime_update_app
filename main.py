from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineAvatarIconListItem, ImageLeftWidget
import shelve, os

class ScreenManagement(ScreenManager):
    pass

class MainWindow(MDScreen):
    def refresh_callback(self, *args):
        print("Refreshing...")

# new class
class CustomListItem(OneLineAvatarIconListItem):
    def delete_item(self, text):
        """Delete list item"""
        with shelve.open('./save_files/mydata')as shelf_file:

            url_list = shelf_file['url_list']
            url_list.remove(str(text))
            shelf_file['url_list'] = url_list

        self.parent.remove_widget(self)

class AddUrlScreen(MDScreen):
    def add_url(self, text):
        """Add the url to list and save the url in shelve file"""
        self.ids.linklist.add_widget(CustomListItem(text=text))
        self.ids.linkinput.focus = True
        self.ids.linkinput.text = ''

        # saving to shelve file
        with shelve.open('./save_files/mydata') as shelf_file:
            url_list = shelf_file['url_list']
            url_list.append(str(text))
            shelf_file['url_list'] = url_list

    def on_pre_enter(self):
    '''Load the shelve file with list item from shelve file'''
        try:
            with shelve.open('./save_files/mydata') as shelf_file:
                self.ids.linklist.clear_widgets()
                for item in shelf_file['url_list']:
                    self.ids.linklist.add_widget(CustomListItem(text=item))

        except KeyError:
            with shelve.open('./save_files/mydata') as shelf_file:
                shelf_file['url_list'] = []


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.root.transition= CardTransition() # new line

    def on_start(self):
        try:
            os.mkdir('images')
            os.mkdir('save_files')
        except:
            pass

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
