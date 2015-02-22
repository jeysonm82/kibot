(pre-alpha stage)

Kibot
=====

Kibot is a basic GUI test automation tool for kivy. You can automate touch and keyboard events with it and use
it in your tests. (Tested in Linux and Windows 7).


**Current features:**
- Finding widgets filtering by property values.
- Clicking/pressing down a widget (using a mouse event provider)
- Sending keystrokes (using current keyboard)
- Creating testcases that can use kibot.
- Recording input events (touches, keyboard input) from a running app to be able to reproduce them later in a test.


Usage
=====

Check example_testing.py for a TestCase example and example_record.py for a recording example


Requirements
============
- Python 2.7.
- kivy 1.8. (It should work with kivy 1.9 as well).


More info
=========

**What doesn't work/is not implemented yet:**
- Double tap, triple tap. The touch provider is a mouseprovider than only sends left button events. Complex things like simulating rotations with two touches don't work.
- Keystrokes modifiers (Shift+, Ctrl+, etc.)

**What I plan to add/do in the near future:**
- Documentation. Lots of it.
- Improve input providers (touch and keyboard). They're already implemented in kivy.
- Running kibot in an android device.
- Some kind of BDD test specification to generate tests using natural language.

**What needs to be improved but I don't have an answer yet:**
- Improve Test maintainability. GUI tests are very sensitive to small changes in the code. For instance, if I record some touch events using Kibot.record any future change in the position and/or size of widgets could break the test.


License
=======

MIT license
