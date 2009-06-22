# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

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

window_manager = Service("WindowManager", version="2.0", coreRelease="2.4",
                         commands=[Request(1, "GetActiveWindow", False,         window_id)
                                  ,Request(3, "ListWindows",     False,         window_list) # core_2_2=window_list_c22
                                  ,Request(5, "ModifyFilter",    window_filter, False)
                                  ,Event(0, "OnWindowUpdated",   window_info)
                                  ,Event(2, "OnWindowClosed",    window_id)
                                  ,Event(4, "OnWindowActivated", window_id)
                                  ],
                         cpp_class="OpScopeWindowManager", cpp_hfile="modules/scope/src/scope_window_manager.h")
