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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.color_definitions import colors
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
# from kivy.utils import platform
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.text import Label as CoreLabel
import shutil
import yaml
import time
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



# Changing the audioplayer library since the default audio_sdl2 does not provide seek operation

import os
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
os.environ['KIVY_AUDIO'] = 'ffpyplayer'
    
# ================================================================= 




KV = '''
#:import utils kivy.utils
#:import colors kivymd.color_definitions.colors
#: import SwapTransition kivy.uix.screenmanager.SwapTransition


<MenuHeader>
    orientation: "vertical"
    adaptive_size: True
    padding: "4dp"

    MDBoxLayout:
        spacing: "12dp"
        adaptive_size: True

        MDIconButton:
            icon: "bed-clock"
            theme_icon_color: "Custom"
            icon_color: '#FFFFFF'
            pos_hint: {"center_y": .5}

        MDLabel:
            markup: True
            text: "[b]Stop audio in[/b]"
            theme_text_color: "Custom"
            text_color: '#FFFFFF'
            font_name: "DejaVuSans"
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
    on_swipe_complete: app.get_running_app().screens.get_screen('menuscreen').remove_item(root)


    MDCardSwipeLayerBox:
        padding: "8dp"
        md_bg_color: utils.get_color_from_hex(colors['DeepOrange']['400'])

        MDIconButton:
            icon: "trash-can"
            theme_icon_color: "Custom"
            icon_color: 1,1,1,0.8
            pos_hint: {"center_y": .5}

    MDCardSwipeFrontBox:
        md_bg_color: 1,1,1,0.8

        TwoLineAvatarListItem:
            id: content
            text: "[size=18]"+root.text+"[/size]"
            secondary_text: "[size=14]"+root.secondary_text+"[/size]"
            text_color: 1, 1, 1, 1
            secondary_text_color: 1, 2, 1, 1 
            _no_ripple_effect: True
            # bg_color: utils.get_color_from_hex(colors['Purple']['300'])
            on_release: 
                app.get_running_app().screens.get_screen('menuscreen').insert_audiobook_parts(root)
                app.root.transition = SwapTransition()
                app.root.current = 'playscreen'

            ImageLeftWidget:
                source: root.source



<ListItemWithCheckbox>:
    _no_ripple_effect: True
    AsyncImage:
        source: root.source
        size_hint: None, None
        size:self.image_ratio*root.height,root.height/1.5
        mipmap: True 
        pos_hint: {'center_x':0.1, 'center_y': 0.5}
        disabled: True
     
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
    audiobook_primary_text: 'No audiobooks found'
    audiobook_secondary_text: 'Click the + button to insert local audiobooks or download avaialable audiobooks from the server'
    gif_source: "assets/images/welcome cat.zip"
    gif_source_2: "assets/images/catplayingdark.zip"

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
            source: root.gif_source if md_list.children == [] else root.gif_source_2
            size_hint: (0.3, 0.3) if md_list.children == [] else (0.22, 0.22)
            pos_hint: {"center_x": 0.5, "center_y": 0.6} if md_list.children == [] else {"center_x": 0.85, "center_y": 0.93}
            anim_delay: 0.1
            minimap: True
            allow_stretch: True
        
        MDScrollView:
            size_hint: (0.98, 0.81)
            pos_hint: {"center_x": 0.5, "center_y": 0.41} 
            do_scroll_y: False
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
            font_size: self.width/13
            bold: True
            text: root.audiobook_primary_text if md_list.children == [] else ""
            font_name: "assets/fonts/PlayfairDisplay-Bold.ttf"
            # font_name: "Roboto Mono Regular"
            halign: 'center'
            size_hint_x: 0.9
            pos_hint: {'center_x':0.5, 'center_y':0.50}
            theme_text_color: 'Custom'
            text_color: utils.get_color_from_hex(colors['Gray']['400'])  
        
        MDLabel:
            font_size: self.width/20
            bold: True
            text: root.audiobook_secondary_text if md_list.children == [] else ""
            font_name: "assets/fonts/PlayfairDisplay-Regular.ttf"
            # font_name: "assets/fonts/Aclonica.ttf"
            halign: 'center'
            size_hint_x: 0.9
            pos_hint: {'center_x':0.5, 'center_y':0.42}
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
    canvas.before:
        Color:
            rgba: eval(f"utils.get_color_from_hex(colors['DeepPurple']['A700'])")
        Rectangle:
            pos: self.pos
            size: self.size
        
    
    MDFloatLayout:
        id: playerpart
        size_hint: 1, 0.8
        pos_hint: {"center_x": .5, "center_y": .58}
        orientation: 'horizontal'

        MagicCard:
            padding: "2dp"
            ripple_behavior: False
            orientation: "horizontal"
            size_hint: (1, .07)
            focus_behavior: False
            pos_hint: {"center_x": .5, "center_y": 1}
            md_bg_color: (0, 0, 0, 0.25)

        MDLabel:
            id: top_bar_heading
            text: ""
            font_size: 14
            font_name: 'DejaVuSans'
            halign: "center"
            # theme_text_color: "Hint"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            pos_hint: {"center_x": 0.5, "center_y": 1}

        MDLabel:
            id: top_bar_sub_heading
            text: ""
            font_size: 10
            font_name: 'DejaVuSans'
            halign: "center"
            # theme_text_color: "Hint"
            theme_text_color: "Custom"
            text_color: 1,1,1,0.8
            pos_hint: {"center_x": 0.5, "center_y": 0.98}

                
        MDIconButton:
            id: sleep_timer_button
            icon: "power-sleep"
            icon_size: "22sp" 
            pos_hint: {"center_x": 0.9, "center_y": 0.99}
            theme_icon_color: "Custom"
            icon_color: 1,1,1,1
            on_release:
                app.sleep_menu.open()

        
        MDIconButton:
            icon: "chevron-down"
            icon_size: "18sp" 
            pos_hint: {"center_x": 0.5, "center_y": 0.96}
            theme_icon_color: "Custom"
            icon_color: (0, 0, 0, 0.25)
            padding: "10sp"
            radius: [0, 0, 64, 64]
            on_release:
                app.get_running_app().screens.get_screen('playscreen').audiobook.stop()
                self.manager.current = 'menuscreen'
            

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
            size_hint: (0.7, 0.41)
            source: ""
            radius: (6, 6, 6, 6)
            pos_hint: {"center_x": .5, "center_y": .63}

        MDLabel:
            id: audiobook_part_name
            text: ""
            font_size: 18
            font_name: 'DejaVuSans'
            halign: "left"
            # theme_text_color: "Hint"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
            pos_hint: {"center_x": .62, "center_y": .38}

        Marquee:
            id: audiobook_album_name
            text: ''
            font_name: 'DejaVuSans'
            duration: 7
            padding: 10
            pos_hint: {'center_x': 0.5, 'center_y': 0.82}
            size_hint_x: 0.76
            
        MySlider:
            id: slider
            color: (1, 1, 1, 1)
            thumb_color_active: "white"
            thumb_color_inactive: "black"
            min: 0
            sound: None
            max: 0
            value: 0
            pos_hint: {'center_x': 0.50, 'center_y': 0.30}
            size_hint: (0.85, 0.1)        
            hint: True
            track: True
            track_color_active: utils.get_color_from_hex(colors['Purple']['700'])
            track_color_inactive: (1,0,1,1)  

        MDBoxLayout:
            orientation: "horizontal"
            padding: (0,8,0,0)
            size_hint: 0.76, None
            height: self.minimum_height
            pos_hint: {'center_x': 0.50, 'center_y': 0.27}

            MDLabel:
                id: sound_pos_label
                text: "0.0"
                font_size: 14
                halign: "left"
                # theme_text_color: "Hint"
                theme_text_color: "Custom"
                text_color: 1,1,1,1

            
            MDLabel:
                id: sound_length_label
                text: "1.0"
                font_size: 14
                halign: "right"
                # theme_text_color: "Hint"
                theme_text_color: "Custom"
                text_color: 1,1,1,1
            
        MDFloatLayout:
            size_hint: 0.76, None
            pos_hint: {'center_x': 0.50, 'center_y': 0.28}
            
            MDIconButton:
                icon: "rewind-10"
                icon_size: "28sp" 
                pos_hint: {'center_x': 0.30, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1
                on_release:
                    self.parent.parent.parent.audiobook.seek(self.parent.parent.parent.audiobook.get_pos() - 10) if self.parent.parent.parent.audiobook.get_pos() > 0.1 else self.parent.parent.parent.audiobook.get_pos()
                    #note that the else part just loses the value and is done just to complete the if else structure whichw as necessary

            MDIconButton:
                id: play_pause_button
                icon: "play-circle"
                icon_size: "48sp" 
                pos_hint: {'center_x': 0.50, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1
                on_release:
                    self.parent.parent.parent.play_pause()


            MDIconButton:
                icon: "fast-forward-10"
                icon_size: "28sp"  
                pos_hint: {'center_x': 0.70, 'center_y': 0}
                theme_icon_color: "Custom"
                icon_color: 1,1,1,1 
                on_release:
                    self.parent.parent.parent.audiobook.seek(self.parent.parent.parent.audiobook.get_pos() + 10) if self.parent.parent.parent.audiobook.get_pos() > 0.1 else 0
                    #note that the else part is done just to complete the if else structure whichw as necessary
            
            MDIconButton:
                icon: "skip-previous"
                theme_icon_color: "Custom"
                icon_color: utils.get_color_from_hex(colors['Gray']['100'])
                icon_size: "28sp"  
                pos_hint: {'center_x': 0.05, 'center_y': 0}
                on_release:
                    self.parent.parent.parent.load_audiobook(int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5])-1) if int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5]) > int(list(app.get_running_app().screens.get_screen('menuscreen').dict_book_link[audiobook_part_name.text[:audiobook_part_name.text.index(':')].lower()][2].keys())[0].replace('part','')) else 0
                    
            MDIconButton:
                icon: "skip-next"
                theme_icon_color: "Custom"
                icon_color: utils.get_color_from_hex(colors['Gray']['100'])
                icon_size: "28sp"  
                pos_hint: {'center_x': 0.95, 'center_y': 0}
                on_release:
                    self.parent.parent.parent.load_audiobook(int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5:])+1) if int(audiobook_part_name.text[audiobook_part_name.text.index('Part')+5:]) < int(list(app.get_running_app().screens.get_screen('menuscreen').dict_book_link[audiobook_part_name.text[:audiobook_part_name.text.index(':')].lower()][2].keys())[-1].replace('part','')) else 0
                    

    
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

class MenuHeader(MDBoxLayout):
    '''An instance of the class that will be added to the menu header.'''

class Marquee(MDFloatLayout):
    texture = ObjectProperty()
    text = StringProperty()
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
        label = CoreLabel(text=self.text, font_name=self.font_name, font_size=self.font_size,
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

        
        self.audiobook = SoundLoader.load(f"app data/audiobooks/{MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook}/part{part_number}.mp3")

        self.playscreen_ids = MDApp.get_running_app().screens.get_screen('playscreen').ids
        self.slider = self.playscreen_ids.slider
        self.playscreen_ids.album_picture.source = MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][1]
        self.playscreen_ids.audiobook_album_name.text = MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0]
        self.playscreen_ids.audiobook_part_name.text = MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook.title() + f": Part-{part_number}"
        self.playscreen_ids.top_bar_heading.text = MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0].replace(MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0][MDApp.get_running_app().screens.get_screen('menuscreen').dict_book_link[MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook][0].index('by'):],'')
        self.playscreen_ids.top_bar_sub_heading.text = MDApp.get_running_app().screens.get_screen('menuscreen').selected_audiobook.title() + f": Part-{part_number}"


        self.slider.sound = self.audiobook
        self.slider.max = self.audiobook.length

        self.playscreen_ids.sound_length_label.text = time.strftime("%H:%M:%S", time.gmtime(self.audiobook.length))
        
        self.updater = None
        self.paused = False     

        self.audiobook_part_selected = [i for i in MDApp.get_running_app().screens.get_screen('playscreen').ids.md_list_2.children if int(i.text.lower().replace("part-","").strip()) == part_number][0]
        
        MDApp.get_running_app().screens.get_screen('menuscreen').part_highlight(self.audiobook_part_selected)
        
        MDApp.get_running_app().screens.get_screen('playscreen').ids.md_list_2.parent.scroll_to(self.audiobook_part_selected)

        self.play_pause()


    def play_pause(self, *args):

        if self.updater is None:
            # schedule updates to the slider
            self.updater = Clock.schedule_interval(self.update_slider, 0.5)

        if self.paused == True:
            self.audiobook.seek(self.stop_position)
            self.audiobook.play()
            self.playscreen_ids.play_pause_button.icon = "play-circle"
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
            

    def update_slider(self, *args):
        # update slider
        self.slider.value = self.audiobook.get_pos()
        # updating the sound position label as well here
        self.playscreen_ids.sound_pos_label.text = time.strftime("%H:%M:%S", time.gmtime(self.audiobook.get_pos()))
        # if the sound has finished, stop the updating
        if self.audiobook.state == 'stop' and self.updater != None:            
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
        

        returned_response = requests.get(r'https://raw.githubusercontent.com/R-Anurag/kivy-audiobook-app/main/assets/links/book%20link%20dict.yaml',headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}) 
        
        self.dict_book_link = yaml.safe_load(returned_response.content )

        
    def remove_item(self, instance):
        
        if os.path.exists(f"app data/audiobooks/{instance.text.lower()}"):
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


    def show_download_list(self, *kwargs):

        already_downloaded_audiobooks = []

        if os.path.isfile("app data/downloaded_audiobooks.dat"):
            
            with (open("app data/downloaded_audiobooks.dat", "rb")) as openfile:
                
                try:
                    while True:
                        already_downloaded_audiobooks.append(pickle.load(openfile))
                except EOFError:
                    pass

    
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
        self.thread.setDaemon(True)
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

        if set(self.selected_books) == set(self.downloaded_audiobooks):
            with open(r"app data/downloaded_audiobooks.dat", "ab") as file:
                for i in self.selected_books:
                    MDApp.get_running_app().screens.get_screen('menuscreen').ids.md_list.add_widget(
                        SwipeToDeleteItem(text=f"{i}".title(), secondary_text=f"{self.dict_book_link[i][0]}", source=f"{self.dict_book_link[i][1]}", 
                        md_bg_color=(1,2,1,1 ))
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
            
                download_dialog.dismiss()

            
                
        with ThreadPoolExecutor() as executor:
            executor.map(download_file, complete_url_list_with_filepath)


    def insert_audiobook_parts(self, instance):

        self.selected_audiobook = instance.text.lower()

        for i in self.dict_book_link[instance.text.lower()][2]:
            MDApp.get_running_app().screens.get_screen('playscreen').ids.md_list_2.add_widget(
            OneLineAvatarIconListItem(IconLeftWidget(icon="headphones", theme_icon_color="Custom",icon_color=(1,1,1,1)), text=f"{i}".replace('part','part-').title(), theme_text_color="Custom",text_color=(1,1,1,1), radius=[10, ]
            # , bg_color = (0,0,0,0.35)
            ,on_press=self.part_highlight, 
            on_release=lambda x: MDApp.get_running_app().screens.get_screen('playscreen').load_audiobook(int(x.text.replace('Part-','').lower()))
            )
            )
            

    def part_highlight(self, instance):
        for i in instance.parent.parent.children[0].children:
            i.bg_color = (0,0,0,0)
        else:
            instance.bg_color = utils.get_color_from_hex(colors['Purple']['A700'])
    

sm = MDScreenManager()
sm.add_widget(MenuScreen(name='menuscreen'))
sm.add_widget(PlayScreen(name='playscreen'))


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screens = Builder.load_string(KV)

        returned_response = requests.get(r'https://raw.githubusercontent.com/R-Anurag/kivy-audiobook-app/main/assets/links/book%20link%20dict.yaml',headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}) 
        
        self.dict_book_link = yaml.safe_load(returned_response.content )
    
        downloaded_audiobook_list = []

        file = "app data/downloaded_audiobooks.dat"
        if os.path.isfile(file): 
            with open(file, "rb") as file_object:
                try:
                    while True:
                        downloaded_audiobook_list.append(pickle.load(file_object))
                except EOFError:
                    pass

        for i in downloaded_audiobook_list:
            MDApp.get_running_app().screens.get_screen('menuscreen').ids.md_list.add_widget(
                SwipeToDeleteItem(text=f"{i}".title(), secondary_text=f"{self.dict_book_link[i][0]}", source=f"{self.dict_book_link[i][1]}", 
                md_bg_color=(1,2,1,1 ))
            )

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "text": "[size=14][font=DejaVuSans]" + [f"{i} minutes" if i != 'End of Episode' else i][0] + "[/font][/size]",
                "theme_text_color": "Custom",
                "text_color": (1,1,1,1),
                # "bg_color": (0,0,0,0.35),
                "on_release": lambda x=i: self.sleep_menu_callback(x),
            } for i in [5, 10, 15, 30, 45, 'End of Episode'] 
        ]

        self.sleep_menu = MDDropdownMenu(
            header_cls=MenuHeader(),
            caller=self.screens.get_screen('playscreen').ids.sleep_timer_button,
            items=menu_items,
            width_mult=4,
            elevation=1,
            # max_height=dp(112),
            # border_margin=dp(24),
            radius=[24, 4, 24, 4],
            background_color=utils.get_color_from_hex(colors['Purple']['A700'])
        )
    
    def sleep_menu_callback(self, instance):
        if instance != 'End of Episode':
            print('sleep function called ')
            # Clock.schedule_once(self.screens.get_screen('playscreen').audiobook.stop(), instance*60)
        


    def on_stop(self):
        try:
            self.screens.get_screen('playscreen').audiobook.unload()
        except AttributeError:
            pass        


    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Light"

        return self.screens
    
    
    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
   
    def on_start(self):
        pass 
        

MainApp().run()