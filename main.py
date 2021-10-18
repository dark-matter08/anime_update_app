from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineAvatarIconListItem, ImageLeftWidget
import shelve, os
from scrap import download_webpage # new import
from threading import Thread # new import

class ScreenManagement(ScreenManager):
    pass

class MainWindow(MDScreen):
    def refresh_callback(self, *args):
        print("Refreshing...")

    def get_anime_info(self):
        '''Get the anime info and creates a list item widget and adds it to screen'''
        # open shelve files and get the urls
        with shelve.open('./save_files/mydata') as shelf_file:
            url_list = shelf_file['url_list']

        # download data from each url
        for url in url_list:
            download_webpage(url)

        # after downloading the data and saving it shelve file get the data and display it
        with shelve.open('./save_files/mydata') as shelf_file:
            for key in shelf_file.keys():
                if key != 'url_list':
                    print(key)
                    anime = shelf_file[key]
                    episodes = anime['episodes']
                    completed = anime['completed']
                    image = anime['image']

                    anime_complete = 'completed' if completed else 'ongoing'
                    # create a list item with the data
                    list_item = ThreeLineAvatarIconListItem(text=key, secondary_text=f"[b]Status:[/b] {anime_complete}", tertiary_text=f"[b]Episodes:[/b] {episodes}")
                    #add image to the list item
                    list_item.add_widget(ImageLeftWidget(source=f"./images/{image}"))

                    # finally add the list item to screen
                    self.ids.box.add_widget(list_item)

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
