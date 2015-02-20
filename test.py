from kibot import Kibot, KibotTestBase, run_kibot_tests


class KibotTestExample(KibotTestBase):

    def test_button_text_equals_pressed(self):
        """Test that my_button has proper text after one click/touch """

        kibot = Kibot(self.app)
        my_button = kibot.find(tag="my_button")  # find button by tag property
        kibot.do_click(widget=my_button)  # click my button
        kibot.wait_until()  # wait until all events are executed

        self.assertEqual(my_button.text, "Pressed!")


if __name__ == '__main__':
    # A kibot testing example
    from kivy.app import App
    from kivy.lang import Builder
    kv = """
BoxLayout:
    BoxLayout:
        Button:
            tag: "my_button"
            text: "Kibot Test"
            on_press: self.text="Pressed!"
"""

    class TestApp(App):

        def build(self):
            return Builder.load_string(kv)

    app = TestApp()  # Do not run the app!
    run_kibot_tests(app)  # This  runs the app and calls unittest.main()
