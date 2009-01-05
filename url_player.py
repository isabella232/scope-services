# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

# Service: UrlPlayer
# TODO: This service should probable be replaced with the Exec service.

urlplayer_window_data = Message("WindowData",
                                fields=[Field(Proto.Uint32, "windowCount", 1)
                                       ])

urlplayer_window_result = Message("WindowResult",
                                 fields=[Field(Proto.Uint32, "windowCount", 1)
                                       ])

urlplayer_play = Message("UrlSelection",
                         fields=[Field(Proto.Uint32, "windowNumber", 1)
                                ,Field(Proto.String, "url",          2)
                                ])

url_player = Service("UrlPlayer", version="2.0", coreRelease="2.4",
                     commands=[Request(1,  "CreateWindows", urlplayer_window_data, urlplayer_window_result)
                              ,Request(3,  "LoadUrl",       urlplayer_play,        False)
                              ],
                     cpp_class="OpScopeUrlPlayer", cpp_hfile="modules/scope/src/urlplayer_command.h")
