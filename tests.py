import unittest
from unittest import TestCase
from kibot import KibotTestCase, run_kibot_tests, WidgetNotFoundError
from kivy.factory import Factory


class TestKibot(KibotTestCase):
    """Kibot testing"""

    def test_find(self):
        widget = self.kibot.find(text="Kibot Test")
        self.assertEqual(widget, self.app.root.my_button)

    def test_find_by_class(self):
        widget = self.kibot.find(class_="Button")
        self.assertEqual(widget, self.app.root.my_button)

    def test_find_by_id(self):
        widget = self.kibot.find(id="_my_button")
        self.assertEqual(widget, self.app.root.my_button)

    def test_do(self):
        from functools import partial
        x = []

        def test(x):
            x.append(1)
        self.kibot.do(partial(test, x))
        self.kibot.wait_until()
        self.assertEqual(x[0], 1)

    def test_wait(self):
        import time
        k = time.time()
        self.kibot.wait(2)
        self.kibot.do(lambda dt: dt)
        self.kibot.wait_until()
        self.assertGreaterEqual(time.time() - k, 2)

    def test_do_press(self):
        self.kibot.do_press(widget=self.app.root.slider, x=0.5, y=0.5)
        self.kibot.wait_until()
        self.assertEqual(self.app.root.slider.value, 50)

    def test_do_release(self):
        self.kibot.do_release()

    def test_do_click(self):
        self.kibot.do_press(widget=self.app.root.my_button)
        self.kibot.wait_until()
        self.assertEqual(self.app.root.my_button.text, "Pressed!")

    def test_do_move(self):
        widget = self.app.root.slider
        self.kibot.do_press(widget=widget, x=0.0, y=0.5)
        self.kibot.do_move(widget=widget, x=0.5, y=0.5)
        self.kibot.do_release(widget=widget, x=0.5, y=0.5)
        self.kibot.wait_until()
        self.assertEqual(widget.value, 50)

    def test_do_keystroke(self):
        widget = self.app.root.textinput
        self.kibot.do_click(widget=widget)
        self.kibot.do_keystroke('h')
        self.kibot.do_keystroke(text='ello world')
        self.kibot.wait_until()
        self.assertEqual("hello world", widget.text)

    def test_record(self):
        self.kibot.record('delete.kibot')
        self.kibot.do_press(x=0, y=100)
        self.kibot.wait_until()
        self.assertEqual("do_press" in str(self.kibot.recorded_commands), True)

    def test_execute_record(self):
        widget = self.app.root.my_button
        try:
            with open("delete.kibot", 'w') as f:
                f.write("self.do_press(x=100, y=100)")
            self.kibot.execute_record("delete.kibot")
            self.kibot.wait_until()
        except Exception as e:
            raise e
        finally:
            import os
            os.remove("delete.kibot")
        self.assertEqual(widget.text, "Pressed!")

if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder
    kv = """
<RootWidget@BoxLayout>:
    orientation: 'vertical'
    my_button: _my_button
    slider: _slider
    textinput: _tinput
    lbl: _lbl

    BoxLayout:
        Button:
            id: _my_button
            text: "Kibot Test"
            on_press: self.text="Pressed!"
        TextInput:
            id: _tinput
    Slider:
        id: _slider
        step: 1
        on_value: _lbl.text="%s"%(self.value)
    Label:
        id: _lbl
        size_hint_y: 0.1
"""

    class TestApp(App):

        def build(self):
            return Factory.RootWidget()

    Builder.load_string(kv)
    app = TestApp()
    run_kibot_tests(app)  # This  runs the app and calls unittest.main()
