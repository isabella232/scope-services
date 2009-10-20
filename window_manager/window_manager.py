# hob
from hob.proto import Proto, Quantifier, Field, Message, Request, Event, Service, Options

window_id = Message("WindowID",
                    fields=[Field(Proto.Uint32, "windowID", 1)
                               ])

window_info = Message("WindowInfo",
                      fields=[Field(Proto.Uint32, "windowID", 1)
                             ,Field(Proto.String, "title", 2)
                             ,Field(Proto.String, "windowType", 3)
                             ,Field(Proto.Uint32, "openerID", 4)
                             ])

window_list = Message("WindowList",
                      fields=[Field(Proto.Message, "windowList", 1, q=Quantifier.Repeated, message=window_info)
                             ])

window_filter = Message("WindowFilter",
                        fields=[Field(Proto.Bool,   "clearFilter",        1, default=False)
                               ,Field(Proto.Uint32, "includeIDList",      2, q=Quantifier.Repeated)
                               ,Field(Proto.String, "includePatternList", 3, q=Quantifier.Repeated)
                               ,Field(Proto.Uint32, "excludeIDList",      4, q=Quantifier.Repeated)
                               ,Field(Proto.String, "excludePatternList", 5, q=Quantifier.Repeated)
                               ])
                               
window_manager = Service("WindowManager",
                         commands=[Request(1, "GetActiveWindow", False,         window_id)
                                  ,Request(2, "ListWindows",     False,         window_list) # core_2_2=window_list_c22
                                  ,Request(3, "ModifyFilter",    window_filter, False)
                                  ,Event(4, "OnWindowUpdated",   window_info)
                                  ,Event(5, "OnWindowClosed",    window_id)
                                  ,Event(6, "OnWindowActivated", window_id)
                                  ,Event(7, "OnWindowLoaded", window_id)
                                  ],
                         options=Options(version="2.0", core_release="2.4",
                                         cpp_class="OpScopeWindowManager", cpp_hfile="modules/scope/src/scope_window_manager.h"))
