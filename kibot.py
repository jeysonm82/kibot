from kivy.input import MotionEventFactory
from kivy.input.providers.mouse import MouseMotionEventProvider
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.config import Config
from functools import partial
import time
from kivy.factory import Factory
import unittest
from threading import Thread


class FakeMouseEventProvider(MouseMotionEventProvider):

    """A fake Mouse Motion Event Provider """

    instance = None

    def start(self):
        print "FakeMouseProvider started"
        FakeMouseEventProvider.instance = self
        self.win = EventLoop.window

    def mouse_down(self, x, y, button='left', t=0):
        self.on_mouse_press(self.win, x, y, button, ())

    def mouse_up(self, x, y, button='left', t=0):
        self.on_mouse_release(self.win, x, y, button, ())

    def move(self, x, y, t=0):
        self.on_mouse_motion(self.win, x, y, ())


class Kibot(object):

    """Kibot intends to become a GUI test automation tool for kivy.
    Works in pc (windows, linux, mac?).
    """

    app = None
    time_cnt = 0
    num_events = 0

    def __init__(self, *args, **kwargs):
        self.app = args[0]
        self.time_cnt = 0

    def wait(self, t=0):
        """Waits specified time
        :param t: time in seconds
        """
        self.time_cnt += t

    def do_press(self, x=0, y=0, widget=None):
        """touch_down event
         :param widget: if widget is provided x and y are obtained from
        widget's position.
        """
        fmp = FakeMouseEventProvider.instance
        if widget is not None:
            x, y = widget.center_x, widget.center_y

        self.do(partial(fmp.mouse_down, x, y, 'left'))

    def do_release(self, x=0, y=0, widget=None):
        """touch_up event
         :param widget: if widget is provided x and y are obtained from
        widget's position.
        """
        fmp = FakeMouseEventProvider.instance
        if widget is not None:
            x, y = widget.center_x, widget.center_y

        self.do(partial(fmp.mouse_up, x, y, 'left'))

    def do_move(self, x=0, y=0, widget=None):
        """mouse move event"""
        fmp = FakeMouseEventProvider.instance
        self.do(partial(fmp.move, x, y))

    def do_click(self, x=0, y=0, t=0.2, widget=None):
        """press, wait and release event
        :param widget: if widget is provided x abd y are obtained from
        widget's position.
        :param t: time to wait between press and release
        """
        self.do_press(x, y, widget)
        self.wait(t)
        self.do_release(x, y, widget)

    def do(self, func):
        self.last = Clock.schedule_once(
            partial(self._event, func), self.time_cnt)
        self.time_cnt += 0.1
        self.num_events += 1

    def _event(self, func, t=0):
        func()
        self.num_events -= 1

    def wait_until(self):
        """Waits until all events have been executed in kivy EventLoop"""
        while self.num_events:  # Warning could result in infinite loop
            pass

    def find(self, root=None, **kwargs):
        """ Find first widget in widget tree with specified properties values
        Ex: find(class_='Button', text='Text')
        :param root: Root widget, if None App.root is used.
        :returns: found widget or None
        """

        attrs, values = zip(*kwargs.items())
        root = self.app.root if root is None else root
        b = True
        for wid in root.children:
            b = True
            for attr, value in kwargs.iteritems():
                if attr == 'class_':
                    if not isinstance(wid, getattr(Factory, value)):
                        b = False
                elif not hasattr(wid, attr):
                    b = False
                else:
                    val = getattr(wid, attr)
                    if val != value:
                        b = False
                if not b:
                    continue
            if b:
                return wid

        # Search inside children
        for wid in root.children:
            if len(wid.children):
                ret = self.find(wid, **kwargs)
                if ret is not None:
                    return ret
        return None  # TODO maybe Raise NotFoundException?

    def reset(self):
        self.time_cnt = 0


class KibotTestBase(unittest.TestCase):

    """ Base kibot testcase """
    app = None
    """App instance """


def _runtests(app):
    time.sleep(1)
    unittest.main()
    app.stop()  # TODO this is not working, line not reached.


def run_kibot_tests(app):
    """ Perform the tests by calling app.run in the main thread and
    unittest.main in a daemon. """

    tl = Thread(target=_runtests, args=(app,))
    tl.daemon = True
    tl.start()
    KibotTestBase.app = app
    app.run()

Config.set("input", "fakemouseprovider", "fakemouseprovider")
MotionEventFactory.register('fakemouseprovider', FakeMouseEventProvider)
