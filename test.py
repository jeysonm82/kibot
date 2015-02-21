from kibot import Kibot, KibotTestCase, run_kibot_tests


class KibotTestExample(KibotTestCase):

    def test_button_text_equals_pressed(self):
        """Test that my_button has proper text after one click/touch """

        kibot = Kibot(self.app)
        # find button by tag property
        my_button = kibot.find(text="Kibot Test")
        kibot.do_click(widget=my_button)  # click my button
        kibot.wait_until()  # wait until all events are executed
        # always call this before asserts

        self.assertEqual(my_button.text, "Pressed!")

    def test_textinput(self):
        """Test that my_textinput has proper text after keyboard input"""
        kibot = Kibot(self.app)
        my_textinput = kibot.find(class_="TextInput")
        kibot.do_click(widget=my_textinput)
        kibot.do_keystroke(text="hello")  # Sends hello using keyboard
        kibot.do_keystroke(key="enter")  # Simulates Enter key
        kibot.do_keystroke(text="world")
        kibot.wait_until()  # wait until all events are executed

        self.assertEqual(my_textinput.text, "hello\nworld")

    def test_slider_and_label(self):
        """Test that slider has proper value and label has proper text after
        touch"""
        kibot = Kibot(self.app)
        my_slider = kibot.find(class_="Slider")
        my_label = kibot.find(class_="Label")
        # touch at x=79% of widget's width, and y=50% of widget's height
        # relative to widget's position
        kibot.do_press(widget=my_slider, x=0.0, y=0.5)
        kibot.delta_time = 0.05
        for i in range(80):
            kibot.do_move(widget=my_slider, x=i / 100., y=0.5)
        kibot.do_release(widget=my_slider, x=0.0, y=0.5)

        kibot.wait_until()

        # On my pc that touch sets slider value to 80
        self.assertEqual(my_slider.value, 80)
        self.assertEqual(my_label.text, "80.0")

if __name__ == '__main__':
    # A kibot testing example
    from kivy.app import App
    from kivy.lang import Builder
    kv = """
BoxLayout:
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
            return Builder.load_string(kv)

    app = TestApp()  # Do not run the app!
    run_kibot_tests(app)  # This  runs the app and calls unittest.main()
