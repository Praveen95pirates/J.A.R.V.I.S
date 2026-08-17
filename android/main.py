#!/usr/bin/env python3
"""
J.A.R.V.I.S. Android Application
Kivy-based Android app with voice, chat, trading, and skill manager
"""

import os
import sys
import json
import threading
import requests
import speech_recognition as sr

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.metrics import dp

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

SERVER_URL = "http://192.168.1.111:5000"


class MessageWidget(BoxLayout):
    def __init__(self, sender, text, emotion=None, intensity=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = dp(8)
        self.spacing = dp(8)
        color = (0.3, 0.6, 1, 1) if sender == 'user' else (0.4, 0.8, 1, 1)
        self.add_widget(Label(text='You' if sender == 'user' else 'J.A.R.V.I.S.', color=color, bold=True, size_hint_x=0.25))
        display = text if len(text) < 120 else text[:117] + '...'
        self.add_widget(Label(text=display, color=(0.9, 0.9, 0.9, 1), text_size=(Window.width * 0.65, None), halign='left', valign='middle'))


class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voice_active = False

    def on_enter(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.chat_scroll = ScrollView()
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        layout.add_widget(self.chat_layout)
        input_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        self.text_input = TextInput(hint_text='Message J.A.R.V.I.S...', multiline=False, size_hint_x=0.7, background_color=(0.1, 0.1, 0.2, 1), foreground_color=(0.9, 0.9, 0.9, 1), padding=[dp(10), dp(15)])
        self.text_input.bind(on_text_validate=self.send_message)
        send_btn = Button(text='Send', size_hint_x=0.3, background_color=(0.4, 0.8, 1, 1), background_normal='')
        send_btn.bind(on_press=self.send_message)
        input_row.add_widget(self.text_input)
        input_row.add_widget(send_btn)
        layout.add_widget(input_row)
        voice_btn = Button(text='🎤', size_hint_y=None, height=dp(50), background_color=(1, 0.6, 0, 1), background_normal='')
        voice_btn.bind(on_press=self.toggle_voice)
        layout.add_widget(voice_btn)
        self.clear_widgets()
        self.add_widget(layout)
        Clock.schedule_once(lambda dt: self.add_message('system', 'Connected to J.A.R.V.I.S. via Android.'), 0.1)

    def add_message(self, sender, text, emotion=None, intensity=None):
        w = MessageWidget(sender, text, emotion, intensity)
        self.chat_layout.add_widget(w)
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll, 'scroll_y', 0), 0.1)

    def send_message(self, instance=None):
        message = self.text_input.text.strip()
        if not message:
            return
        self.add_message('user', message)
        self.text_input.text = ''
        threading.Thread(target=self._send, args=(message,), daemon=True).start()

    def _send(self, message):
        try:
            r = requests.post(f"{SERVER_URL}/api/chat", json={'message': message}, timeout=30)
            data = r.json()
            Clock.schedule_once(lambda dt: self.add_message('jarvis', data.get('response', '')), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_message('system', f'Error: {str(e)}'), 0)

    def toggle_voice(self, instance):
        if not self.voice_active:
            self.voice_active = True
            instance.text = '🔴'
            instance.background_color = (1, 0.3, 0.3, 1)
            threading.Thread(target=self._listen_loop, daemon=True).start()
        else:
            self.voice_active = False
            instance.text = '🎤'
            instance.background_color = (1, 0.6, 0, 1)

    def _listen_loop(self):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
            while self.voice_active:
                try:
                    with sr.Microphone() as source:
                        audio = r.listen(source, timeout=3, phrase_time_limit=8)
                    text = r.recognize_google(audio)
                    if text and self.voice_active:
                        Clock.schedule_once(lambda dt, t=text: self._process_voice(t), 0)
                except Exception:
                    continue
        except Exception as e:
            print('[Voice] Mic error', e)

    def _process_voice(self, text):
        if 'jarvis' in text.lower():
            cmd = text.lower().replace('jarvis', '').strip()
            if cmd:
                self.add_message('user', text)
                self.text_input.text = cmd
                self.send_message()
            else:
                self.add_message('system', 'J.A.R.V.I.S. activated.')
        else:
            self.add_message('user', text)
            self.text_input.text = text
            self.send_message()


class TradingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.status_label = Label(text='Trading skills ready', size_hint_y=None, height=dp(30), color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.status_label)
        self.output_label = Label(text='', color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.output_label)
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(520))
        buttons = [
            ('Quotes', lambda *a: self.call_trading('stock_quotes', {"symbols": ["RELIANCE","TCS","INFY"]})),
            ('Crypto', lambda *a: self.call_trading('crypto_trading', {"symbols": ["BTCUSD","ETHUSD","SOLUSD"]})),
            ('Forex', lambda *a: self.call_trading('forex_trading', {"symbols": ["EURUSD","GBPUSD","USDJPY"]})),
            ('Technical', lambda *a: self.call_trading('technical_analysis', {"symbol": "RELIANCE"})),
            ('Portfolio', lambda *a: self.call_trading('portfolio_tracking', {})),
            ('Risk', lambda *a: self.call_trading('risk_management', {"symbol": "RELIANCE", "quantity": 10})),
            ('Options', lambda *a: self.call_trading('options_analytics', {"symbol": "RELIANCE"})),
            ('Alerts', lambda *a: self.call_trading('alert_management', {"action": "list"})),
            ('News', lambda *a: self.call_trading('news_sentiment', {"symbols": ["RELIANCE", "INFY"]})),
            ('Calendar', lambda *a: self.call_trading('economic_calendar', {})),
            ('Paper Reset', lambda *a: self.call_trading('paper_trading', {"action": "reset"})),
            ('Paper Balance', lambda *a: self.call_trading('paper_trading', {"action": "balance"})),
        ]
        for name, fn in buttons:
            b = Button(text=name, background_color=(0.2, 0.5, 0.9, 1), background_normal='')
            b.bind(on_press=fn)
            grid.add_widget(b)
        scroll = ScrollView()
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.clear_widgets()
        self.add_widget(layout)

    def call_trading(self, skill, payload):
        self.status_label.text = f'Calling {skill}...'
        threading.Thread(target=self._do_call, args=(skill, payload), daemon=True).start()

    def _do_call(self, skill, payload):
        try:
            r = requests.post(f"{SERVER_URL}/api/trading/{skill}", json=payload, timeout=30)
            data = r.json()
            Clock.schedule_once(lambda dt: self._show(data), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show({'error': str(e)}), 0)

    def _show(self, data):
        self.status_label.text = 'Result'
        try:
            self.output_label.text = json.dumps(data, indent=2)
        except Exception:
            self.output_label.text = str(data)


class SkillsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.status_label = Label(text='Loading skills...', size_hint_y=None, height=dp(30), color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.status_label)
        self.output_label = Label(text='', color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.output_label)
        refresh_btn = Button(text='Refresh Skills', size_hint_y=None, height=dp(50), background_color=(0.4, 0.8, 1, 1), background_normal='')
        refresh_btn.bind(on_press=lambda *a: self.load_skills())
        layout.add_widget(refresh_btn)
        self.clear_widgets()
        self.add_widget(layout)
        Clock.schedule_once(lambda dt: self.load_skills(), 0.1)

    def load_skills(self):
        threading.Thread(target=self._do_load, daemon=True).start()

    def _do_load(self):
        try:
            r = requests.get(f"{SERVER_URL}/api/skill-manager/skills", timeout=30)
            data = r.json()
            Clock.schedule_once(lambda dt: self._show(data), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show({'error': str(e)}), 0)

    def _show(self, data):
        self.status_label.text = f"Skills: {data.get('enabled', 0)}/{data.get('total', 0)}"
        try:
            self.output_label.text = json.dumps(data, indent=2)
        except Exception:
            self.output_label.text = str(data)


class JarvisAndroidApp(App):
    title = "J.A.R.V.I.S."

    def build(self):
        Window.clearcolor = (0.04, 0.05, 0.15, 1)
        sm = ScreenManager()
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(TradingScreen(name='trading'))
        sm.add_widget(SkillsScreen(name='skills'))
        root = BoxLayout(orientation='vertical')
        nav = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        chat_btn = Button(text='Chat', background_color=(0.4, 0.8, 1, 1), background_normal='')
        chat_btn.bind(on_press=lambda *a: setattr(sm, 'current', 'chat'))
        trade_btn = Button(text='Trading', background_color=(0.2, 0.7, 0.4, 1), background_normal='')
        trade_btn.bind(on_press=lambda *a: setattr(sm, 'current', 'trading'))
        skills_btn = Button(text='Skills', background_color=(0.8, 0.4, 0.2, 1), background_normal='')
        skills_btn.bind(on_press=lambda *a: setattr(sm, 'current', 'skills'))
        nav.add_widget(chat_btn)
        nav.add_widget(trade_btn)
        nav.add_widget(skills_btn)
        root.add_widget(nav)
        root.add_widget(sm)
        return root

    def on_start(self):
        print('[Android] J.A.R.V.I.S. started')
        print(f'[Android] Connecting to: {SERVER_URL}')

    def on_stop(self):
        print('[Android] J.A.R.V.I.S. stopped')


if __name__ == '__main__':
    JarvisAndroidApp().run()
