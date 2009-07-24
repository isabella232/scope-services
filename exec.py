# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

# Service: Exec

actiondoc = """The name of the action to execute. 
This is either a regular Opera action (e.g. "Page Down"),
or a special exec-action. Both kinds can be found by 
calling `GetActionInfoList`. The special cases are
prefixed with underscore ("_"), and these require `value` 
parameter to work, but always ignores `windowID`.

The special cases may include:
    _keydown | _keyup: 
        The `value` is either a key-name ("ctrl", "down", etc.)
        or a single character ("a", "b", etc.)
    _type: 
        Types the text present in `value` 
        (a different approach is the "Insert" action)

It is currently not possible to figure out which actions 
take parameters (`value`), and which don't. Optimistically, 
we have made the `Action` type extendable to include 
such information later."""

exec_data = Message("ActionList",
                    fields=[Field(Proto.Message, "actionList", 1, q=Quantifier.Repeated,
                                  message=Message("Action", is_global=False,
                                                  doc="""Executes a series of actions in the opera host,\neach action consists of a name identifying the\naction and optionally a value for the action.\nThe value depends on the type of action.""",
                                                  fields=[Field(Proto.String, "name",  1, doc=actiondoc)
                                                         ,Field(Proto.String, "value", 2, Quantifier.Optional)
                                                         ,Field(Proto.Uint32, "windowID", 3, Quantifier.Optional)
                                                         ]))
                           ])

get_action_list = Message("ActionInfoList", doc="List all valid `Action` `name`s",
        fields=[Field(Proto.Message, "actionInfoList", 1, q=Quantifier.Repeated,
                      message=Message("ActionInfo", is_global=False,
                                      doc="""Name of an action, to be used in the `Action` message.""",
                                      fields=[Field(Proto.String, "name", 1),
                                             ]
                                     ))])

area = Message("Area",
               fields=[Field(Proto.Int32, "x", 1),
                       Field(Proto.Int32, "y", 2),
                       Field(Proto.Int32, "w", 3),
                       Field(Proto.Int32, "h", 4)])

color_spec_doc="""Specifies a new color specification.
The `id` is used when reporting back the results.
You can have overlapping color specifications.
Note: There can be a maximum of 16 color specifications!

Color values ranges from 0 (no color) to 255 (maximal saturation), other values are not allowed.
Default (meaning field missing) is 0 for *Low elements and 255 for *High fields.
"""

color_spec = Message("ColorSpec", doc=color_spec_doc, is_global=False,
                     fields=[Field(Proto.Uint32, "id", 1),
                             Field(Proto.Uint32, "redLow",    2, q=Quantifier.Optional),
                             Field(Proto.Uint32, "redHigh",   3, q=Quantifier.Optional),
                             Field(Proto.Uint32, "greenLow",  4, q=Quantifier.Optional),
                             Field(Proto.Uint32, "greenHigh", 5, q=Quantifier.Optional),
                             Field(Proto.Uint32, "blueLow",   6, q=Quantifier.Optional),
                             Field(Proto.Uint32, "blueHigh",  7, q=Quantifier.Optional),
                             ])

screenwatcher_data = Message("ScreenWatcher",
                             fields=[Field(Proto.Uint32,  "timeOut",       1, doc="Number of milliseconds to wait before capturing the screen area."),
                                     Field(Proto.Message, "area",          2, message = area),
                                     Field(Proto.String,  "md5List",       3, q=Quantifier.Repeated),
                                     Field(Proto.Uint32,  "windowID",      4, q=Quantifier.Optional, doc="The ID of the window to watch, the default (or 0) is to watch the current window"),
                                     Field(Proto.Message, "colorSpecList", 5, q=Quantifier.Repeated, message=color_spec),
                                     ])

color_match = Message("ColorMatch", is_global=False,
                      fields=[Field(Proto.Uint32, "id",    1, doc="The `ColorSpec.id` which matched a color"),
                              Field(Proto.Uint32, "count", 2),
                              ])

screenwatcher_result = Message("ScreenWatcherResult",
                              fields=[Field(Proto.Uint32,  "windowID",       1, doc="The ID of the window that was triggered by a screen watch, or 0 if the screen watch failed or was cancelled"),
                                      Field(Proto.String,  "md5",            2),
                                      Field(Proto.Bytes,   "png",            3, q=Quantifier.Optional),
                                      Field(Proto.Message, "colorMatchList", 4, q=Quantifier.Repeated, message=color_match),
                                      ])

mouse_action = Message("MouseAction",
                       fields=[Field(Proto.Uint32, "windowID", 1),
                               Field(Proto.Int32,  "x", 2),
                               Field(Proto.Int32,  "y", 3),
                               Field(Proto.Uint32, "buttonAction", 4,
                                     doc="""`buttonAction` specifies the buttons to press or release
It is specifies as the sum of button actions:
      1 - Button 1 down
      2 - Button 1 up

      4 - Button 2 down
      8 - Button 2 up

     16 - Button 3 down
     32 - Button 3 up

For example, to press button 1 and release button 2, the value is 9 (1+8)

Buttons are clicked in the sequence listed above. Note that down actions are
listed before up actions, thus allowing single-clicking with one command
(e.g. using value 3)"""),
                               ])

mouse_doc="""Move mouse to the given position on the screen/window.
Note that the mouse cursor is not moved visibly.

The coordinates are relative to the upper left corner of the tab
(not including chrome)."""

exec_service = Service("Exec", version="2.0", coreRelease="2.4",
                       doc="""The Opera Exec protocol can be used to control an Opera instance from\nthe outside, and various operations can be initiated. This\nfunctionality is mainly useful for QA testing.""",
                       commands=[Request(1, "Exec", exec_data, False),
                                 Request(2, "GetActionInfoList", False, get_action_list),
                                 Request(3, "SetupScreenWatcher", screenwatcher_data, screenwatcher_result, async=True),
#                                 Event(4,   "OnScreenWatcherEvent", screenwatcher_event),
                                 Request(5, "SendMouseAction", mouse_action, False, doc=mouse_doc),
                                ],
                       cpp_class="OpScopeExec", cpp_hfile="modules/scope/src/scope_exec.h")
