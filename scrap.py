import os,sys
import requests
import shelve
from bs4 import BeautifulSoup

def download_webpage(url):
    try:
        # use requests to get the url text
        res = requests.get(url)
        res.raise_for_status()

        # parse the text to BeautifulSoup
        get_soup_text = BeautifulSoup(res.text, features='lxml')

        # download the image
        print("Downloading")
        download_details(get_soup_text)
    except Exception as e:
        print(e)

def download_details(soup_text):
    # get the anime title
    anime_title = soup_text.select('.anime_info_episodes > h2')[0].getText()
    # get the number of episodes
    episodes = soup_text.select('.anime_video_body ul li .active')[0].get('ep_end')
    # get the status
    completed = True if soup_text.find(title = 'Completed Anime') != None else False
    ongoing = True if soup_text.find(title = 'Ongoing Anime') != None else False
    # get the image
    image_elements = soup_text.select('.anime_info_body_bg img')

    if image_elements == []:
        pass
    else:
        # get image source
        image_url = image_elements[0].get('src')
        image = requests.get(image_url)
        image.raise_for_status()

    ## Save details to shelve file
    with shelve.open('./save_files/mydata') as shelf_file:
        file_name = os.path.basename(image_url)

        shelf_file[anime_title] = {
            'episodes': episodes,
            'completed': completed,
            'ongoing': ongoing,
            'image': file_name
            }

    # save the image
    if os.path.exists(f'./images/{file_name}') != True:
        image_file = open(os.path.join('images', file_name), 'wb')
        for chuck in image.iter_content(100000):
            image_file.write(chuck)
        image_file.close()
    else:
        pass
