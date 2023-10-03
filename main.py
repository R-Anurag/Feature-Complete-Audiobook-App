from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, DictProperty
from kivymd.color_definitions import colors
from kivy.core.audio import SoundLoader
from kivymd.uix.slider import MDSlider
from kivy import utils
from kivymd.color_definitions import colors
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.dialog import MDDialog
# from kivy.utils import platform
import os
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton, MDIconButton
import requests
from concurrent.futures import ThreadPoolExecutor
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner.spinner import MDSpinner
import time
from threading import Thread
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
    VariableListProperty,
)
from kivy.metrics import dp
import kivymd.material_resources as m_res
import pickle

# Checking the device platform to manage the download directory

# if platform == 'android':
#     from android.storage import primary_external_storage_path
#     dir = primary_external_storage_path()
#     download_dir_path = os.path.join(dir, 'Download')
# else:
#     download_dir_path = ''
    
# ================================================================= 


KV = '''
#:import utils kivy.utils
#:import colors kivymd.color_definitions.colors


<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height


    MDCardSwipeLayerBox:
        padding: "8dp"
        md_bg_color: utils.get_color_from_hex(colors['DeepOrange']['400'])

        MDIconButton:
            icon: "trash-can"
            theme_icon_color: "Custom"
            icon_color: 1,1,1,0.6
            pos_hint: {"center_y": .5}
            on_release: app.get_running_app().screens.get_screen('menuscreen').remove_item(root)

    MDCardSwipeFrontBox:
        md_bg_color: 1,1,1,0.8

        TwoLineAvatarListItem:
            id: content
            text: root.text
            secondary_text: "Rick Riordan"
            text_color: 1, 1, 1, 1
            secondary_text_color: 1, 2, 1, 1 
            _no_ripple_effect: True
            # bg_color: utils.get_color_from_hex(colors['Purple']['300'])

            ImageLeftWidget:
                source: ""



<ListItemWithCheckbox>:
    _no_ripple_effect: True
    AsyncImage:
        source: root.source
        size_hint: None, None
        size:self.image_ratio*root.height,root.height/1.5
        mipmap: True 
        pos_hint: {'center_x':0.1, 'center_y': 0.5}
     
    MDCheckbox:
        id: checkbox
        checkbox_icon_down: 'checkbox-marked-outline'
        pos_hint: {'center_x':0.92, 'center_y': 0.5}
        size_hint: (None, None)
        size: ("24dp", "24dp")
        selected_color: utils.get_color_from_hex(colors['Green']['700'])
        unselected_color: utils.get_color_from_hex(colors['Gray']['500'])
        disabled_color: utils.get_color_from_hex(colors['Gray']['500'])
        on_state:
            size_label.text = root.mb_text if checkbox.active == True else ""

    MDLabel:
        id: size_label
        text: ""
        halign: "center"
        font_size: 10
        pos_hint: {'center_x':0.92, 'center_y': 0.22}
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 0.8
    

    

<ClickableTextFieldRound>:
    size_hint_y: None

    MDTextField:
        id: text_field
        mode: 'fill'
        font_size: '14sp'
        hint_text: root.hint_text
        text: root.text
        password: False
        fill_color_normal: 1,1,1,0.6
        active_line: True
        radius: 6,6,6,6
        hint_text_color_focus: utils.get_color_from_hex(colors['Purple']['900'])
        text_color_focus: utils.get_color_from_hex(colors['Purple']['900'])
        icon_left_color_focus: utils.get_color_from_hex(colors['Purple']['900'])
        icon_left: "magnify"
        on_focus:
            close_button.icon_color: utils.get_color_from_hex(colors['Purple']['900'])
        on_text: 
            app.screens.get_screen('library').set_list_md_icons(self.text.lower(), True)
            
    MDIconButton:
        id: close_button
        icon: "close"
        icon_size: "16sp"   
        theme_icon_color: "Custom"
        icon_color: 0,0,0,0.8
        ripple_scale: .5
        pos_hint: {"center_y": .7}
        pos: text_field.width - self.width + dp(8), 0.5
        on_release:
            text_field.text=''
            # self.icon = "pencil" if self.icon == "close" else "close"
            # text_field.password = False if text_field.password is True else True


MDScreenManager:
    MenuScreen
    PlayScreen
    
    
    

<MenuScreen>
    name: 'menuscreen'
    back_color: '200'
    search_label_color: '200'
    audiobook_primary_text: 'No audiobooks found in the library'
    audiobook_secondary_text: 'Click the + button to insert local audiobooks or download avaialable audiobooks from the server'
    gif_source: "assets/images/catplayingdark.zip"

    canvas.before:
        Color:
            rgba: eval(f"utils.get_color_from_hex(colors['DeepPurple']['A700'])")
        Rectangle:
            pos: self.pos
            size: self.size
            

    MDFloatLayout:
        id: floatlayout_id
        Image:
            id: background_gif
            source: root.gif_source
            size_hint: (0.3, 0.3)
            pos_hint: {"center_x": 0.8, "center_y": 0.95} 
            anim_delay: 0.1
            minimap: True
            allow_stretch: True
        
        MDScrollView:
            size_hint: (0.98, 0.81)
            pos_hint: {"center_x": 0.5, "center_y": 0.41} 
            MDList:
                id: md_list
                padding: 0

        MDFloatingActionButtonSpeedDial:
            id: speed_dial
            # icon: "open-in-app"
            # markup: True
            data: root.data
            root_button_anim: True
            hint_animation: True
            label: True
            label_text_color: "black"
            label_bg_color: "orange"
            bg_hint_color: 1,0,1,1
            bg_color_root_button: utils.get_color_from_hex(colors['Purple']['500'])
            bg_color_stack_button: utils.get_color_from_hex(colors['Purple']['500'])
        
        MDLabel:
            font_size: self.width/8.5
            bold: True
            text:'Search' 
            font_name: "assets/fonts/try2.ttf"
            halign: 'left'
            pos_hint: {'center_x':0.55, 'center_y':0.93}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors['Purple'][root.search_label_color])  

        MDLabel:
            font_size: self.width/20
            bold: True
            text: root.audiobook_primary_text
            # font_name: "assets/fonts/Aclonica.ttf"
            halign: 'center'
            size_hint_x: 0.9
            pos_hint: {'center_x':0.5, 'center_y':0.54}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors['Gray']['400'])  
        
        MDLabel:
            font_size: self.width/30
            bold: True
            text: root.audiobook_secondary_text
            # font_name: "assets/fonts/Aclonica.ttf"
            halign: 'center'
            size_hint_x: 0.8
            pos_hint: {'center_x':0.5, 'center_y':0.49}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors['Gray']['300'])  
        
        ClickableTextFieldRound:
            id: search_field
            size_hint_x: None
            width: root.width/1.02
            height: root.height/20
            hint_text: "Author, title or series" 
            pos_hint: {"center_x": .5, "center_y": .85}
            on_text: root.set_list_md_icon(self.text, True)        

        

<PlayScreen>
    name: 'playscreen'
    bg_source: 'assets/images/dayreading.png'

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: self.bg_source
        
    MDFloatLayout:
        id: playerpart
        size_hint: 1, 0.8
        pos_hint: {"center_x": .5, "center_y": .6}
        orientation: 'horizontal'

        MagicCard:
            radius: [10, ]
            padding: "2dp"
            ripple_behavior: True
            elevation: 10
            orientation: "vertical"
            size_hint: (.9, .8)
            focus_behavior: False
            pos_hint: {"center_x": .5, "center_y": .45}
            md_bg_color: (0, 0, 0, 0.5)

        FitImage:
            size_hint: (0.80, 0.5)
            source: "assets/images/nightreading.jpg"
            radius: (6, 6, 6, 6)
            pos_hint: {"center_x": .5, "center_y": .55}
        
        MySlider:
            id: slider
            color: (1, 1, 1, 1)
            thumb_color_active: "white"
            thumb_color_inactive: "black"
            min: 0
            sound: None
            max: 0
            value: 0
            pos_hint: {'center_x': 0.50, 'center_y': 0.26}
            size_hint: (0.88, 0.1)        
            hint: True
            track: True
            track_color_active: (1, 0, 0, 1)
            track_color_inactive: (1,0,1,1)  

        MDBoxLayout:
            orientation: "horizontal"
            padding: (0,8,0,0)
            size_hint: 0.8, None
            height: self.minimum_height
            pos_hint: {'center_x': 0.50, 'center_y': 0.23}

            MDLabel:
                text: "0.0"
                font_size: 14
                halign: "left"
                # theme_text_color: "Hint"
                theme_text_color: "Custom"
                text_color: 1,1,1,1

            
            MDLabel:
                text: "1.0"
                font_size: 14
                halign: "right"
                # theme_text_color: "Hint"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
            
        MDFloatLayout:
            size_hint: 0.8, None
            pos_hint: {'center_x': 0.50, 'center_y': 0.25}
            
            MDIconButton:
                icon: "rewind-10"
                icon_size: "28sp" 
                pos_hint: {'center_x': 0.30, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1

            MDIconButton:
                icon: "play-circle"
                icon_size: "48sp" 
                pos_hint: {'center_x': 0.50, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1
                on_release:
                    self.icon = "pause-circle" if self.icon == "play-circle" else "play-circle"


            MDIconButton:
                icon: "fast-forward-10"
                icon_size: "28sp"  
                pos_hint: {'center_x': 0.70, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1 
            
            MDIconButton:
                icon: "replay"
                icon_size: "28sp"  
                pos_hint: {'center_x': 0.05, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1 

            MDIconButton:
                icon: "repeat"
                theme_icon_color: "Custom"
                icon_color: utils.get_color_from_hex(colors['Gray']['100'])
                icon_size: "28sp"  
                pos_hint: {'center_x': 0.95, 'center_y': 0}
                on_release:
                    self.icon_color = utils.get_color_from_hex(colors['Green']['500']) if self.icon_color == utils.get_color_from_hex(colors['Gray']['100']) else utils.get_color_from_hex(colors['Gray']['100'])
                                                                 
                
    
    MDFloatLayout:
        MDIconButton:
            icon: "lightbulb-on"
            icon_size: "20sp"   
            theme_icon_color: "Custom"
            icon_color: utils.get_color_from_hex(colors['Lime']['500'])  
            md_bg_color: 0, 0, 0, 0.3
            pos_hint: {"center_x": .9, "center_y": .05}
            on_release:
                self.icon = "lightbulb-off-outline" if self.icon == "lightbulb-on" else "lightbulb-on"
                self.icon_color = utils.get_color_from_hex(colors['Gray']['500']) if self.icon_color == utils.get_color_from_hex(colors['Lime']['500']) else utils.get_color_from_hex(colors['Lime']['500']) 
                app.switch_theme_style()
                self.parent.parent.bg_source = 'assets/images/nightreading.jpg' if self.parent.parent.bg_source == 'assets/images/dayreading.png' else "assets/images/dayreading.png"


                

'''

# for searchbar in library
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()



class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    source = ObjectProperty()
    mb_text = StringProperty()
    _txt_right_pad = NumericProperty("0dp")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._txt_right_pad = dp(10) + m_res.HORIZ_MARGINS
    

class MagicCard(MagicBehavior, MDCard):
    pass

class MySlider(MDSlider):
    sound = ObjectProperty(None)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            # call super method and save its return
            ret_val = super(MySlider, self).on_touch_up(touch)

            # adjust position of sound
            self.sound.seek(self.max * self.value_normalized)

            # if sound is stopped, restart it
            if self.sound.state == 'stop':
                MDApp.get_running_app().screens.get_screen('playscreen').start_play()

            # return the saved return value
            return ret_val
        else:
            return super(MySlider, self).on_touch_up(touch)


class PlayScreen(MDScreen):

    def on_enter(self, *args):
         self.a = SoundLoader.load('test.mp3')
         self.updater = None
         self.start_play()
        
    def start_play(self, *args):
        # play the sound
        self.a.play()
        if self.updater is None:
            # schedule updates to the slider
            self.updater = Clock.schedule_interval(self.update_slider, 0.5)

    def update_slider(self, dt):
        # update slider

        # if the sound has finished, stop the updating
        if self.a.state == 'stop':
            print('stopped')
            self.updater.cancel()
            self.updater = None



class MenuScreen(MDScreen):

    data = DictProperty()
    content_dict = DictProperty()
    icon_image_dict = DictProperty()


    def on_enter(self, *kwargs):              

        self.data = {
                'Switch mode': [
                    'lightbulb-on',
                    "on_release", lambda x: self.callback(x),
                ],
                'Add Audiobook': [
                    'attachment-plus',
                    "on_release", lambda x: self.callback(x),     
                ],
            }
        
        returned_response = requests.session().get(r'https://raw.githubusercontent.com/R-Anurag/kivy-audiobook-app/main/assets/links/book%20link%20dict.yaml',headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}) 
        

        import yaml
        yaml_book_link = returned_response.content 
        self.dict_book_link = yaml.safe_load(yaml_book_link)

        
    def remove_item(self, instance):
        MDApp.get_running_app().screens.get_screen('menuscreen').ids.md_list.remove_widget(instance)

    def callback(self, x):

        screen_accessed = MDApp.get_running_app().screens.get_screen('menuscreen')

        if x.icon != 'attachment-plus':

            if x.icon == 'lightbulb-on':
                x.icon = 'lightbulb-off-outline'
                x.icon_color = utils.get_color_from_hex(colors['Gray']['500']) 
                screen_accessed.search_label_color = '200'
                screen_accessed.back_color = '900'
                screen_accessed.gif_source = 'assets/images/catplayingdark.zip'

            else:
                x.icon = 'lightbulb-on'
                x.icon_color: utils.get_color_from_hex(colors['Lime']['500']) 
                screen_accessed.search_label_color = '900'
                screen_accessed.back_color = '200'
                screen_accessed.gif_source = 'assets/images/catplaying.zip'
        
        else:

            self.show_download_list()

    def add_card(self):

        if not MDApp.get_running_app().screens.get_screen('menuscreen').ids.download_list.children:
            print(MDApp.get_running_app().screens.get_screen('menuscreen').ids)

            # self.manager.get_screen('menuscreen').ids.download_list.add_widget(MagicCard())

    def show_download_list(self, *kwargs):

        already_downloaded_audiobooks = []
        if os.path.isfile("app_data/downloaded_audiobooks.dat"):
            
            with (open("app_data/downloaded_audiobooks.dat", "rb")) as openfile:
                while True:
                    try:
                        already_downloaded_audiobooks.append(pickle.load(openfile))
                    except EOFError:
                        break
        print(already_downloaded_audiobooks)
        dialog_items = []
        
        for i in self.dict_book_link.keys():

            if i not in already_downloaded_audiobooks:
                
                dialog_items.append(ListItemWithCheckbox(text = f'[size=14][font=DejaVuSans]{i.title()}[/font][/size]',
                                                secondary_text=f"[size=12][font=assets/fonts/Roboto-LightItalic.ttf]{self.dict_book_link[i][0].title()}[/font][/size]",
                                                source=self.dict_book_link[i][1],
                                                mb_text=self.dict_book_link[i][3],
                                                divider='Inset',   
                                                divider_color=utils.get_color_from_hex(colors['Purple']['200'])))
        
            
        self.dialogx = MDDialog(
            size_hint=(0.90, None),
            md_bg_color=[1,1,1,0.7],
            title = "[font=assets/fonts/Aclonica.ttf][size=18][b]Download Audiobooks?[/b][/size][/font]",
            text = "[size=16]Select the ones you want to download[/size]",
            elevation = 4,
            radius = [20, 7, 20, 7],
            padding = 0, 
            type = 'confirmation',
            items = dialog_items,
            buttons = [
                MDRectangleFlatIconButton(
                    icon='close',
                    md_bg_color = utils.get_color_from_hex(colors['Purple']['500']),
                    theme_text_color="Custom",
                    icon_color=[1,1,1,0.9],
                    text_color=[1,1,1,0.9],
                    line_color=[.2,.2,.2,0.85],
                    text="[font=assets/fonts/Aclonica.ttf][size=14][b]CANCEL[/b][/size][/font]",
                    padding=[4,4],
                    on_release = lambda x: self.dialogx.dismiss()
                    
                ),
                MDRectangleFlatIconButton(
                    icon='thumb-up',
                    text="[font=assets/fonts/Aclonica.ttf][size=14][b]OK[/b][/size][/font]",
                    md_bg_color = utils.get_color_from_hex(colors['Purple']['500']),
                    theme_text_color="Custom",
                    icon_color=[1,1,1,0.9],
                    text_color=[1,1,1,0.9],
                    line_color=[.2,.2,.2,0.85],
                    padding=[4,4],
                    on_press = self.get_active_boxes,
                ),
            ])
        
        self.dialogx.open()


    def get_active_boxes(self, *kwargs):
        

        #Storing the active checkboxes in a list
        self.mdlist_items = self.dialogx.children[0].children[2].children[0].children
        self.selected_books = [i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower() for i in self.mdlist_items if i.children[1].active == True]
    
        
        #This is a list containing nested list for downloading 
        complete_url_list_with_filepath = []
        for i in self.dict_book_link.keys():
            for j in self.dict_book_link[i][2].keys():
                if i in self.selected_books:
                    complete_url_list_with_filepath.append([i.lower(), j.lower(), self.dict_book_link[i][2][j], self.dict_book_link[i][3] ])
        
        
        #Forming a dictionary to store the size of audiobook and current_downloaded_size
        self.downloading_size_dict = {}
        for i in self.selected_books:

            self.downloading_size_dict[f"{i}_full_size"] = int(self.dict_book_link[i][3].replace('MB', ''))
            
            self.downloading_size_dict[f"{i}_downloaded_size"] = 0
           
        
        #Deleting the ok and cancel button 
        for i in list(self.dialogx.children[0].children[0].children[0].children):
            self.dialogx.children[0].children[0].children[0].remove_widget(i)
        

        # Removing the Checkbox from the selected items
        for i in self.mdlist_items:
            if i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower() in self.selected_books:
                    i.remove_widget(i.children[1])
            else:
                i.ids.checkbox.disabled = True
                i.ids.checkbox.checkbox_icon_normal = "checkbox-blank-off"



        # adding the spinner to selected items from the dialog list
        for i in self.mdlist_items:
            if i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower() in self.selected_books:
                i.add_widget(
                    MDSpinner(size_hint=(None, None), size=(dp(24), dp(24)), pos_hint={"center_x":0.92, "center_y":0.5}, active=True, line_width=dp(3), palette=[
                        [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                        [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                        [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                        [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                    ])
                )      

        # Adding the Downloading label button to MDDialog
        self.label_button = MDRaisedButton(
            text="", 
            md_bg_color=utils.get_color_from_hex(colors['DeepPurple']['A400']), font_size="12sp",
            theme_text_color="Custom", text_color=utils.get_color_from_hex(colors['Gray']['200']), padding=[8,0], elevation=None, ripple_scale=0, size_hint=(None, None), size=(100, 20)
            )
        
        self.dialogx.children[0].children[0].children[0].add_widget(self.label_button)
        
            
        #Adding downloading percentage label to md_list
        for i in self.mdlist_items:
            if i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower() in self.selected_books:
                
                var_name = i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower()
                
                i.add_widget(
                    MDLabel(
                        text="[size=10]"+str(self.downloading_size_dict[f"{var_name}_downloaded_size"])+"[/size]",
                        halign="center",
                        markup=True,
                        pos_hint={'center_x':0.82, 'center_y': 0.22},
                        theme_text_color="Custom",
                        text_color=utils.get_color_from_hex(colors['Green']['700'])
                    )
                )
                
                       
        
        self.thread = Thread(target=self.thread_pool_download_function, args=(complete_url_list_with_filepath, self.mdlist_items))
        # run the thread
        self.thread.start()

        self.downloaded_audiobooks = []
        Clock.schedule_interval(self.check_downloaded_status, 1)


    def check_downloaded_status(self, *args):

        for i in self.mdlist_items:

            variable = i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower()
            
            if variable in self.selected_books and variable not in self.downloaded_audiobooks:
                
                if not self.downloading_size_dict[f"{variable}_downloaded_size"] < self.downloading_size_dict[f"{variable}_full_size"] - 2:
                     
                    
                    self.downloaded_audiobooks.append(variable)

                    i.remove_widget(i.children[1])

                    i.add_widget(
                         MDIconButton(
                            icon="checkbox-marked-circle",
                            pos_hint={"center_x":0.92, "center_y":0.5},theme_icon_color="Custom",
                            icon_color=utils.get_color_from_hex(colors['Green']['700'])
                         )
                    )

        if self.selected_books == self.downloaded_audiobooks:
            with open(r"app_data/downloaded_audiobooks.dat", "ab") as file:
                for i in self.selected_books:
                    pickle.dump(i, file)
            Clock.unschedule(self.check_downloaded_status)

    
    def thread_pool_download_function(self, complete_url_list_with_filepath, mdlist_items):

        
        def get_confirm_token(response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value

            return None
            

        def download_file(url_filepath_list):
            
            session = requests.Session()
        
            response = session.get(url_filepath_list[2], params = { 'id' : id }, stream = True)
            token = get_confirm_token(response)
            
            if token:
                params = { 'id' : id, 'confirm' : token }
                response = session.get(url_filepath_list[2], params = params, stream = True)

            save_response_content(response, url_filepath_list)
        
        def save_response_content(response, url_filepath_list):


            # download_filder_path contains the name of the file as well
            download_folder_path = os.path.join(r'app data/audiobooks', url_filepath_list[0]) 

            if not os.path.exists(download_folder_path):
                os.makedirs(download_folder_path)


            filename = url_filepath_list[1]

            CHUNK_SIZE = 32768
            with open(os.path.join(download_folder_path, filename)+'.mp3', "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk: 

                        self.downloading_size_dict[f"{url_filepath_list[0].lower()}_downloaded_size"] += len(chunk)/(1024*1024)
                        f.write(chunk)

                        combined_downloaded_size = sum([ self.downloading_size_dict[i] for i in self.downloading_size_dict.keys() if i.endswith("_downloaded_size") ])

                        combined_full_size = sum([ self.downloading_size_dict[i] for i in self.downloading_size_dict.keys() if i.endswith("_full_size") ])

                        combined_download_percentage = combined_downloaded_size / combined_full_size * 100
     

                        update_downloading_perc_label(self.downloading_size_dict[f"{url_filepath_list[0].lower()}_downloaded_size"], url_filepath_list[0], combined_download_percentage, self.downloading_size_dict[f"{url_filepath_list[0].lower()}_full_size"], self.dialogx, self.mdlist_items)

                

            
        def update_downloading_perc_label(downloaded_size, received_name, download_percentage, full_size, download_dialog, mdlist_items):


            req_label_widget = [i for i in mdlist_items if i.text.replace('[size=14][font=DejaVuSans]','').replace('[/font][/size]','').lower() == received_name.lower() ][0].children[0]

            req_label_button_widget = self.label_button
            
        
            req_label_widget.text =  "[size=10]" + str(f"{round(downloaded_size,1)}") + "/" + "[/size]" 

                    
            #Updating the button label in MDDialog box
            if download_percentage < 99.7:
                req_label_button_widget.text = "[font=assets/fonts/try4.ttf]Downloading... [/font]" + f"[b]{round(download_percentage,1)}%[/b]"
            else:
                for i in range(5,0,-1):
                    req_label_button_widget.text = "[font=assets/fonts/try4.ttf]Download Finished! [/font]" + f"[b]{100.0}%[/b]" + f"\n[font=assets/fonts/try4.ttf][i]This Dialog box will self close in[/i][/font] [b]{i}[/b]"
                
                    time.sleep(1)

                download_dialog.dismiss()

                
                # import threading
                # print(threading.active_count())
                # #using an exec statement to stop the threading
                # if self.thread.is_set():
                #     return
                
        with ThreadPoolExecutor() as executor:
            executor.map(download_file, complete_url_list_with_filepath)
        
    

sm = MDScreenManager()
sm.add_widget(MenuScreen(name='menuscreen'))
sm.add_widget(PlayScreen(name='playscreen'))


class MainApp(MDApp):


    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        try:
            MDApp.get_running_app().screens.get_screen('menuscreen').stop.set()
        except:
            pass        


    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Light"



        self.screens = Builder.load_string(KV)
        return self.screens
    
    
    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
   
    def on_start(self):
         for i in range(20):
            MDApp.get_running_app().screens.get_screen('menuscreen').ids.md_list.add_widget(
                SwipeToDeleteItem(text=f"One-line item {i}",
                md_bg_color=(1,2,1,1 ))
            )

MainApp().run()