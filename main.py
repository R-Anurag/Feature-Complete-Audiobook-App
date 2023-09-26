from kivy.lang import Builder
from kivymd.app import MDApp
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
from kivy.utils import platform
import os
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.network.urlrequest import UrlRequest
import zipfile
import threading
import time
import io
import requests


# Checking the device platform to manage the download directory

if platform == 'android':
    from android.storage import primary_external_storage_path
    dir = primary_external_storage_path()
    download_dir_path = os.path.join(dir, 'Download')
else:
    download_dir_path = ''
    
# ================================================================= 


KV = '''
#:import utils kivy.utils
#:import colors kivymd.color_definitions.colors


<ListItemWithCheckbox>:
    _no_ripple_effect: True

    AsyncImage:
        source: root.source
        size_hint: (0.95,0.6)
        pos_hint: {'center_x':0.05, 'center_y': 0.5}
        
    MDCheckbox:
        checkbox_icon_down: 'checkbox-marked-outline'
        selected_color: [0.2,0.6,1,1]
        unselected_color: app.theme_cls.primary_color
        disabled_color: app.theme_cls.primary_color
        pos_hint: {'center_x':0.92, 'center_y': 0.5}
        size_hint: (None, None)
        size: "24dp", "24dp"

    

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
    search_label_color: '900'
    gif_source: "assets/images/catplaying.zip"

    canvas.before:
        Color:
            rgba: eval(f"utils.get_color_from_hex(colors['Purple']['{self.back_color}'])")
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
            font_size: self.width/12
            bold: True
            text:'Search' 
            font_name: "assets/fonts/Aclonica.ttf"
            halign: 'left'
            pos_hint: {'center_x':0.55, 'center_y':0.94}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors['Purple'][root.search_label_color])  
        
        ClickableTextFieldRound:
            id: search_field
            size_hint_x: None
            width: root.width/1.1
            height: root.height/20
            hint_text: "Author, title or series" 
            pos_hint: {"center_x": .5, "center_y": .84}
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


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    source = ObjectProperty()

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

        self.dialogx = None           

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
        

        # self.book_link_dict = {
            
        #     'the lightning thief' : {
        #         'part 1': 'https://drive.google.com/file/d/1myykN1CC520dFhvBzM7oM6bGY0cNpAbU/view?usp=sharing',
        #         'part 2': 'https://drive.google.com/file/d/17g55Uijk4X_2Wc-U37xCqj9PkJCX9x6z/view?usp=sharing', 
        #         'part 3': 'https://drive.google.com/file/d/1uP4wO0u94aXYQ-nHmicc117PajzVR2PP/view?usp=sharing', 
        #         'part 4': 'https://drive.google.com/file/d/1QuWRoTiOLBvoJadjrhfFqYA4CHG59uqd/view?usp=sharing',
        #         'part 5': 'https://drive.google.com/file/d/1j6katSD6mSlKZIWIjplbZ_X39KAtiidq/view?usp=sharing', 
        #         'part 6': 'https://drive.google.com/file/d/1bDZ5WU5g9t_uuXDQl0RJc2Tl5pebZLBp/view?usp=sharing', 
        #         'part 7': 'https://drive.google.com/file/d/1lBPfLgfgyqNMa4_Y-7SKVhpR0KRcuB05/view?usp=sharing', 
        #         'part 8': 'https://drive.google.com/file/d/1afK5jE9b3pSmGOuZ6S158SNZ27vsTKiA/view?usp=sharing', 
        #         'part 9': 'https://drive.google.com/file/d/1qZqBbarDT6w6GNvrP9PV4YKOY2PKs8dF/view?usp=sharing',
        #         'part 10': 'https://drive.google.com/file/d/1rQ45EilX2GPOi3Y78lgL4rxULdLi9lwB/view?usp=sharing', 
        #         'part 11': 'https://drive.google.com/file/d/1DanUoeiJfDYPMiYwuxktPilxNmywbphY/view?usp=sharing', 
        #         'part 12': 'https://drive.google.com/file/d/1GBMu9tqi1-Yf9FZDGAeY-eV9eOznX5Ax/view?usp=sharing'
        #     },

        #     'the sea of monsters' : {
        #         'part 1': 'https://drive.google.com/file/d/1X2C7KlZJiaURwFfid31OXa7jhGmjVCYi/view?usp=sharing', 
        #         'part 2': 'https://drive.google.com/file/d/1UlfrDGwhybsotiBt2HENBDiwNJ1yUs9H/view?usp=sharing',
        #         'part 3': 'https://drive.google.com/file/d/1x5aBAzo6J9NuqGSVsGyao4nK3fG8SlPa/view?usp=sharing', 
        #         'part 4': 'https://drive.google.com/file/d/1CFrCQM5hH0IQJE7XjUYgwGOiqTzQURx3/view?usp=sharing', 
        #         'part 5': 'https://drive.google.com/file/d/1lDqO39fk0mQlTBlS4NQtWbRMlnGfmg9-/view?usp=sharing', 
        #         'part 6': 'https://drive.google.com/file/d/10MmXi3WG7OYDV3iWWFkgZcZISJRPR_b_/view?usp=sharing', 
        #         'part 7': 'https://drive.google.com/file/d/1U4L6wJpPrNjpQIl7RXIvJcLKs_RU4d3T/view?usp=sharing', 
        #         'part 8': 'https://drive.google.com/file/d/1I-4Ctn97kplkxW6ybJu5r-iOFkk4nhv1/view?usp=sharing'
        #     },

        #     'the battle of labyrinth' : {
        #         'part 1': 'https://drive.google.com/file/d/1z1dkadBpjYvzGdRgIbaAg8iO9FXRf0jL/view?usp=sharing',
        #         'part 2': 'https://drive.google.com/file/d/1Nl5DFf48v0ITR6M78S64Dj9Q2dUZArsH/view?usp=sharing', 
        #         'part 3': 'https://drive.google.com/file/d/1_8wFXHVsUJarS9GDxKkVHtvsyXkcAKDh/view?usp=sharing', 
        #         'part 4': 'https://drive.google.com/file/d/1tDfFRYbiUBhZWG4NMIK83vWM17UuDFg4/view?usp=sharing',
        #         'part 5': 'https://drive.google.com/file/d/12vBkNAaMcejPvalDydhJvHncShBRZKkx/view?usp=sharing', 
        #         'part 6': 'https://drive.google.com/file/d/1SUJNml3SpICYAjiScUzpSH0lJ10q9MLy/view?usp=sharing', 
        #         'part 7': 'https://drive.google.com/file/d/1xshTkzbINu9fEt_ccwqtinaYl-Suke_P/view?usp=sharing', 
        #         'part 8': 'https://drive.google.com/file/d/18UzF2su1-MSGhL3RwrBA-2q85mWGnyP6/view?usp=sharing', 
        #         'part 9': 'https://drive.google.com/file/d/1q38EyYEc9g_S8Yq9izbxgnnk6ULLbfni/view?usp=sharing',
        #         'part 10': 'https://drive.google.com/file/d/181vyPFDYjgrbAMmidtmpwXcD-Q57V76y/view?usp=sharing', 
        #         'part 11': 'https://drive.google.com/file/d/1lg0W0Gx_Wd_gyn27uVO1gg5CIlEO4TVX/view?usp=sharing'
        #     },

        #     'the titan\'s curse' : {
        #         'part 1': 'https://drive.google.com/file/d/1d-JFaAQ-AclooLsoMus2e7OEfmaXzKXs/view?usp=sharing', 
        #         'part 2': 'https://drive.google.com/file/d/1mQnKGbA45WTSZG6beK2g29-D-wRTqNZ6/view?usp=sharing', 
        #         'part 3': 'https://drive.google.com/file/d/1aTXJpDplPM-UkpEf9Mz1MnkFbWhp69Pb/view?usp=sharing', 
        #         'part 4': 'https://drive.google.com/file/d/1_nS_Hli1YimaSO_GaeVoowxfay_Ygw9d/view?usp=sharing', 
        #         'part 5': 'https://drive.google.com/file/d/153JZfeZa3GDRYEho8iX07OldGlq3qNYD/view?usp=sharing', 
        #         'part 6': 'https://drive.google.com/file/d/1ZJPm0CE5FKs0nPL0_eg4kK81MoWu2qI4/view?usp=sharing', 
        #         'part 7': 'https://drive.google.com/file/d/1vajjFlobJ7WsY2x8my1WpVvLd9OtIaQ8/view?usp=sharing', 
        #         'part 8': 'https://drive.google.com/file/d/1AuWqkZ-fMb21xpMqoOUWWX8WMsDoriaC/view?usp=sharing',
        #         'part 9': 'https://drive.google.com/file/d/1jo9HGW-uSMQppqCEBVl-HhXVV1mefNju/view?usp=sharing'
        #     },

        #     'the last olympian' : {
        #         'part 1': 'https://drive.google.com/file/d/1HXOucheuBxPXbRdghXYiENbGfAmTs6pk/view?usp=sharing',
        #         'part 2': 'https://drive.google.com/file/d/16bJ93ZG_YBjZ7oSmZkG0wyZ_gp2wDKgR/view?usp=sharing', 
        #         'part 3': 'https://drive.google.com/file/d/1OKn0P3FN4Bt-7BiidQRk-Y909AcButAS/view?usp=sharing',
        #         'part 4': 'https://drive.google.com/file/d/1EYYJ2PgVdH4ezgkrs4autTFJoCuDV7eO/view?usp=sharing', 
        #         'part 5': 'https://drive.google.com/file/d/1zoaP9PTHOsthrJC2xZX5v-TwJ6e1sIG-/view?usp=sharing', 
        #         'part 6': 'https://drive.google.com/file/d/149wwBnrTOmMWPjlTMgVo4x4x72t_wsaa/view?usp=sharing',
        #         'part 7': 'https://drive.google.com/file/d/1Z6YPJhAJrCVbch0rZSdcaNgBiWk4YX_z/view?usp=sharing', 
        #         'part 8': 'https://drive.google.com/file/d/11v515vx1JHaK3UA44pEhuZ1PkYiK21V5/view?usp=sharing',
        #         'part 9': 'https://drive.google.com/file/d/1Y2-hmaZCrTxZ-8zaugW1G2bwPc0nJf4M/view?usp=sharing', 
        #         'part 10': 'https://drive.google.com/file/d/1zn7zM-azTyJGGph-UGW_wHGsKNiX1PeN/view?usp=sharing', 
        #         'part 11': 'https://drive.google.com/file/d/1MxRAmmRfWiPwGHjnCRJb0Xd18MXqJ9sS/view?usp=sharing',
        #         'part 12': 'https://drive.google.com/file/d/1iuMRDb1de49Bn6RpC38cHA-rtu-XDg0c/view?usp=sharing'
        #     }

        # }


        self.book_name_dict = {
            'the lightning theif' : ['https://m.media-amazon.com/images/I/51SOMFPQ69L.jpg', 'not downloaded', 'Rick Riordan', 'https://drive.google.com/file/d/1GhR3evadmL2b3vbj1nconmAF_uzufutv/view?usp=sharing'],
            'the sea of monsters' : ['https://m.media-amazon.com/images/I/51ui+BmTrqL.jpg', 'not downloaded', 'Rick Riordan', 'https://drive.google.com/file/d/1mEcxuPzGScDuIbwjP9x2ofR6G4nZsm5o/view?usp=sharing'],
            'the battle of labyrinth' : ['https://m.media-amazon.com/images/I/51JqintVoTL.jpg', 'not downloaded', 'Rick Riordan', 'https://drive.google.com/file/d/1GcWm-YlgHq9XM06m_owBB-BnDDXi040_/view?usp=sharing'],
            'the titan\'s curse' : ['https://m.media-amazon.com/images/I/51q9kr8AroL.jpg', 'not downloaded', 'Rick Riordan', 'https://drive.google.com/file/d/1vArbVlwYhA9b2hMT2M9rM20SNudy1o8P/view?usp=sharing'],
            'the last labyrinth' : ['https://m.media-amazon.com/images/I/511BtjZ4VnL.jpg', 'not downloaded', 'Rick Riordan', 'https://drive.google.com/file/d/1ZbK5BE33n9JVQZDTpT4Ljch0Njx79gUc/view?usp=sharing']
        }

        

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

        dialog_items = []
        
        for i in self.book_name_dict.keys():

            dialog_items.append(ListItemWithCheckbox(text = f'[size=16][font=DejaVuSans]{i.title()}[/font][/size]',
                                              secondary_text=f"[size=14][font=assets/fonts/Roboto-LightItalic.ttf]{self.book_name_dict[i][2].title()}[/font][/size]",
                                              source=self.book_name_dict[i][0],
                                              divider='Inset',
                                              divider_color=utils.get_color_from_hex(colors['Purple']['200'])))
        
        if not self.dialogx:

            self.dialogx = MDDialog(
                size_hint=(0.85, None),
                md_bg_color=[1,1,1,0.7],
                title = "[font=assets/fonts/Aclonica.ttf][size=18][b]Download Audiobooks?[/b][/size][/font]",
                text = "[size=16]Select the ones you want to download[/size]",
                type = 'confirmation',
                items = dialog_items,
                buttons=[
                    MDRectangleFlatIconButton(
                        icon='close',
                        md_bg_color = utils.get_color_from_hex(colors['Purple']['500']),
                        theme_text_color="Custom",
                        icon_color=[1,1,1,0.9],
                        text_color=[1,1,1,0.9],
                        line_color=[.2,.2,.2,0.85],
                        text="[font=assets/fonts/Aclonica.ttf][size=16][b]CANCEL[/b][/size][/font]",
                        padding=[6,6]
                        
                    ),
                    MDRectangleFlatIconButton(
                        icon='thumb-up',
                        text="[font=assets/fonts/Aclonica.ttf][size=16][b]OK[/b][/size][/font]",
                        md_bg_color = utils.get_color_from_hex(colors['Purple']['500']),
                        theme_text_color="Custom",
                        icon_color=[1,1,1,0.9],
                        text_color=[1,1,1,0.9],
                        line_color=[.2,.2,.2,0.85],
                        padding=[6,6],
                        on_release = self.get_active_boxes
                    ),
                ])
            
            self.dialogx.open()


    def get_active_boxes(self, *kwargs):
        
        if self.dialogx:
            
            selected_books = self.dialogx.children[0].children[2].children[0].children
            self.selected_books = [i.text.replace('[size=16][font=DejaVuSans]','').replace('[/font][/size]','') for i in selected_books if i.children[0].active == True]
       
            print(self.selected_books)
            self.thread()
    
    def thread(self, *args):
        
        self.stop = threading.Event() 

        for i in self.selected_books:
            if i in [x.title() for x in self.book_name_dict.keys()]:
                print('found')
                ZIP_URL = self.book_name_dict[i.lower()][3]
                self.r = requests.get(ZIP_URL)
             
                self.ZIP_FILENAME = i+'.zip'

                with open(os.path.join(download_dir_path,self.ZIP_FILENAME), 'wb') as f:
                    f.write(self.r.content)
                self.unzip_content()
                # req = UrlRequest(ZIP_URL,
                #             chunk_size=1024, on_success=self.unzip_content,
                #             file_path=os.path.join(download_dir_path, self.ZIP_FILENAME))
                # print(self.ZIP_FILENAME)
            
                #THE DOWNLOADING SOMEHOW CORRUPS THE FILE FROM GOOGLE DRIVE IG COZ ITS TOO BIG. ill upload to github and then download maybe

    def unzip_content(self):
        print('came inside unzip content ')
        threading.Thread(target=self.unzip_thread).start()

    def unzip_thread(self):
        print('came inside unzip thread')
        print("Unzipping file")
        fh = open(os.path.join(download_dir_path,self.ZIP_FILENAME), 'rb')
        z = zipfile.ZipFile(fh)
        ZIP_EXTRACT_FOLDER = os.path.join(download_dir_path,'zipfile.zip') + '_extracted'
        print(ZIP_EXTRACT_FOLDER)
        if not os.path.exists(ZIP_EXTRACT_FOLDER):
            os.makedirs(ZIP_EXTRACT_FOLDER)
        z.extractall(ZIP_EXTRACT_FOLDER)
        fh.close()
        # os.remove(ZIP_FILENAME)
        time.sleep(4) # DEBUG: stretch out the unzip method to test threading

       
        z = zipfile.ZipFile(io.BytesIO(self.r.content))
        z.extractall()

        print("Done")




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
   

MainApp().run()