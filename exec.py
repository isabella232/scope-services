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

screenwatcher_data = Message("ScreenWatcher",
                             fields=[Field(Proto.Uint32, "timeOut",  1),
                                     Field(Proto.Message, "area",    2, message = area),
                                     Field(Proto.String, "md5List",  3, q=Quantifier.Repeated),
                                     Field(Proto.Uint32, "windowID", 4, q=Quantifier.Optional)])

screenwatcher_event = Message("ScreenWatcherEvent",
                              fields=[Field(Proto.Uint32, "windowID", 1),
                                      Field(Proto.String, "md5", 2, q=Quantifier.Optional),
                                      Field(Proto.Bytes, "png", 3, q=Quantifier.Optional)])

exec_service = Service("Exec", version="2.0", coreRelease="2.4",
                       doc="""The Opera Exec protocol can be used to control an Opera instance from\nthe outside, and various operations can be initiated. This\nfunctionality is mainly useful for QA testing.""",
                       commands=[Request(1, "Exec", exec_data, False),
                                 Request(2, "GetActionInfoList", False, get_action_list),
                                 Request(3, "SetupScreenWatcher", screenwatcher_data, False),
                                 Event(4, "OnScreenWatcherEvent", screenwatcher_event)
                                ],
                       cpp_class="OpScopeExec", cpp_hfile="modules/scope/src/scope_exec.h")
