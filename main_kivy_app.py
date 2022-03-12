from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.image import AsyncImage

from Nasa_map import *
import time


def get_nasa_daily_data() -> dict:
    url = 'https://api.nasa.gov/planetary/apod?api_key=fM34eU62v6JIHGlv9kZ1QLvTyTK9nwimaIG4oxOu'
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    nasa_daily = {'image_url': result['url'],
                  'title': result['title']}
    return nasa_daily


class NasaAPiApp(App):
    def build(self):
        nasa_daily: dict = get_nasa_daily_data()
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.greeting = Label(
            text=f"{nasa_daily['title']}\n(From Nasa Astronomy Picture of the Day)\n\nChose your map style now ;)",
            font_size=14,
            color='#00FFCE'
        )

        self.window.add_widget(AsyncImage(
            source=nasa_daily['image_url']))

        self.window.add_widget(self.greeting)

        self.button_old = Button(
            text="old style",
            size_hint=(1, 0.2),
            bold=True,
            background_color='#00FFCE',
        )

        self.button_now_physical = Button(
            text="physical map",
            size_hint=(1, 0.2),
            bold=True,
            background_color='#00FFCE',
        )

        self.button_now_political = Button(
            text="political map",
            size_hint=(1, 0.2),
            bold=True,
            background_color='#00FFCE',
        )
        self.button_old.bind(on_press=self.choice_old_map)
        self.button_now_physical.bind(on_press=self.choice_physical_map)
        self.button_now_political.bind(on_press=self.choice_political_map)
        self.window.add_widget(self.button_old)
        self.window.add_widget(self.button_now_physical)
        self.window.add_widget(self.button_now_political)
        return self.window

    @staticmethod
    def close_app():
        App.get_running_app().stop()
        Window.close()

    def choice_old_map(self, instance):
        self.close_app()
        map_main('old')

    def choice_physical_map(self, instance):
        self.close_app()
        map_main('physical')

    def choice_political_map(self, instance):
        self.close_app()
        map_main('political')


if __name__ == "__main__":
    NasaAPiApp().run()
