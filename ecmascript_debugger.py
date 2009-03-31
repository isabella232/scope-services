# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

runtime_selection = Message("RuntimeSelection",
                            fields=[Field(Proto.Uint32, "runtimeList",  1, q=Quantifier.Repeated)
                                   ,Field(Proto.Bool,   "allRuntimes",  2, q=Quantifier.Optional)
                                   ])

runtime_info = Message("RuntimeInfo",
                      fields=[Field(Proto.Uint32, "runtimeID",     1)
                             ,Field(Proto.String, "htmlFramePath", 2)
                             ,Field(Proto.Uint32, "windowID",      3)
                             ,Field(Proto.Uint32, "objectID",      4)
                             ,Field(Proto.String, "uri",           5)
                             ])

runtime_id = Message("RuntimeID",
                      fields=[Field(Proto.Uint32, "runtimeID",     1)
                             ])

runtime_list = Message("RuntimeList",
                      fields=[Field(Proto.Message, "runtimeList", 1, q=Quantifier.Repeated, message=runtime_info)
                             ])

script_info = Message("ScriptInfo",
                      fields=[Field(Proto.Uint32, "runtimeID",  1)
                             ,Field(Proto.Uint32, "scriptID",   2)
                             ,Field(Proto.String, "scriptType", 3)
                             ,Field(Proto.String, "scriptData", 4)
                             ,Field(Proto.String, "uri",        5, q=Quantifier.Optional, comment="present if `scriptType` is Linked")
                             ])

thread_info = Message("ThreadInfo",
                      fields=[Field(Proto.Uint32, "runtimeID",      1)
                             ,Field(Proto.Uint32, "threadID",       2)
                             ,Field(Proto.Uint32, "parentThreadID", 3)
                             ,Field(Proto.String, "threadType",     4)
                             ,Field(Proto.String, "eventNamespace", 5, q=Quantifier.Optional, comment="present if `threadType` is Event")
                             ,Field(Proto.String, "eventType",      6, q=Quantifier.Optional, comment="present if `threadType` is Event")
                             ])

thread_stopinfo = Message("ThreadStopInfo",
                      fields=[Field(Proto.Uint32, "runtimeID",     1)
                             ,Field(Proto.Uint32, "threadID",      2)
                             ,Field(Proto.Uint32, "scriptID",      3)
                             ,Field(Proto.Uint32, "lineNumber",    4)
                             ,Field(Proto.String, "stoppedReason", 5)
                             ,Field(Proto.Uint32, "breakpointID",  6, q=Quantifier.Optional)
                             ])

thread_result = Message("ThreadResult",
                      fields=[Field(Proto.Uint32, "runtimeID", 1)
                             ,Field(Proto.Uint32, "threadID",  2)
                             ,Field(Proto.String, "status",    3)
                             ])

dom_event = Message("DomEvent",
                    fields=[Field(Proto.Uint32, "objectID",  1)
                           ,Field(Proto.Uint32, "handlerID", 2)
                           ,Field(Proto.String, "eventType", 3)
                           ])

object_selection = Message("ObjectSelection",
                    fields=[Field(Proto.Uint32, "objectID",  1)
                           ,Field(Proto.Uint32, "windowID",  2)
                           ,Field(Proto.Uint32, "runtimeID", 3, q=Quantifier.Optional)
                           ])

thread_mode = Message("ThreadMode",
                      fields=[Field(Proto.Uint32, "runtimeID", 1)
                             ,Field(Proto.Uint32, "threadID",  2)
                             ,Field(Proto.String, "mode",      3)
                             ])

object_value = Message("ObjectValue",
                      fields=[Field(Proto.Uint32,  "objectID",    1)
                             ,Field(Proto.Bool,    "isCallable",  2)
                             ,Field(Proto.Bool,    "isFunction",  3)
                             ,Field(Proto.String,  "type",        4, comment="type, function or object") # TODO Make it an enum
                             ,Field(Proto.Uint32,  "prototypeID", 5, q=Quantifier.Optional)
                             ,Field(Proto.String,  "name",        6, q=Quantifier.Optional, comment="Name of class (object) or function")
                             ])

eval_property = Message("Property", is_global=False,
                        fields=[Field(Proto.String, "name",      1)
                               ,Field(Proto.String, "type",      2) # TODO Make an enum, "number", "boolean", "string", "null", "undefined", "object-id"
                               ,Field(Proto.String, "value",     3, q=Quantifier.Optional, comment="Only present for `Number`, `String` or `Boolean`")
                               ,Field(Proto.Uint32, "objectID",  4, q=Quantifier.Optional, comment="Only present for `Object`")
                               ])

eval_data = Message("EvalData",
                    fields=[Field(Proto.Uint32,  "runtimeID",  1)
                           ,Field(Proto.Uint32,  "threadID",   2)
                           ,Field(Proto.Uint32,  "frameID",    3)
                           ,Field(Proto.String,  "scriptData", 4)
                           ,Field(Proto.Message, "properties", 5, q=Quantifier.Repeated, message=eval_property)
                           ])

eval_result = Message("EvalResult",
                      fields=[Field(Proto.String,  "status",       1)
                             ,Field(Proto.String,  "type",         2) # TODO Make an enum, "number", "boolean", "string", "null", "undefined", "object-id"
                             ,Field(Proto.String,  "value",        3, q=Quantifier.Optional, comment="Only present for `Number`, `String` or `Boolean`")
                             ,Field(Proto.Message, "objectValue",  4, q=Quantifier.Optional, message=object_value, comment="Only present for `Object`")
                             ])

examine_list = Message("ExamineList",
                       fields=[Field(Proto.Uint32, "runtimeID",  1)
                              ,Field(Proto.Uint32, "objectList", 2, q=Quantifier.Repeated)
                              ])

frame_selection = Message("FrameSelection",
                          fields=[Field(Proto.Uint32, "runtimeID", 1)
                                 ,Field(Proto.Uint32, "threadID",  2)
                                 ,Field(Proto.Uint32, "frameID",   3)
                                 ])

property_data = Message("Property", is_global=False,
                        fields=[Field(Proto.String,  "name",         1)
                               ,Field(Proto.String,  "type",         2) # TODO Make an enum, "number", "boolean", "string", "null", "undefined", "object-id"
                               ,Field(Proto.String,  "value",        3, q=Quantifier.Optional, comment="Only present for `Number`, `String` or `Boolean`")
                               ,Field(Proto.Message, "objectValue",  4, q=Quantifier.Optional, message=object_value, comment="Only present for `Object`")
                               ])

object_data = Message("ObjectInfo",
                      fields=[Field(Proto.Message, "value",       1, message=object_value)
                             ,Field(Proto.Message, "properties",  2, q=Quantifier.Repeated, message=property_data)
                             ])

object_info = Message("ObjectList",
                      fields=[Field(Proto.Message, "objects", 1, q=Quantifier.Repeated, message=object_data)
                             ])

spotlight_box = Message("SpotlightBox", is_global=False, doc="Color is encoded as RGBA with 8 bits for each channel.",
                        fields=[Field(Proto.Uint32, "boxType",    1, doc="Valid values:\n  0: dimension\n  1: padding\n  2: border\n  3: margin")
                               ,Field(Proto.Uint32, "fillColor",  2, q=Quantifier.Optional)
                               ,Field(Proto.Uint32, "frameColor", 3, q=Quantifier.Optional, doc="Drawn with 1px width inside the box")
                               ,Field(Proto.Uint32, "gridColor",  4, q=Quantifier.Optional, doc="Drawn with 1px width inside the box over the whole document")
                               ]) 

spotlight_object = Message("SpotlightObject", doc="The drawing order is box, reference-box-frame, box-frame, grid.",
                              fields=[Field(Proto.Uint32,  "objectID",       1)
                                     ,Field(Proto.Bool,    "scrollIntoView", 2, doc="Chooses whether the given object should be scrolled into view or not.")
                                     ,Field(Proto.Message, "boxes",          3, q=Quantifier.Repeated, message=spotlight_box)
                                     ]) 

spotlight_selection = Message("SpotlightSelection",
                              fields=[Field(Proto.Message, "spotlightObjects", 1, q=Quantifier.Repeated, message=spotlight_object)
                                     ]) 

spotlight_object_selection = Message("SpotlightObjectSelection",
                                     fields=[Field(Proto.Uint32, "objectID",       1)
                                            ,Field(Proto.Bool,   "scrollIntoView", 2, doc="Chooses whether the given object should be scrolled into view or not.")
                                            ]) 

breakpoint_pos = Message("BreakpointPosition", # TODO: Perhaps it is better to create one Command per break-type?
                         fields=[Field(Proto.Uint32, "breakpointID", 1)
                                ,Field(Proto.String, "type",         2) # TODO: enum, "line", "function", "event"

                                ,Field(Proto.Uint32, "scriptID",     3, q=Quantifier.Optional, comment="Present when `Type` is `Line`")
                                ,Field(Proto.Uint32, "lineNumber",   4, q=Quantifier.Optional, comment="Present when `Type` is `Line`")

                                ,Field(Proto.String, "eventType",    5, q=Quantifier.Optional, comment="Present when `Type` is `Event`")
                                ]) 

breakpoint_id = Message("BreakpointID",
                        fields=[Field(Proto.Uint32, "breakpointID", 1)
                               ]) 

event_handler = Message("EventHandler",
                        fields=[Field(Proto.Uint32,  "handlerID",       1, comment="`handlerID` is set by the client and is referred to by both client and host.")
                               ,Field(Proto.Uint32,  "objectID",        2)
                               ,Field(Proto.String,  "namespace",       3, comment="Namespace of the event. If empty, it will match any namespace.")
                               ,Field(Proto.String,  "eventType",       4)
                               ,Field(Proto.Bool,    "preventDefaultHandler", 5, comment="Prevents the default event handler from running.")
                               ,Field(Proto.Bool,    "stopPropagation",       6, comment="Stops propagation of the event beyond this `objectID` (it will however run for all handlers on the object).")
                               ],
                        comment="Add an event handler. This will generate a HANDLE-EVENT event every time the XML event defined by the pair (NAMESPACE, EVENT-TYPE) reaches the object defined by OBJECT-ID in the capturing phase. XML events are defined in http://www.w3.org/TR/xml-events")
event_handler_id = Message("EventHandlerID",
                           fields=[Field(Proto.Uint32,  "handlerID", 1, comment="`handlerID` as specified in EventHandler.handlerID.")
                                  ])

configuration  = Message("Configuration",
                         fields=[Field(Proto.Bool, "stopAtScript",    1, q=Quantifier.Optional)
                                ,Field(Proto.Bool, "stopAtException", 2, q=Quantifier.Optional)
                                ,Field(Proto.Bool, "stopAtError",     3, q=Quantifier.Optional)
                                ,Field(Proto.Bool, "stopAtAbort",     4, q=Quantifier.Optional)
                                ,Field(Proto.Bool, "stopAtGc",        5, q=Quantifier.Optional)
                                ,Field(Proto.Bool, "stopAtDebuggerStatement", 6, q=Quantifier.Optional)
                                ])

backtrace_selection = Message("BacktraceSelection",
                              fields=[Field(Proto.Uint32, "runtimeID", 1)
                                     ,Field(Proto.Uint32, "threadID",  2)
                                     ,Field(Proto.Uint32, "maxFrames", 3, q=Quantifier.Optional, default=0, comment="If `maxFrames` is omitted, all frames are returned")
                                     ])

break_selection = Message("BreakSelection",
                          fields=[Field(Proto.Uint32, "runtimeID", 1)
                                 ,Field(Proto.Uint32, "threadID",  2)
                                 ])

backtrace_frame = Message("BacktraceFrame",
                           fields=[Field(Proto.Uint32,  "functionID",     1)
                                  ,Field(Proto.Uint32,  "argumentObject", 2)
                                  ,Field(Proto.Uint32,  "variableObject", 3)
                                  ,Field(Proto.Uint32,  "thisObject",     4)
                                  ,Field(Proto.Message, "objectValue",    5, q=Quantifier.Optional, message=object_value) # TODO: Spec says repeated, while the code only assumes one (optional)
                                  ,Field(Proto.Uint32,  "scriptID",       6, q=Quantifier.Optional)
                                  ,Field(Proto.Uint32,  "lineNumber",     7, q=Quantifier.Optional)
                                  ])

backtrace_frames = Message("BacktraceFrameList",
                           fields=[Field(Proto.Message, "frames", 1, q=Quantifier.Repeated, message=backtrace_frame)
                                  ])

dom_traversal = Message("DomTraversal", 
                        fields=[Field(Proto.Uint32,  "objectID",  1)
                               ,Field(Proto.String,  "traversal", 2, doc = """\
traversal on off:  
- parent-node-chain-with-children
    take the parent node chain for the target node.
    add for each node in that chain all children, 
    and for all children there first child,
    if that is a text node and the only node, 
    starting with the document node.
- children
    get node data for all children in their flow
- node
    get node data for that node
- subtree
    get node data for the subtree in the flow of it""") # TODO: Enum, "subtree", "node", "children", "parent-node-chain-with-children"
                               ])

attribute = Message("Attribute", is_global=False,
                    fields=[Field(Proto.String,  "namePrefix", 1)
                           ,Field(Proto.String,  "name",       2)
                           ,Field(Proto.String,  "value",      3)
#                           ,Field(Proto.Message, "attributes", 4, q=Quantifier.Repeated)
                           ])
#attribute.fields[3].message = attribute

node_info = Message("NodeInfo",
                    fields=[Field(Proto.Uint32,  "objectID", 1)
                           ,Field(Proto.Uint32,  "type",     2)
                           ,Field(Proto.String,  "name",     3)
                           ,Field(Proto.Uint32,  "depth",    4)

                           # If `type` is 1
                           ,Field(Proto.String,  "namespacePrefix", 5, q=Quantifier.Optional)
                           ,Field(Proto.Message, "attributes",      6, q=Quantifier.Repeated, message=attribute)
                           ,Field(Proto.Uint32,  "childrenLength",  7, q=Quantifier.Optional)

                           # If `type` is 3, 4, 7 or 8
                           ,Field(Proto.String,  "value",    8, q=Quantifier.Optional)

                           # If `type` is 10
                           ,Field(Proto.String,  "publicID", 9,  q=Quantifier.Optional)
                           ,Field(Proto.String,  "systemID", 10, q=Quantifier.Optional)
                           ])

node_list = Message("NodeList",
                    fields=[Field(Proto.Message,  "nodes", 1, q=Quantifier.Repeated, message=node_info)
                           ])

css_index_map = Message("CssIndexMap",
                    fields=[Field(Proto.String,  "property", 1, q=Quantifier.Repeated)
                           ])

css_stylesheet = Message("Stylesheet", is_global=False,
                         fields=[Field(Proto.Uint32,  "objectID",    1)
                                ,Field(Proto.Bool,    "isDisabled",  2) # TODO: Should it be isEnabled?
                                ,Field(Proto.String,  "href",        3)
                                ,Field(Proto.String,  "title",       4)
                                ,Field(Proto.String,  "type",        5)
                                ,Field(Proto.String,  "media",       6, q=Quantifier.Repeated)
                                ,Field(Proto.Uint32,  "ownerNodeID", 7, q=Quantifier.Optional)
                                ,Field(Proto.Uint32,  "ownerRuleID", 8, q=Quantifier.Optional)
                                ,Field(Proto.Uint32,  "parentStylesheetID", 9, q=Quantifier.Optional)
                                ])

css_stylesheet_list = Message("CssStylesheetList",
                              fields=[Field(Proto.Message,  "stylesheets", 1, q=Quantifier.Repeated, message=css_stylesheet)
                                     ])

css_stylesheet_selection = Message("CssStylesheetSelection",
                                   fields=[Field(Proto.Uint32,  "runtimeID",     1)
                                          ,Field(Proto.Uint32,  "stylesheetID",  2)
                                          ])

css_stylesheet_rule = Message("StylesheetRule", is_global=False, update=False,
                              fields=[Field(Proto.Uint32,  "type",                1) 
# Type values:
# 0 - UNKNOWN
# 1 - STYLE
# 2 - CHARSET
# 3 - IMPORT
# 4 - MEDIA
# 5 - FONT_FACE
# 6 - PAGE
# 7 - NAMESPACE // Not supported
                                     ,Field(Proto.Uint32,  "stylesheetID",        2)
                                     ,Field(Proto.Uint32,  "ruleID",              3)

                                     # Common to FONT_FACE, PAGE and STYLE
                                     ,Field(Proto.Uint32,  "indexes",             4, q=Quantifier.Repeated)
                                     ,Field(Proto.String,  "values",              5, q=Quantifier.Repeated)
                                     ,Field(Proto.Bool,    "priorities",          6, q=Quantifier.Repeated)

                                     # Common to STYLE and PAGE
                                     ,Field(Proto.String,  "selectors",           7, q=Quantifier.Repeated, comment="0..1 for PAGE and 0..* for STYLE")
                                     ,Field(Proto.Uint32,  "specificities",       8, q=Quantifier.Repeated, comment="1..1 for PAGE and 0..* for STYLE")

                                     # Common to MEDIA and IMPORT
                                     ,Field(Proto.String,  "media",               9, q=Quantifier.Repeated)

                                     # For MEDIA
                                     ,Field(Proto.Message, "rules",              10, q=Quantifier.Repeated)

                                     # For IMPORT
                                     ,Field(Proto.String,  "href",               11, q=Quantifier.Optional)
                                     ,Field(Proto.Uint32,  "importStylesheetID", 12, q=Quantifier.Optional)

                                     # For PAGE
                                     ,Field(Proto.Uint32,  "pseudoClass",        13, q=Quantifier.Optional)

                                     # For CHARSET
                                     ,Field(Proto.String,  "charset",            14, q=Quantifier.Optional)
                                     ])
# Must be set separately due to recursion
css_stylesheet_rule["rules"].message = css_stylesheet_rule
css_stylesheet_rule.updateCount({})

css_stylesheet_rules = Message("CssStylesheetRules",
                               fields=[Field(Proto.Message, "rules",  1, q=Quantifier.Repeated, message=css_stylesheet_rule)
                                      ])

css_element_selection = Message("CssElementSelection",
                                fields=[Field(Proto.Uint32,  "runtimeID",  1)
                                       ,Field(Proto.Uint32,  "objectID",   2)
                                       ])

css_style_decl = Message("StyleDeclaration", is_global=False,
                         fields=[Field(Proto.Uint32,  "origin",        1) # 1 = USER-AGENT, 2=LOCAL, 3=AUTHOR, 4=ELEMENT

                                # Common to all origins
                                ,Field(Proto.Uint32,  "indexes",       2, q=Quantifier.Repeated)
                                ,Field(Proto.String,  "values",        3, q=Quantifier.Repeated)
                                ,Field(Proto.Bool,    "priorities",    4, q=Quantifier.Repeated)
                                ,Field(Proto.Uint32,  "statuses",      5, q=Quantifier.Repeated) # 0 = overwritten, 1 = standard

                                # Common to AUTHOR and LOCAL
                                ,Field(Proto.String,  "selector",      6, q=Quantifier.Optional)
                                ,Field(Proto.Uint32,  "specificity",   7, q=Quantifier.Optional)

                                # For AUTHOR
                                ,Field(Proto.Uint32,  "stylesheetID",  8, q=Quantifier.Optional)
                                ,Field(Proto.Uint32,  "ruleID",        9, q=Quantifier.Optional)
                                ,Field(Proto.Uint32,  "ruleType",     10, q=Quantifier.Optional)
                                ])

css_node_style = Message("NodeStyle", is_global=False,
                         fields=[Field(Proto.Uint32,  "objectID",     1) 
                                ,Field(Proto.String,  "elementName",  2)
                                ,Field(Proto.Message, "styles",       3, q=Quantifier.Repeated, message=css_style_decl)
                                ])

css_node_decls = Message("CssStyleDeclarations",
                         fields=[Field(Proto.String,  "computedStyles",  1, q=Quantifier.Repeated)
                                ,Field(Proto.Message, "nodeStyles",      2, q=Quantifier.Repeated, message=css_node_style)
                                ])

es_debugger = Service("EcmascriptDebugger", version="5.0", coreRelease="2.4",
                      commands=[Request(1,  "ListRuntimes",        runtime_selection,   runtime_list)
                               ,Request(2,  "ContinueThread",      thread_mode,         False)
                               ,Request(3,  "Eval",                eval_data,           eval_result, async=True)
                               ,Request(4,  "ExamineObjects",      examine_list,        object_info)
                               ,Request(5,  "SpotlightObject",     spotlight_object_selection, False)
                               ,Request(27, "SpotlightObjects",    spotlight_selection, False)
                               ,Request(6,  "AddBreakpoint",       breakpoint_pos,      False)
                               ,Request(7,  "RemoveBreakpoint",    breakpoint_id,       False)
                               ,Request(8,  "AddEventHandler",     event_handler,       False)
                               ,Request(9,  "RemoveEventHandler",  event_handler_id,    False)
                               ,Request(10, "SetConfiguration",    configuration,       False)
                               ,Request(11, "GetBacktrace",        backtrace_selection, backtrace_frames)
                               ,Request(12, "Break",               break_selection,     False)
                               ,Request(13, "InspectDom",          dom_traversal,       node_list)
#                               ,Request(7,  "ExamineFrame",        frame_selection,     object_info)
# TODO ExamineFrame does not seem to exists, remove it
                               ,Event(14, "OnRuntimeStarted",  runtime_info)
                               ,Event(15, "OnRuntimeStopped",  runtime_id)
                               ,Event(16, "OnNewScript",       script_info)
                               ,Event(17, "OnThreadStarted",   thread_info)
                               ,Event(18, "OnThreadFinished",  thread_result)
                               ,Event(19, "OnThreadStoppedAt", thread_stopinfo)
                               ,Event(20, "OnHandleEvent",     dom_event)
                               ,Event(21, "OnObjectSelected",  object_selection)

                               # CSS inspector, should be moved to separate service
                               ,Request(22, "CssGetIndexMap",          False,                    css_index_map)
                               ,Request(23, "CssGetAllStylesheets",    runtime_id,               css_stylesheet_list)
                               ,Request(24, "CssGetStylesheet",        css_stylesheet_selection, css_stylesheet_rules)
                               ,Request(25, "CssGetStyleDeclarations", css_element_selection,    css_node_decls)

                               ,Request(26, "GetSelectedObject",       False,                    object_selection)
                               ],
                      cpp_class="ES_ScopeDebugFrontend", cpp_hfile="modules/scope/src/scope_ecmascript_debugger.h")
