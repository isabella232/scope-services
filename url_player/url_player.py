# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service, Options

# Service: UrlPlayer
# TODO: This service should probable be replaced with the Exec service.

window_count = Message("WindowCount",
                       fields=[Field(Proto.Uint32, "windowCount", 1)
                              ])

request = Message("Request",
                         fields=[Field(Proto.Uint32, "windowNumber", 1)
                                ,Field(Proto.String, "url",          2)
                                ])

window = Message("Window",
                 fields=[Field(Proto.Uint32, "windowID", 1)
                        ])

url_player = Service("UrlPlayer",
                     commands=[Request(1, "CreateWindows",      window_count, window_count)
                              ,Request(2, "LoadUrl",            request,      window)
                              ,Event(3,   "OnUrlLoaded",        window)
                              ,Event(4,   "OnConnectionFailed", window)
                              ],
                     options=Options(version="2.0", core_release="2.4",
                                     cpp_class="OpScopeUrlPlayer", cpp_hfile="modules/scope/src/urlplayer_command.h"))
