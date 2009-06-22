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

# Core 2.2 examples
window_list_c22 = """<list-windows-reply>
  <window-info>
    <window-id>5</window-id>
    <title>node</title>
    <window-type>body</window-type>
    <opener-id>7</opener-id>
  </window-info>
</list-windows-reply>
"""

filter_c22 = """<filter>
  <clear>1</clear>
  <include>
    <window-id>7</window-id>
  </include-id>
  <include>
    <string>html</string>
  </include-pattern>
  <include>
    <string>dom</string>
  </include-pattern>
  <include>
    <string>node</string>
  </include-pattern>
  <exclude>
    <string>body</string>
  </exclude-pattern>
</filter>
"""
updated_window_c22="""<updated-window>
  <window-id>7</window-id>
  <title>html</title>
  <window-type>dom</window-type>
  <opener-id>10</opener-id>
</updated-window>
"""
window_closed_c22="""<window-closed>
  <window-id>1</window-id>
</window-closed>
"""

window_manager = Service("WindowManager", version="2.0", coreRelease="2.4",
                         commands=[Request(1, "GetActiveWindow", False,         window_id)
                                  ,Request(3, "ListWindows",     False,         window_list) # core_2_2=window_list_c22
                                  ,Request(5, "ModifyFilter",    window_filter, False)
                                  ,Event(0, "OnWindowUpdated",   window_info)
                                  ,Event(2, "OnWindowClosed",    window_id)
                                  ,Event(4, "OnWindowActivated", window_id)
                                  ],
                         cpp_class="OpScopeWindowManager", cpp_hfile="modules/scope/src/scope_window_manager.h")
