from kibot import Kibot
from kivy.factory import Factory

if __name__ == '__main__':
    # A kibot testing example
    from kivy.app import App
    from kivy.lang import Builder
    kv = """
<RootWidget@BoxLayout>:
    orientation: 'vertical'
    BoxLayout:
        Button:
            text: "Kibot Test"
            on_press: self.text="Pressed!"
        TextInput:
    Slider:
        step: 1
        on_value: _lbl.text="%s"%(self.value)
    Label:
        id: _lbl
        size_hint_y: 0.1
"""

    class TestApp(App):

        def build(self):
            return Factory.RootWidget()

    def test(t):
        kibot.execute_record()

    Builder.load_string(kv)
    app = TestApp()  # Do not run the app!
    kibot = Kibot(app)
    kibot.record()  # Record events
    #  Comment previous line and uncomment next one to execute recorded events
    # kibot.execute_record('test.kibot')
    app.run()
