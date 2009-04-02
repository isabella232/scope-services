# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

scope_message = Message("ScopeMessage",
                          fields=[Field(Proto.String, "message",    1)])

scope = Service(
    "Scope", 
    version="1.0", 
    coreRelease="2.4",
    commands=[
        Event(0,  "OnServices",  scope_message),
        Event(1,  "OnConnect",  scope_message),
        Event(2,  "COnQuit",  scope_message),
        Event(3,  "OnConnectionLost",  scope_message),
        Request(4,  "Enable",       scope_message,      scope_message),
        Request(5,  "Disable",       scope_message,      scope_message),
        Request(6,  "Configure",       scope_message,      scope_message),
        Request(7,  "Info",       scope_message,      scope_message),
        Request(8,  "Quit",       scope_message,      scope_message),                       
        ],
    cpp_class="", 
    cpp_hfile=""
    )
