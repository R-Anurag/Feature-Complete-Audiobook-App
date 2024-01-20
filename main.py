# Changing the audioplayer library since the default audio_sdl2 does not provide seek operation

import os
from kivy.config import Config
# Config.set('input', 'mouse', 'mouse,multitouch_on_demand') Not removing this since this little bugger was responsible for firing on_release twice in android phone and only once in desktop!! <crying emoji>
os.environ['KIVY_AUDIO'] = 'ffpyplayer'

# =================================================================

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, DictProperty
from kivymd.color_definitions import colors
from kivymd.uix.snackbar import Snackbar
from kivy.core.audio import SoundLoader
from kivymd.uix.slider import MDSlider
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy import utils
from kivymd.uix.menu import MDDropdownMenu
from kivymd.color_definitions import colors
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import MagicBehavior
from itertools import chain
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, OneLineIconListItem, IRightBodyTouch
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Color, Rectangle
# from kivy.utils import platform
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.text import Label as CoreLabel
import shutil
import yaml
import time
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton, MDIconButton, MDFlatButton
import requests

from concurrent.futures import ThreadPoolExecutor
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner.spinner import MDSpinner
import time
import threading
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



# Declaring global variables to pass data in different threads
global combined_download_percentage
combined_download_percentage = 0
global downloading_size_dict
downloading_size_dict = {}
# =================================================================


kivy_string = '''
#:import utils kivy.utils
#:import colors kivymd.color_definitions.colors
#:import SwapTransition kivy.uix.screenmanager.SwapTransition
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import Gradient main.Gradient

<MenuHeader>
    orientation: "vertical"
    adaptive_size: True
    padding: "4dp"

    MDBoxLayout:
        spacing: "12dp"
        adaptive_size: True

        MDIconButton:
            icon: root.icon
            theme_icon_color: "Custom"
            icon_color: (1,1,1,1)
            pos_hint: {"center_y": .5}

        MDLabel:
            markup: True
            text: f"[b]{root.label}[/b]"
            theme_text_color: "Custom"
            text_color: (1,1,1,1)
            font_name: r"assets/fonts/try2.ttf"
            adaptive_size: True
            pos_hint: {"center_y": .5}


<Marquee>:
    StencilView:
        id: sten
        pos: root.pos
        size_hint: None, None
        size: root.size
        Image:
            id: label
            texture: root.texture
            pos: root.pos
            size_hint: None, None
            size: self.texture_size
             
            
<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height
    type_swipe: "hand"
    max_opened_x: "60dp"

    MDCardSwipeLayerBox:
        padding: "8dp"
        md_bg_color: utils.get_color_from_hex(colors['DeepOrange']['400'])

        MDIconButton:
            icon: "trash-can"
            theme_icon_color: "Custom"
            icon_color: 1,1,1,0.8
            pos_hint: {"center_y": .5}
            on_release:
                app.screens.get_screen('menuscreen').remove_item(root)

    MDCardSwipeFrontBox:
        md_bg_color: 1,1,1,0.8

        TwoLineAvatarListItem:
            id: content
            text: "[size=18sp]"+root.text+"[/size]"
            secondary_text: "[size=14sp]"+root.secondary_text+"[/size]"
            secondary_theme_text_color: "Custom"
            secondary_text_color: (0,0,0,0)
            _no_ripple_effect: True
            # bg_color: utils.get_color_from_hex(colors['Purple']['300'])

            Marquee:
                text: root.secondary_text
                color: 0,0,0,0.7
                font_name: 'DejaVuSans'
                font_size: '14sp'
                duration: 7
                padding: 10
                pos_hint: {'center_x': 0.45, 'center_y': 0.59}
                size_hint_x: 0.5

   
            Widget:
                pos_hint: {"center_x": .4, "center_y": .5}
                canvas.before:
                    Color:
                        rgba: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])
                    Rectangle:
                        pos: self.width/1.3, 1
                        size: self.width/4, self.height
                        texture: Gradient.horizontal(utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])[:3] + [0.35], (1, 1, 1, 0.30))

                MDRectangleFlatIconButton:
                    icon: "menu-right-outline"
                    text: ""
                    icon_size: "28sp"
                    theme_icon_color: "Custom"
                    icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])
                    md_bg_color: (0,0,0,0)
                    line_color: (0,0,0,0)
                    pos: self.parent.width/1.4, 1
                    padding: [self.parent.width/5, self.parent.height/1.5, self.parent.width/20, self.parent.height/3]
                    on_release: 
                        app.screens.get_screen('menuscreen').insert_audiobook_parts(root)
                        app.root.transition = SwapTransition()
                        app.root.current = 'playscreen'
                        

            
            ImageLeftWidget:
                source: root.source if app.screens.get_screen('menuscreen').check_internet_connection() != 'off' else 'assets/images/appicon.png'
                disabled: True
                ripple_scale: 0
                ripple_color: 0,0,0,0


<ListItemWithCheckbox>:
    adaptive_height: True
    _no_ripple_effect: True
    AsyncImage:
        source: root.source 
        size_hint: None, None
        size: self.image_ratio*root.height,root.height/1.5
        mipmap: True 
        pos_hint: {'center_x':0.1, 'center_y': 0.5}
        disabled: True
        on_error:
            self.source = 'assets/images/appicon.png'
     
    RightCheckbox:
        id: checkbox
        checkbox_icon_down: 'checkbox-marked-outline'
        disabled_color: utils.get_color_from_hex(colors['Gray']['500'])
        pos_hint: {'center_x':0.92, 'center_y': 0.5}
        size_hint: (None, None)
        size: (dp(48), dp(48))
        active: False
        on_active:
            size_label.text = root.mb_text if checkbox.active else ""


    MDLabel:
        id: size_label
        text: ""
        halign: "center"
        font_size: "10sp"
        pos_hint: {'center_x':0.92, 'center_y': 0.22}
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 0.8

    Marquee:
        text: root.sliding_text
        color: 0,0,0,0.7
        font_name: 'DejaVuSans'
        font_size: '14sp'
        duration: 7
        padding: 10
        pos_hint: {'center_x': 0.46, 'center_y': 0.58}
        size_hint_x: 0.5

    MDIcon:
        icon: root.new_icon
        icon_size: "28sp"
        theme_text_color: "Custom"
        text_color: utils.get_color_from_hex(colors['Red'][app.theme_cls.primary_hue])
        pos_hint: {'center_x':0.90, 'center_y': 0.85}


    

<ClickableTextFieldRound>:
    size_hint_y: None

    MDTextField:
        id: text_field
        mode: 'fill'
        font_size: '16sp'
        hint_text: root.hint_text
        text: root.text
        password: False
        fill_color_normal: 1,1,1,0.6
        active_line: True
        radius: 6,6,6,6
        hint_text_color_focus: utils.get_color_from_hex(colors[app.theme_cls.primary_palette]['500'])
        text_color_focus: utils.get_color_from_hex(colors[app.theme_cls.primary_palette]['900'])
        icon_left_color_focus: utils.get_color_from_hex(colors[app.theme_cls.primary_palette]['500'])
        icon_left: "magnify"
        on_focus:
            close_button.icon_color = utils.get_color_from_hex(colors[app.theme_cls.primary_palette]['500'])
        on_text: 
            app.screens.get_screen('menuscreen').set_menu_screen_list_items(self.text.lower(), True)
            
    MDIconButton:
        id: close_button
        icon: "close"
        icon_size: "20sp"   
        theme_icon_color: "Custom"
        icon_color: 0,0,0,0.8
        md_bg_color: 0,0,0,0
        pos_hint: {"center_y": .55}
        pos: text_field.width - self.width, text_field.height - self.height
        on_release:
            text_field.text=''
            # self.icon = "pencil" if self.icon == "close" else "close"
            # text_field.password = False if text_field.password is True else True

            
<IconListItem>
    IconLeftWidget:
        icon: root.icon
        theme_icon_color: "Custom"
        icon_color: root.icon_color


        
MDScreenManager:
    WelcomeScreen
    MenuScreen
    PlayScreen

    

<WelcomeScreen>
    name: 'welcomescreen'

    canvas.before:
        Color:
            rgba: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])  
        Rectangle:
            pos: self.pos
            size: self.size
            
    MDCarousel:
        id: carousel
        anim_move_duration: 0.5
        scroll_timeout: 0
        MDFloatLayout:
            FitImage:
                source: "assets/images/on_boarding_1.png"
                pos_hint: {"center_x":0.5, "center_y":0.7}
                size_hint: (0.8, 0.4)
    
            MDLabel:
                text: "No more boring reading"
                size_hint_x: 0.6
                halign: "center"
                pos_hint: {"center_x": 0.5, "center_y": 0.38}
                font_name: "assets/fonts/Poppins-Bold.ttf"
                font_size: "20sp"
                theme_text_color: "Custom"
                text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])

            MDLabel:
                text: "Say goodbye to dull and unexciting reading experiences, and open the door to captivating storytelling through immersive audiobooks."
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5, "center_y": 0.27}
                font_name: "assets/fonts/Poppins-Medium.ttf"
                font_size: "18sp"
                theme_text_color: "Custom"
                text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])

        MDFloatLayout:
            FitImage:
                source: "assets/images/on_boarding_2.png"
                pos_hint: {"center_x":0.5, "center_y":0.7}
                size_hint: (0.8, 0.4)
            
            MDLabel:
                text: "Seamless listening session"
                size_hint_x: 0.6
                halign: "center"
                pos_hint: {"center_x": 0.5, "center_y": 0.38}
                font_name: "assets/fonts/Poppins-Bold.ttf"
                font_size: "20sp"
                theme_text_color: "Custom"
                text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])

            MDLabel:
                text: "Experience the delight of an uninterrupted and immersive listening session, where your audiobooks come to life in a flowing and engaging journey."
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5, "center_y": 0.27}
                font_name: "assets/fonts/Poppins-Medium.ttf"
                font_size: "18sp"
                theme_text_color: "Custom"
                text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])

        MDFloatLayout:
            FitImage:
                source: "assets/images/on_boarding_3.png"
                pos_hint: {"center_x":0.5, "center_y":0.7}
                size_hint: (0.8, 0.4)
            
            MDLabel:
                text: "No frustrating ads or promotions"
                size_hint_x: 0.6
                halign: "center"
                pos_hint: {"center_x": 0.5, "center_y": 0.38}
                font_name: "assets/fonts/Poppins-Bold.ttf"
                font_size: "20sp"
                theme_text_color: "Custom"
                text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])

            MDLabel:
                text: "Enjoy your audiobooks without the annoyance of intrusive ads or promotional interruptions."
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5, "center_y": 0.27}
                font_name: "assets/fonts/Poppins-Medium.ttf"
                font_size: "18sp"
                theme_text_color: "Custom"
                text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])

    MDRelativeLayout:
        id: start_buttons
        size_hint: None, None
        size: self.parent.width, self.parent.height
        pos: 0, 0

        MDRectangleFlatButton:
            id: remove
            icon: "chevron-left"
            text: "SKIP"
            font_size: "18sp"
            font_name: "assets/fonts/Poppins-Medium.ttf"
            radius: [32,]
            rounded_button: True
            md_bg_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])
            theme_text_color: "Custom"
            text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])
            line_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])
            padding: [30, 20, 30, 20]
            pos: dp(30), self.parent.parent.height/14
            on_press: self.parent.parent.load(self.text.lower())
            

        MDRectangleFlatButton:
            text: "NEXT"
            font_size: "18sp"
            font_name: "assets/fonts/Poppins-Medium.ttf"
            radius: [32,]
            rounded_button: True
            md_bg_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])
            theme_text_color: "Custom"
            text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])
            line_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])
            padding: [30, 20, 30, 20]
            pos: self.parent.parent.width - (self.width +dp(30)), self.parent.parent.height/14 
            on_press: 
                app.root.current = "menuscreen" if self.text == "START" else "welcomescreen"
                self.parent.parent.load(self.text.lower())

    MDRelativeLayout:
        id: swipe_dots
        size_hint: None, None
        size: self.parent.width, self.parent.height
        pos: self.width/2 - 75, self.parent.height/35

        MDIconButton:
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])
            icon_size: "8sp"
            pos: 0, self.parent.parent.height/8
        
        MDIconButton:
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: [0,0,0,0.6]
            icon_size: "8sp"
            pos: 50, self.parent.parent.height/8
            
        MDIconButton:
            icon: "circle"
            theme_icon_color: "Custom"
            icon_color: [0,0,0,0.6]
            icon_size: "8sp"
            pos: 100, self.parent.parent.height/8


            
    
<MenuScreen>
    name: "menuscreen"
    audiobook_primary_text: 'Hey buddy! You`ve no audiobooks'
    audiobook_secondary_text: 'Let me show you how to download some by clicking'
    gif_source: "assets/images/welcome cat.zip"
    gif_source_2: "assets/images/catdrinkingjuice.zip"
    gif_source_3: "assets/images/catpointingright.zip"


    canvas.before:
        Color:
            rgba: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])  
        Rectangle:
            pos: self.pos
            size: self.size
            

    MDFloatLayout:
        id: floatlayout_id

        Image:
            id: background_gif
            source: root.gif_source if md_list.children == [] else root.gif_source_2
            size_hint: (0.3, 0.3) if md_list.children == [] else (0.27, 0.27) 
            pos_hint: {"center_x": 0.5, "center_y": 0.6} if md_list.children == [] else {"center_x": 0.84, "center_y": 0.94}
            anim_delay: 0.1
            minimap: True
            allow_stretch: True

        
        MDScrollView:
            size_hint: (0.98, 0.81)
            pos_hint: {"center_x": 0.5, "center_y": 0.41} 
            effect_cls: "ScrollEffect"
            MDList:
                id: md_list
                padding: 0

        MDLabel:
            font_size: self.width/8.5
            bold: True
            text:'Search' 
            font_name: "assets/fonts/try2.ttf"
            halign: 'left'
            pos_hint: {'center_x':0.55, 'center_y':0.93}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])  

        MDLabel:
            id: primary_label
            font_size: self.width/15
            bold: True
            text: root.audiobook_primary_text if md_list.children == [] else ""
            font_name: "assets/fonts/PlayfairDisplay-Bold.ttf"
            halign: 'center'
            size_hint_x: 0.9
            pos_hint: {'center_x':0.5, 'center_y':0.50}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])  
        
        MDLabel:
            id: secondary_label
            markup: True
            font_size: self.width/22
            bold: True
            text: root.audiobook_secondary_text if md_list.children == [] else ""
            font_name: "DejaVuSans"
            # font_name: "assets/fonts/Aclonica.ttf"
            halign: 'center'
            size_hint_x: 0.95
            pos_hint: {'center_x':0.5, 'center_y':0.42}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])  
        
        MDFlatButton:
            id: here_label
            font_size: secondary_label.font_size
            text: f'[color={colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue]}]here[/color]' if md_list.children == [] else ""
            pos_hint: {'center_x':0.64, 'center_y':0.41}
            disabled: True if md_list.children != [] else False
            ripple_scale: 0 if md_list.children != [] else 0.3
            padding: [0, ]
            on_release:
                background_gif.source = root.gif_source_3 if md_list.children == [] else root.gif_source_2
                background_gif.pos_hint= {"center_x": 0.7, "center_y": 0.075} if md_list.children == [] else {"center_x": 0.84, "center_y": 0.92}
                background_gif.size_hint= (0.4, 0.4) if md_list.children == [] else (0.27, 0.27) 
                secondary_label.text= "Yes! That button right there!" if md_list.children == [] else ""
                primary_label.text= "Press it" if md_list.children == [] else ""
                self.text = ""
                self.parent.remove_widget(self)
                
        
        ClickableTextFieldRound:
            id: search_field
            size_hint_x: None
            width: root.width/1.02
            height: root.height/20
            hint_text: "Author, title or series" 
            pos_hint: {"center_x": .5, "center_y": .85}
            on_text: root.set_list_md_icon(self.text, True) 

        MDIconButton:
            icon: "attachment-plus"
            theme_icon_color: "Custom"
            icon_color: (1,1,1,1)
            icon_size: "28sp"
            elevation: 6
            md_bg_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])  
            pos_hint: {"center_x":0.91, "center_y": .06}
            on_release:
                root.show_download_list()

        MDIconButton:
            id: color_palette
            icon: "palette"
            theme_icon_color: "Custom"
            icon_color: (1,1,1,1)
            icon_size: "28sp"
            elevation: 6
            md_bg_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])  
            pos_hint: {"center_x":0.91, "center_y": .14}
            on_release: 
                root.palette_button_fun()
  




<PlayScreen>
    name: 'playscreen'
    canvas.before:
        Color:
            rgba: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])  
        Rectangle:
            pos: self.pos
            size: self.size
        
    
    MDFloatLayout:
        id: playerpart
        size_hint: 1, 0.8
        pos_hint: {"center_x": .5, "center_y": .58}

        MagicCard:
            padding: "2dp"
            ripple_behavior: False
            orientation: "horizontal"
            size_hint: (1, .09)
            focus_behavior: False
            pos_hint: {"center_x": .5, "center_y": 1}
            md_bg_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])
                
        MDLabel:
            markup: True
            id: top_bar_heading
            text: ""
            font_size: '14sp'
            font_name: 'DejaVuSans'
            halign: "center"
            # theme_text_color: "Hint"
            theme_text_color: "Custom"
            text_color: (1,1,1,1)
            pos_hint: {"center_x": .5, "center_y": 1}

                
        MDIconButton:
            id: sleep_timer_button
            icon: "power-sleep"
            icon_size: "24sp" 
            pos_hint: {"center_x": 0.9, "center_y": 0.99}
            theme_icon_color: "Custom"
            icon_color: 1,1,1,1
            on_release:
                app.sleep_button_fun(self)


        MagicCard:
            radius: [10, ]
            padding: "2dp"
            ripple_behavior: False
            orientation: "vertical"
            size_hint: (.85, .75)
            focus_behavior: False
            pos_hint: {"center_x": .5, "center_y": .5}
            md_bg_color: (0, 0, 0, 0.35)

        AsyncImage:
            id: album_picture
            size_hint: (1, 0.75)
            source: ""
            radius: (6, 6, 6, 6)
            minimap: True
            pos_hint: {"center_x": .5, "center_y": .63}
            

        MDLabel:
            id: audiobook_part_name
            text: ""
            font_size: "18sp"
            font_name: 'DejaVuSans'
            halign: "left"
            # theme_text_color: "Hint"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            pos_hint: {"center_x": .62, "center_y": .38}

        Marquee:
            id: audiobook_album_name
            text: ''
            font_size: '14sp'
            font_name: 'DejaVuSans'
            duration: 7
            bold: True
            size_hint_x: 0.76
            pos_hint: {'center_x': 0.5, 'center_y': 0.82}
            padding: 10
            
        MySlider:
            id: slider
            color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])
            thumb_color_active: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])
            thumb_color_inactive: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])
            min: 0
            sound: None
            max: 0
            value: 0
            pos_hint: {'center_x': 0.50, 'center_y': 0.30}
            size_hint: (0.85, 0.1)  
            hint: False      
            track: True
            track_color_active: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])
            track_color_inactive: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_dark_hue])

        MDBoxLayout:
            orientation: "horizontal"
            padding: (0,8,0,0)
            size_hint: 0.76, None
            height: self.minimum_height
            pos_hint: {'center_x': 0.50, 'center_y': 0.27}

            MDLabel:
                id: sound_pos_label
                text: "0.0"
                font_size: '12sp'
                halign: "left"
                # theme_text_color: "Hint"
                theme_text_color: "Custom"
                text_color: 1,1,1,1

            
            MDLabel:
                id: sound_length_label
                text: "1.0"
                font_size: '12sp'
                halign: "right"
                # theme_text_color: "Hint"
                theme_text_color: "Custom"
                text_color: 1,1,1,1

            
        MDFloatLayout:
            size_hint: 0.76, None
            pos_hint: {'center_x': 0.50, 'center_y': 0.22}
            
            MDIconButton:
                icon: "rewind-10"
                icon_size: "40sp" 
                pos_hint: {'center_x': 0.30, 'center_y': 0}
                ripple_scale: 0.5
                theme_icon_color: "Custom"
                icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue]) 
                on_release:
                    self.parent.parent.parent.audiobook.seek(self.parent.parent.parent.audiobook.get_pos() - 10) if self.parent.parent.parent.audiobook.get_pos() > 0.1 else self.parent.parent.parent.audiobook.get_pos()
                    #note that the else part just loses the value and is done just to complete the if else structure whichw as necessary

            MDIconButton:
                id: play_pause_button
                icon: "play-circle"
                icon_size: "68sp" 
                pos_hint: {'center_x': 0.50, 'center_y': 0}
                ripple_scale: 0.5
                theme_icon_color: "Custom"
                icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue]) 
                on_release:
                    self.parent.parent.parent.play_pause()


            MDIconButton:
                icon: "fast-forward-10"
                icon_size: "40sp"  
                pos_hint: {'center_x': 0.70, 'center_y': 0}
                ripple_scale: 0.5
                theme_icon_color: "Custom"
                icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue]) 
                on_release:
                    self.parent.parent.parent.audiobook.seek(self.parent.parent.parent.audiobook.get_pos() + 10) if self.parent.parent.parent.audiobook.get_pos() > 0.1 else 0
                    #note that the else part is done just to complete the if else structure whichw as necessary
            
            MDIconButton:
                icon: "skip-previous"
                theme_icon_color: "Custom"
                ripple_scale: 0.5
                icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue]) 
                icon_size: "44sp"  
                pos_hint: {'center_x': 0.05, 'center_y': 0}
                on_release:
                    self.parent.parent.parent.load_audiobook(int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5:])-1) if int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5:]) > int(list(app.screens.get_screen('menuscreen').dict_book_link[audiobook_part_name.text[:audiobook_part_name.text.index(':')].lower()][2].keys())[0].replace('part','')) else 0
                    
            MDIconButton:
                icon: "skip-next"
                theme_icon_color: "Custom"
                ripple_scale: 0.5
                icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue]) 
                icon_size: "44sp"  
                pos_hint: {'center_x': 0.95, 'center_y': 0}
                on_release:
                    self.parent.parent.parent.load_audiobook(int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5:])+1) if int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5:]) < int(list(app.screens.get_screen('menuscreen').dict_book_link[audiobook_part_name.text[:audiobook_part_name.text.index(':')].lower()][2].keys())[-1].replace('part','')) else 0
                    

    
    MDFloatLayout
        pos_hint: {"center_x":0.5, "center_y":1}
        Marquee:
            id: top_bar_sub_heading
            text: ""
            color: (1,1,1,1)
            pos_hint: {"center_x": 0.5, "center_y": 0.95}        
            font_size: '12sp'
            font_name: 'DejaVuSans'
            duration: 7
            bold: True
            size_hint_x: 0.5
    
            
    MDFloatLayout
        pos_hint: {"center_x":0.5, "center_y":0.5}
        canvas:
            Color:
                rgba: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_hue])
            Triangle:
                points: (self.width/2)-12.5,(self.height/1.056),   (self.width/2)+12.5,(self.height/1.056),   (self.width/2),(self.height/1.056)-12

        MDIconButton:
            icon: "chevron-down"
            icon_size: "24sp" 
            pos_hint: {"center_x": 0.5, "center_y": 0.94}
            ripple_scale: 0.8
            theme_icon_color: "Custom"
            icon_color: utils.get_color_from_hex(colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue]) 
            on_release:
                app.screens.get_screen('playscreen').audiobook.stop()
                app.root.transition = SlideTransition(direction='down')
                app.root.current = 'menuscreen'
                

    MDFloatLayout:
        MDScrollView:
            size_hint: (0.85, 0.2)
            pos_hint: {"center_x": 0.5, "center_y": 0.15} 
            effect_cls: "ScrollEffect"
            radius: [10, ]
            MDList:
                id: md_list_2
                radius: [10, ]
                md_bg_color: (0,0,0,0.35)
                padding: 0
                

'''


# for searchbar in library


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    source = ObjectProperty()

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
    pass
    
class Gradient(object):
    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens"

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    sliding_text = StringProperty()
    secondary_theme_text_color = StringProperty()
    secondary_text_color = ColorProperty()
    source = ObjectProperty()
    mb_text = StringProperty()
    new_icon = StringProperty("")
    _txt_right_pad = NumericProperty("0dp")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._txt_right_pad = dp(10) + m_res.HORIZ_MARGINS


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
    icon_color = ColorProperty()


class MagicCard(MagicBehavior, MDCard):
    pass


class MenuHeader(MDBoxLayout):
    icon = StringProperty()
    label = StringProperty()


class Marquee(MDFloatLayout):
    texture = ObjectProperty()
    text = StringProperty()
    color = ColorProperty()
    duration = NumericProperty(2)
    font_name = StringProperty("Consolas")
    font_size = NumericProperty(12)
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    padding = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Marquee, self).__init__(**kwargs)
        self.anim = None
        self.x_original = None
        fbind = self.fbind
        redraw = self.redraw
        fbind('text', redraw)
        fbind('color', redraw)
        fbind('duration', redraw)
        fbind('font_name', redraw)
        fbind('font_size', redraw)
        fbind('bold', redraw)
        fbind('italic', redraw)
        fbind('padding', redraw)

    def on_x(self, *args):
        self.x_original = self.x
        Clock.schedule_once(self.redraw)

    def redraw(self, *args):
        if self.x_original is None:
            return
        if self.text == '':
            self.texture = None
            return
        label = CoreLabel(text=self.text, color=self.color, font_name=self.font_name, font_size=self.font_size,
                          bold=self.bold, italic=self.italic, padding=self.padding)
        label.refresh()
        self.texture = label.texture
        Clock.schedule_once(self.do_anim)

    def do_anim(self, *args):
        if self.anim is not None:
            self.anim.cancel(self.ids.label)
            self.anim = None
        self.ids.label.x = self.x_original
        x_end = self.ids.label.x - self.ids.label.width
        self.anim = Animation(x=x_end, duration=self.duration)
        self.anim.bind(on_complete=self.do_anim)
        self.anim.start(self.ids.label)


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
                MDApp.get_running_app().screens.get_screen('playscreen').play_pause()

            # return the saved return value
            return ret_val
        else:
            return super(MySlider, self).on_touch_up(touch)


class PlayScreen(MDScreen):

    def on_pre_enter(self, *args):
        self.load_audiobook(1)

    def load_audiobook(self, part_number, *args):
        # Adding a try except block since this function is called every single time any of the parts are pressed to play
        try:
            self.audiobook.stop()
        except AttributeError:
            pass

        self.audiobook = SoundLoader.load(
            f"app data/audiobooks/{MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook}/part{part_number}.mp3")

        self.playscreen_ids = MDApp.get_running_app().screens.get_screen('playscreen').ids
        self.slider = self.playscreen_ids.slider

        if MDApp.get_running_app().screens.get_screen('menuscreen').check_internet_connection() != 'off':
            self.playscreen_ids.album_picture.source = MDApp.get_running_app().screens.get_screen(
                'menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][1]
        else:
              self.playscreen_ids.album_picture.source = "assets/images/appicon.png"


        self.playscreen_ids.audiobook_album_name.text = MDApp.get_running_app().screens.get_screen(
            'menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0]
        self.playscreen_ids.audiobook_part_name.text = MDApp.get_running_app().screens.get_screen(
            'menuscreen').selected_audiobook.title() + f": Part-{part_number}"
        self.playscreen_ids.top_bar_heading.text = "[b]" + "Album: " + MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0].replace(MDApp.get_running_app().screens.get_screen(
            'menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0][MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0].index('by'):], '') + "[/b]"
        self.playscreen_ids.top_bar_sub_heading.text = "Currently playing: " + MDApp.get_running_app().screens.get_screen(
            'menuscreen').selected_audiobook.title() + f" part-{part_number}"

        self.slider.sound = self.audiobook
        self.slider.max = self.audiobook.length

        self.playscreen_ids.sound_length_label.text = time.strftime(
            "%H:%M:%S", time.gmtime(self.audiobook.length))

        self.updater = None
        self.paused = False

        self.audiobook_part_selected = [i for i in MDApp.get_running_app().screens.get_screen(
            'playscreen').ids.md_list_2.children if int(i.text.lower().replace("part-", "").strip()) == part_number][0]

        MDApp.get_running_app().screens.get_screen(
            'menuscreen').part_highlight(self.audiobook_part_selected)

        MDApp.get_running_app().screens.get_screen(
            'playscreen').ids.md_list_2.parent.scroll_to(self.audiobook_part_selected)

        self.play_pause()

    def play_pause(self, *args):
        if self.updater is None:
            # schedule updates to the slider
            self.updater = Clock.schedule_interval(self.update_slider, 1)

        if self.paused == True:
            self.audiobook.play()
            self.audiobook.seek(self.stop_position)
            self.playscreen_ids.play_pause_button.icon = "pause-circle"
            self.paused = False
        elif self.paused == False:
            if self.audiobook.state == "stop":
                self.audiobook.play()
                self.playscreen_ids.play_pause_button.icon = "pause-circle"
            elif self.audiobook.state == "play":
                self.stop_position = self.audiobook.get_pos()
                self.audiobook.stop()
                self.playscreen_ids.play_pause_button.icon = "play-circle"
                self.paused = True
                # stop the slider from updating the value
                self.updater.cancel()
                self.updater = None

    def update_slider(self, *args):
        # if the sound has finished, stop the updating
        if self.audiobook.state == 'stop' and self.updater != None:
            self.updater.cancel()
            self.updater = None
        # update slider
        self.slider.value = self.audiobook.get_pos()
        # updating the sound position label as well here
        self.playscreen_ids.sound_pos_label.text = time.strftime(
            "%H:%M:%S", time.gmtime(self.audiobook.get_pos()))


class MenuScreen(MDScreen):

    data = DictProperty()
    content_dict = DictProperty()
    icon_image_dict = DictProperty()

    def on_enter(self, *kwargs):

        with open('app data/book link dict.yaml', 'r') as file:
            self.dict_book_link = yaml.safe_load(file)

        # self.downloaded_audiobook_list = []

    def remove_item(self, instance):

        if os.path.exists(f"app data/app dapp data/downapp data/downata/down data/downbooks/{instance.text.lower()}"):
            shutil.rmtree(f"app data/audiobooks/{instance.text.lower()}")

        with open(r"app data/downloaded_audiobooks.dat", "rb+") as file_object:
            downloaded_audiobooks = []
            try:
                while True:
                    downloaded_audiobooks.append(pickle.load(file_object))
            except EOFError:
                pass

        with open(r"app data/downloaded_audiobooks.dat", "wb") as file:
            for i in downloaded_audiobooks:
                if i != instance.text.lower():
                    pickle.dump(i, file)

        MDApp.get_running_app().screens.get_screen(
            'menuscreen').ids.md_list.remove_widget(instance)

    def palette_button_fun(self, *kwargs):
        MDApp.get_running_app().theme_menu.caller = self.ids.color_palette
        MDApp.get_running_app().theme_menu.open()
    

    def show_download_list(self, *kwargs):
        self.already_downloaded_audiobooks = []

        if os.path.isfile("app data/downloaded_audiobooks.dat"):
            with (open("app data/downloaded_audiobooks.dat", "rb")) as openfile:
                try:
                    while True:
                        self.already_downloaded_audiobooks.append(
                            pickle.load(openfile))
                except EOFError:
                    pass

        dialog_items = []

        for i in self.dict_book_link.keys():
            if i not in self.already_downloaded_audiobooks:
                dialog_items.append(ListItemWithCheckbox(text=f'[size=16sp][font=DejaVuSans]  {i.title()}[/font][/size]',
                                                         secondary_text="sffsfsafasfasfas",
                                                         secondary_theme_text_color="Custom",
                                                         secondary_text_color=(
                                                             0, 0, 0, 0),
                                                         sliding_text=f"{self.dict_book_link[i][0].title()}",
                                                         source=self.dict_book_link[i][1],
                                                         mb_text=self.dict_book_link[i][3],
                                                         divider='Inset',
                                                         divider_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue])))

        self.dialogx = MDDialog(
            size_hint=(0.90, None),
            md_bg_color=[1, 1, 1, 0.7],
            title=f"[color={colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_dark_hue]}][font=assets/fonts/try2.ttf][size=18sp][b]Download Audiobooks?[/b][/size][/font][/color]",
            text=f"[color={colors[MDApp.get_running_app().theme_cls.primary_palette]['700']}][size=16sp][font=DejaVuSans]Select the ones you want to download[/font][/size][/color]",
            radius=[20, 7, 20, 7],
            padding=0,
            type='confirmation',
            auto_dismiss=False,
            items=dialog_items,
            buttons=[
                MDRectangleFlatIconButton(
                    text="[font=assets/fonts/Aclonica.ttf][size=12sp][b]UPDATE LIST[/b][/size][/font]",
                    icon="update",
                    md_bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app(
                    ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                    theme_text_color="Custom",
                    theme_icon_color="Custom",
                    icon_color=(1, 1, 1, 1),
                    text_color=(1, 1, 1, 1),
                    line_color=utils.get_color_from_hex(
                        colors[MDApp.get_running_app().theme_cls.primary_palette]['700']),
                    on_release=lambda x: self.update_download_list()

                ),

                MDRectangleFlatIconButton(
                    icon='close',
                    md_bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app(
                    ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                    theme_text_color="Custom",
                    theme_icon_color="Custom",
                    icon_color=(1, 1, 1, 1),
                    text_color=(1, 1, 1, 1),
                    line_color=utils.get_color_from_hex(
                        colors[MDApp.get_running_app().theme_cls.primary_palette]['700']),
                    text="[font=assets/fonts/Aclonica.ttf][size=12sp][b]CLOSE[/b][/size][/font]",
                    padding=[4, 4],
                    on_release=self.dialog_dismiss

                ),
                MDRectangleFlatIconButton(
                    icon='thumb-up',
                    text="[font=assets/fonts/Aclonica.ttf][size=12sp][b]OK[/b][/size][/font]",
                    md_bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app(
                    ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                    theme_text_color="Custom",
                    theme_icon_color="Custom",
                    icon_color=(1, 1, 1, 1),
                    text_color=(1, 1, 1, 1),
                    line_color=utils.get_color_from_hex(
                        colors[MDApp.get_running_app().theme_cls.primary_palette]['700']),
                    padding=[4, 4],
                    on_press=self.get_active_boxes
                ),
            ])

        self.dialogx.open()
        
    def dialog_dismiss(self, obj):
    	self.dialogx.dismiss(force=True)

    def get_active_boxes(self, *kwargs):
        
        global counter
        counter = 5

        # Storing the active checkboxes in self.selected_books
        self.mdlist_items = self.dialogx.children[0].children[2].children[0].children
        self.selected_books = [i.text.replace('[size=16sp][font=DejaVuSans]', '').replace('[/font][/size]', '').lower().strip() for i in self.mdlist_items if i.children[4].children[0].active == True]

        if self.selected_books != []:
            if self.check_internet_connection() == 'off':
                Snackbar(text=f"There is trouble connecting to Internet!", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]), snackbar_y="10dp", size_hint_x=(self.width - 20) / self.width, elevation=2).open()
                Clock.schedule_once(self.implementCounterEnd, 3)
            else:
                # This is a list containing nested list for downloading
                complete_url_list_with_filepath = []
                for i in self.dict_book_link.keys():
                    for j in self.dict_book_link[i][2].keys():
                        if i in self.selected_books:
                            complete_url_list_with_filepath.append([i.lower(), j.lower(), self.dict_book_link[i][2][j], self.dict_book_link[i][3]])

                # Forming a dictionary to store the size of audiobook and current_downloaded_size
                global downloading_size_dict
                downloading_size_dict = {}
                for i in self.selected_books:
                    downloading_size_dict[f"{i}_full_size"] = float(
                        self.dict_book_link[i][3].replace('MB', ''))

                    downloading_size_dict[f"{i}_downloaded_size"] = 0

                # Deleting the ok, close and update button
                for i in list(self.dialogx.children[0].children[0].children[0].children):
                    self.dialogx.children[0].children[0].children[0].remove_widget(i)

                # Removing the Checkbox from the selected items
                for i in self.mdlist_items:
                    if i.text.replace('[size=16sp][font=DejaVuSans]', '').replace('[/font][/size]', '').lower().strip() in self.selected_books:
                        i.children[4].remove_widget(i.children[4].children[0])
                    else:
                        i.ids.checkbox.disabled = True
                        i.ids.checkbox.checkbox_icon_normal = "checkbox-blank-off"

                # adding the spinner to selected items from the dialog list
                for i in self.mdlist_items:
                    if i.text.replace('[size=16sp][font=DejaVuSans]', '').replace('[/font][/size]', '').lower().strip() in self.selected_books:
                        i.add_widget(
                            MDSpinner(size_hint=(None, None), size=(dp(24), dp(24)), pos_hint={"center_x": 0.90, "center_y": 0.5}, active=True, line_width=dp(3), palette=[
                                [0.28627450980392155, 0.8431372549019608,
                                    0.596078431372549, 1],
                                [0.3568627450980392, 0.3215686274509804,
                                    0.8666666666666667, 1],
                                [0.8862745098039215, 0.36470588235294116,
                                    0.592156862745098, 1],
                                [0.8784313725490196, 0.9058823529411765,
                                    0.40784313725490196, 1],
                            ])
                        )

                # Adding the Downloading label button to MDDialog
                self.label_button = MDRaisedButton(
                    text="",
                    md_bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]), font_size="12sp",
                    theme_text_color="Custom", text_color=(1, 1, 1, 1), padding=[8, 0], elevation=2, ripple_scale=0, size_hint=(None, None), size=(100, 20)
                )

                self.dialogx.children[0].children[0].children[0].add_widget(
                    self.label_button)

                # Adding downloading percentage label to md_list
                for i in self.mdlist_items:
                    if i.text.replace('[size=16sp][font=DejaVuSans]', '').replace('[/font][/size]', '').lower().strip() in self.selected_books:

                        var_name = i.text.replace('[size=16sp][font=DejaVuSans]', '').replace(
                            '[/font][/size]', '').lower().strip()

                        i.add_widget(
                            MDLabel(
                                text="[size=10sp]"+str(
                                    downloading_size_dict[f"{var_name}_downloaded_size"])+"[/size]",
                                halign="center",
                                markup=True,
                                pos_hint={'center_x': 0.82, 'center_y': 0.22},
                                theme_text_color="Custom",
                                text_color=utils.get_color_from_hex(colors[MDApp.get_running_app(
                                ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_dark_hue])
                            )
                        )

                self.thread = threading.Thread(target=self.thread_pool_download_function, args=(
                    complete_url_list_with_filepath, self.mdlist_items))
                self.thread.start()

                self.downloaded_audiobooks = []
                Clock.schedule_interval(self.check_downloaded_status, 0.5)
                
        
        else:
            Snackbar(text=f"No audiobooks selected!", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]), snackbar_y="10dp", size_hint_x=(self.width - 20) / self.width, elevation=2).open()


    def check_downloaded_status(self, *args):

        for i in self.mdlist_items:

            variable = i.text.replace('[size=16sp][font=DejaVuSans]', '').replace(
                '[/font][/size]', '').lower().strip()

            if variable in self.selected_books and variable not in self.downloaded_audiobooks:

                if not downloading_size_dict[f"{variable}_downloaded_size"] < downloading_size_dict[f"{variable}_full_size"] - 2:

                    self.downloaded_audiobooks.append(variable)

                    # removing the spinner
                    i.remove_widget(i.children[1])

                    # adding the done icon
                    i.add_widget(
                        MDIconButton(
                            icon="checkbox-marked-circle",
                            pos_hint={"center_x": 0.92, "center_y": 0.5}, theme_icon_color="Custom",
                            icon_color=utils.get_color_from_hex(
                                colors[MDApp.get_running_app().theme_cls.primary_palette]['700'])
                        )
                    )

        if set(self.selected_books) == set(self.downloaded_audiobooks):
            with open(r"app data/downloaded_audiobooks.dat", "ab") as file:
                for i in self.selected_books:
                    MDApp.get_running_app().screens.get_screen('menuscreen').ids.md_list.add_widget(
                        SwipeToDeleteItem(text=f"{i}".title(
                        ), secondary_text=f"{self.dict_book_link[i][0]}", source=f"{self.dict_book_link[i][1]}")
                    )

                    pickle.dump(i, file)

            self.stop_scheduled_function()

    def stop_scheduled_function(self, *args):
        Clock.unschedule(self.check_downloaded_status)

    def thread_pool_download_function(self, complete_url_list_with_filepath, mdlist_items):

        def get_confirm_token(response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value

            return None

        def download_file(url_filepath_list):

            session = requests.Session()

            response = session.get(url_filepath_list[2], params={
                                   'id': id}, stream=True)
            token = get_confirm_token(response)

            if token:
                params = {'id': id, 'confirm': token}
                response = session.get(
                    url_filepath_list[2], params=params, stream=True)

            save_response_content(response, url_filepath_list)

        def save_response_content(response, url_filepath_list):
            global combined_download_percentage
            global downloading_size_dict
            # download_filder_path contains the name of the file as well
            download_folder_path = os.path.join(
                r'app data/audiobooks', url_filepath_list[0])

            if not os.path.exists(download_folder_path):
                os.makedirs(download_folder_path)

            filename = url_filepath_list[1]

            CHUNK_SIZE = 32768
            f = open(os.path.join(download_folder_path, filename)+'.mp3', "wb")
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:

                    downloading_size_dict[f"{url_filepath_list[0].lower()}_downloaded_size"] += len(
                        chunk)/(1024*1024)

                    f.write(chunk)

                    combined_downloaded_size = sum(
                        [downloading_size_dict[i] for i in downloading_size_dict.keys() if i.endswith("_downloaded_size")])

                    combined_full_size = sum(
                        [downloading_size_dict[i] for i in downloading_size_dict.keys() if i.endswith("_full_size")])

                    combined_download_percentage = combined_downloaded_size / combined_full_size * 100

            else:
                f.close()

        Clock.schedule_interval(
            self.updateTotalDownloadingPercentage, 0.5)

        with ThreadPoolExecutor() as executor:

            executor.map(download_file, complete_url_list_with_filepath)

            # executor.shutdown()

    def updateTotalDownloadingPercentage(self, *kwargs):
        global combined_download_percentage

        global downloading_size_dict

        # Updating the button label in MDDialog box
        if combined_download_percentage < 99:
            self.label_button.text = "[font=assets/fonts/try4.ttf]Downloading... [/font]" + \
                f"[b]{round(combined_download_percentage, 1)}%[/b]"
        else:
            Clock.unschedule(self.updateTotalDownloadingPercentage)
            Clock.schedule_interval(self.closingCounter, 1)
            Clock.schedule_once(self.implementCounterEnd, 6) 

        # updating the respective download percetnage of audiobooks
        for i in downloading_size_dict:
            if not i.endswith("_full_size"):
                req_label_widget = [j for j in self.mdlist_items if j.text.replace('[size=16sp][font=DejaVuSans]', '').replace(
                    '[/font][/size]', '').lower().strip() == f"{i.lower().replace('_downloaded_size','')}"][0].children[0]

                req_label_widget.text = "[size=10sp]" + \
                    str(
                        f"{round(downloading_size_dict[f'{i.lower()}'],1)}") + "/" + "[/size]"
                

    def closingCounter(self, *kwargs):
        global counter
        self.label_button.text = "[font=assets/fonts/try4.ttf]Download Finished! [/font]" + \
                    f"[b]{100.0}%[/b]" + \
                    f"\n[font=assets/fonts/try4.ttf][i]This Dialog box will self close in[/i][/font] [b]{counter}[/b]"
        if counter > 0:
                counter -= 1

    def implementCounterEnd(self, *kwargs):
        self.dialogx.dismiss()
        try:
            Clock.unschedule(self.closingCounter)
        except:
            pass

    def insert_audiobook_parts(self, instance):

        MDApp.get_running_app().screens.get_screen(
            'playscreen').ids.md_list_2.clear_widgets()
        self.selected_audiobook = instance.text.lower()

        for i in self.dict_book_link[instance.text.lower()][2]:
            MDApp.get_running_app().screens.get_screen('playscreen').ids.md_list_2.add_widget(
                OneLineAvatarIconListItem(IconLeftWidget(icon="headphones", theme_icon_color="Custom", icon_color=(1, 1, 1, 1), disabled=True), text=f"{i}".replace('part', 'part-').title(), theme_text_color="Custom", text_color=(1, 1, 1, 1), radius=[10, ]                                          # , bg_color = (0,0,0,0.35)
                                          , on_press=self.part_highlight,
                                          on_release=lambda x: MDApp.get_running_app().screens.get_screen(
                                          'playscreen').load_audiobook(int(x.text.replace('Part-', '').lower()))
                                          )
            )

    def check_internet_connection(self, *kwargs):
        url = "https://www.github.com"
        timeout = 3
        try:
            request = requests.get(url,
                                   timeout=timeout)
            return "on"
        except (requests.ConnectionError,
                requests.Timeout) as exception:
            return "off"

    def update_download_list(self, *kwargs):

        internet_status = self.check_internet_connection()

        if internet_status != 'off':

            old_list_of_audiobooks = self.dict_book_link

            returned_response = requests.get(r'https://raw.githubusercontent.com/R-Anurag/kivy-audiobook-app/main/assets/links/book%20link%20dict.yaml', headers={
                'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})

            content = yaml.safe_load(returned_response.content)

            self.dict_book_link = content

            with open("app data/book link dict.yaml", "w") as file_object:
                yaml.dump(content, file_object, sort_keys=False)

            newly_added_audiobooks = [i for i in list(
                self.dict_book_link.keys()) if i not in list(old_list_of_audiobooks)]

            for i in newly_added_audiobooks:
                self.dialogx.children[0].children[2].children[0].add_widget(
                    ListItemWithCheckbox(text=f'[size=16sp][font=DejaVuSans]{i.title()}[/font][/size]',
                                        secondary_text="sffsfsafasfasfas",
                                        secondary_theme_text_color="Custom",
                                        secondary_text_color=(0, 0, 0, 0),
                                        sliding_text=f"{self.dict_book_link[i][0].title()}",
                                        source=self.dict_book_link[i][1],
                                        mb_text=self.dict_book_link[i][3],
                                        new_icon='new-box',
                                        divider='Inset',
                                        divider_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue])),

                    len(self.dialogx.children[0].children[2].children[0].children)
                )

            if newly_added_audiobooks == []:
                Snackbar(text=f"The download list is up-to-date already!", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                        snackbar_y="10dp", size_hint_x=(self.width - 20) / self.width, elevation=2).open()

            else:
                Snackbar(text=f"The download list has been updated!", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                        snackbar_y="10dp", size_hint_x=(self.width - 20) / self.width, elevation=2).open()

        else:
            Snackbar(text=f"Trouble connecting to the internet!", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                    snackbar_y="10dp", size_hint_x=(self.width - 20) / self.width, elevation=2).open()

    def part_highlight(self, instance):
        for i in instance.parent.parent.children[0].children:
            i.bg_color = (0, 0, 0, 0)
        else:
            instance.bg_color = utils.get_color_from_hex(colors[MDApp.get_running_app(
            ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue])

    def set_menu_screen_list_items(self, text="", search=False):

        if search:
            self.ids.md_list.clear_widgets()
            for audiobook in MDApp.get_running_app().downloaded_audiobook_list:
                if text in audiobook.lower():
                    self.ids.md_list.add_widget(
                        SwipeToDeleteItem(text=f"{audiobook}".title(
                        ), secondary_text=f"{self.dict_book_link[audiobook][0]}", source=f"{self.dict_book_link[audiobook][1]}")
                    )

        else:
            for audiobook in MDApp.get_running_app().downloaded_audiobook_list:
                self.ids.md_list.add_widget(
                    SwipeToDeleteItem(text=f"{audiobook}".title(
                    ), secondary_text=f"{self.dict_book_link[audiobook][0]}", source=f"{self.dict_book_link[audiobook][1]}")
                )



class WelcomeScreen(MDScreen):

    def load(self, direction, *args):
        if direction == 'skip':
            self.ids.carousel.load_slide(self.ids.carousel.slides[2])
            for i in self.ids.swipe_dots.children:
                i.icon_color = (0, 0, 0, 0.6)
            self.ids.swipe_dots.children[0].icon_color = utils.get_color_from_hex(
                colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_light_hue])
            self.ids.start_buttons.children[1].pos = (
                -dp(100),  self.height/14)
            self.ids.start_buttons.children[0].text = "START"

        elif direction == 'next' or direction == 'start':
            self.ids.carousel.load_next(mode='next')

            if self.ids.carousel.index != 2:
                for i in self.ids.swipe_dots.children:
                    i.icon_color = (0, 0, 0, 0.6)
                list(reversed(self.ids.swipe_dots.children))[self.ids.carousel.index+1].icon_color = utils.get_color_from_hex(
                    colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_light_hue])

            if self.ids.carousel.index == 1:
                self.ids.start_buttons.children[1].pos = (
                    -dp(100),  self.height/14)
                self.ids.start_buttons.children[0].text = "START"



sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(MenuScreen(name='menuscreen'))
sm.add_widget(PlayScreen(name='playscreen'))


class MainApp(MDApp):

    def build(self):
        # defining color themes for the app
        # yeah don`t really see any change, except for the change that it brings out in the shape of floatingactionbutton. Otherwise, it is pretty useless ig
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style_switch_anmation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.56060
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.primary_dark_hue = "900"
        self.theme_cls.primary_light_hue = "200"
        # ______________________________________________

        self.sleep_timer = None

        self.screens = Builder.load_string(kivy_string)

        # returned_response = requests.get(r'https://raw.githubusercontent.com/R-Anurag/kivy-audiobook-app/main/assets/links/book%20link%20dict.yaml', headers={
        #                                  'user-agent': 'Mozilla/4.0 (compatible; MS60IE 5.5; Windows NT)'})

        # self.dict_book_link = yaml.safe_load(returned_response.content)

        with open('app data/book link dict.yaml', 'r') as file:
            self.dict_book_link = yaml.safe_load(file)

        self.downloaded_audiobook_list = []

        file = "app data/downloaded_audiobooks.dat"
        if os.path.isfile(file):
            with open(file, "rb") as file_object:
                try:
                    while True:
                        self.downloaded_audiobook_list.append(
                            pickle.load(file_object))
                except EOFError:
                    pass

        for i in self.downloaded_audiobook_list:
            self.screens.get_screen('menuscreen').ids.md_list.add_widget(
                SwipeToDeleteItem(text=f"{i}".title(
                ), secondary_text=f"{self.dict_book_link[i][0]}", source=f"{self.dict_book_link[i][1]}")
            )

        # Sleep timer drop-down menu
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "text": "[size=16sp][font=DejaVuSans][b]" + [f"{i} minutes" if i != 'End of Episode' else i][0] + "[/b][/font][/size]",
                "theme_text_color": "Custom",
                "text_color": (1, 1, 1, 1),
                # "bg_color": (0,0,0,0.35),
                "on_press": lambda x=i: Snackbar(text=f"[b]The audio will stop in {x} seconds[/b]", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                                                 snackbar_y="10dp", size_hint_x=(self.screens.get_screen('menuscreen').width - 20) / self.screens.get_screen('menuscreen').width, elevation=2).open(),
                "on_release": lambda x=i: self.sleep_menu_callback(x),
            } for i in [5, 10, 15, 30, 45, 'End of Episode']
        ]

        self.sleep_menu = MDDropdownMenu(
            header_cls=MenuHeader(icon="sleep", label="Stop  audio  in"),
            caller=self.screens.get_screen(
                'playscreen').ids.sleep_timer_button,
            items=menu_items,
            width_mult=4,
            position="bottom",
            ver_growth="down",
            hor_growth="left",
            border_margin=dp(20),
            elevation=4,
            # max_height=dp(112),
            # border_margin=dp(24),
            radius=[24, 4, 24, 4],
            background_color=utils.get_color_from_hex(
                colors[self.theme_cls.primary_palette][self.theme_cls.primary_hue])
        )

        # _________________________________________________________________________________

        # Theme colour of the app

        theme_color_menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "invert-colors",
                "icon_color": utils.get_color_from_hex(colors[i]['300']),
                "theme_text_color": "Custom",
                "text_color": (1, 1, 1, 0.9),
                "height": dp(40),
                "text": "[size=16][font=DejaVuSans]" + f"{i}" + "[/font][/size]",
                "bg_color": utils.get_color_from_hex(colors[i]['900']),
                "on_release": lambda x=f"{i}": self.theme_color_menu_callback(x),
            } for i in ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        ]

        self.theme_menu = MDDropdownMenu(
            header_cls=MenuHeader(icon="select-color",
                                  label="Select  theme - color"),
            items=theme_color_menu_items,
            ver_growth="up",
            hor_growth="left",
            width_mult=5,
            elevation=4,
            max_height=dp(412),
            border_margin=dp(20),
            # border_margin=dp(24),
            radius=[24, 4, 24, 4],
            background_color=utils.get_color_from_hex(
                colors[self.theme_cls.primary_palette][self.theme_cls.primary_hue])
        )

        return self.screens

    def sleep_button_fun(self, instance):

        if instance.icon_color == utils.get_color_from_hex(
                colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_dark_hue]):

            self.change_sleep_button_color()

            Clock.unschedule(self.make_playing_audio_pause)

            Snackbar(text=f"The Audio stop-timer is removed!", snackbar_x="10dp", bg_color=utils.get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue]),
                     snackbar_y="10dp", size_hint_x=(self.screens.get_screen('menuscreen').width - 20) / self.screens.get_screen('menuscreen').width, elevation=2).open()

        else:
            self.sleep_menu.open()

    def make_playing_audio_pause(self, *kwargs):
        if self.screens.get_screen('playscreen').audiobook.state == 'play':
            # who knows if the user stops the audio himself before the timer hits
            self.screens.get_screen('playscreen').play_pause()
        self.change_sleep_button_color()

    def sleep_menu_callback(self, instance):

        Clock.schedule_once(self.make_playing_audio_pause, instance)

        self.screens.get_screen('playscreen').ids.sleep_timer_button.icon_color = utils.get_color_from_hex(
            colors[MDApp.get_running_app().theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_dark_hue])

        if self.screens.get_screen('playscreen').audiobook.state == 'stop':
            self.screens.get_screen("playscreen").play_pause()
        else:
            # The audio is already playing so wouldn`t need playing it.. FOR it to be stopped later at the timer ending
            pass

        self.sleep_menu.dismiss()

    def theme_color_menu_callback(self, selected_color):
        self.theme_cls.primary_palette = selected_color
        self.sleep_menu.background_color = utils.get_color_from_hex(colors[MDApp.get_running_app(
        ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue])
        self.theme_menu.background_color = utils.get_color_from_hex(colors[MDApp.get_running_app(
        ).theme_cls.primary_palette][MDApp.get_running_app().theme_cls.primary_hue])
        self.sleep_menu.dismiss()
        self.screens.get_screen('menuscreen').ids.here_label.text = f'[color={colors[self.theme_cls.primary_palette][self.theme_cls.primary_hue]}]here[/color]' if self.screens.get_screen('menuscreen').ids.md_list.children == [] else ""

    def change_sleep_button_color(self, *args):
        self.screens.get_screen(
            'playscreen').ids.sleep_timer_button.icon_color = (1, 1, 1, 1)

    def on_start(self):
        if os.path.exists('app data/downloaded_audiobooks.dat'):
            self.screens.get_screen(
                'welcomescreen').manager.current = 'menuscreen'

    def on_stop(self):
        try:
            self.screens.get_screen('playscreen').audiobook.unload()
        except AttributeError:
            pass


MainApp().run()
