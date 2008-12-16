# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

runtime_selection = Message("RuntimeSelection",
                        fields=[Field(Proto.Uint32, "runtimeID",    1, q=Quantifier.Repeated)
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

thread_status = Message("ThreadStatus",
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
                    fields=[Field(Proto.Uint32, "objectID", 1)
                           ,Field(Proto.Uint32, "windowID", 2)
                           ])

thread_mode = Message("ThreadMode",
                      fields=[Field(Proto.Uint32, "runtimeID", 1)
                             ,Field(Proto.Uint32, "threadID",  2)
                             ,Field(Proto.String, "mode",      3)
                             ])

property_data = Message("Property",
                        fields=[Field(Proto.Uint32, "name",     1)
                               ,Field(Proto.String, "type",     2) # TODO Make an enum
                               ,Field(Proto.String, "value",    3, q=Quantifier.Optional, comment="Only present for `Object`, `Number`, `String` or `Boolean`")
                               ,Field(Proto.Uint32, "objectID", 4, q=Quantifier.Optional, comment="If you want to set a property on an object")
                               ])

eval_data = Message("EvalData",
                    fields=[Field(Proto.Uint32,  "runtimeID",  1)
                           ,Field(Proto.Uint32,  "threadID",   2)
                           ,Field(Proto.Uint32,  "frameID",    3)
                           ,Field(Proto.String,  "scriptData", 4)
                           ,Field(Proto.Message, "properties", 5, q=Quantifier.Repeated, message=property_data)
                           ])

eval_result = Message("EvalResult",
                      fields=[Field(Proto.String, "status",    2)
                             ,Field(Proto.String, "type",      3) # TODO Make an enum
                             ,Field(Proto.String, "value",     4, q=Quantifier.Optional, comment="Only present for `Object`, `Number`, `String` or `Boolean`")
                             ])

object_selection = Message("ObjectSelection",
                           fields=[Field(Proto.Uint32, "runtimeID", 1)
                                  ,Field(Proto.Uint32, "objectID",  2, q=Quantifier.Repeated)
                                  ])

frame_selection = Message("FrameSelection",
                          fields=[Field(Proto.Uint32, "runtimeID", 1)
                                 ,Field(Proto.Uint32, "threadID",  2)
                                 ,Field(Proto.Uint32, "frameID",   3)
                                 ])

object_data = Message("Object",
                      fields=[Field(Proto.Uint32,  "objectID",    1)
                             ,Field(Proto.Bool,    "isCallable",  2)
                             ,Field(Proto.Bool,    "isFunction",  3)
                             ,Field(Proto.String,  "type",        4, comment="type, function or object") # TODO Make it an enum
                             ,Field(Proto.Uint32,  "prototypeID", 5, q=Quantifier.Optional)
                             ,Field(Proto.String,  "name",        6, q=Quantifier.Optional, comment="Name of class (object) or function")
                             ,Field(Proto.Message, "properties",  7, q=Quantifier.Repeated, message=property_data)
                             ])

object_info = Message("ObjectInfo",
                      fields=[Field(Proto.Message, "objects", 1, q=Quantifier.Repeated, message=object_data)
                             ])

spotlight_selection = Message("SpotlightSelection",
                              fields=[Field(Proto.Uint32, "objectID",       1)
                                     ,Field(Proto.Bool,   "scrollIntoView", 2)
                                     ]) 

breakpoint_pos = Message("BreakpointPosition",
                         fields=[Field(Proto.Uint32, "breakpointID", 1)
                                ,Field(Proto.Uint32, "scriptID",     2)
                                ,Field(Proto.Uint32, "lineNumber",   3)
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
                                ])

backtrace_selection = Message("BacktraceSelection",
                              fields=[Field(Proto.Uint32, "runtimeID", 1)
                                     ,Field(Proto.Uint32, "threadID",  2)
                                     ,Field(Proto.Uint32, "maxFrames", 3, q=Quantifier.Optional, comment="If `maxFrames` is omitted, all frames are returned")
                                     ])

backtrace_frame = Message("BacktraceFrame",
                           fields=[Field(Proto.Uint32,  "functionID",     1)
                                  ,Field(Proto.Uint32,  "argumentObject", 2)
                                  ,Field(Proto.Uint32,  "varibleObject",  3)
                                  ,Field(Proto.Uint32,  "thisObject",     4)
                                  ,Field(Proto.Message, "objects",        5, q=Quantifier.Repeated, message=object_data)
                                  ,Field(Proto.Uint32,  "scriptID",       6, q=Quantifier.Optional)
                                  ,Field(Proto.Uint32,  "lineNumber",     7, q=Quantifier.Optional)
                                  ])

backtrace_frames = Message("BacktraceFrameList",
                           fields=[Field(Proto.Message, "frames", 1, q=Quantifier.Repeated, message=backtrace_frame)
                                  ])

es_debugger = Service("EcmascriptDebugger", version="5.0", coreRelease="2.4",
                      commands=[Request(1,  "ListRuntimes",        runtime_selection,   runtime_list)
                               ,Request(3,  "ContinueThread",      thread_mode,         False)
                               ,Request(5,  "Eval",                eval_data,           eval_result)
                               ,Request(7,  "ExamineObjects",      object_selection,    object_info)
                               ,Request(9,  "SpotlightObject",     spotlight_selection, False)
                               ,Request(11, "AddBreakpoint",       breakpoint_pos,      False)
                               ,Request(13, "RemoveBreakpoint",    breakpoint_id,       False)
                               ,Request(15, "AddEventHandler",     event_handler,       False)
                               ,Request(17, "RemoveEventHandler",  event_handler_id,    False)
                               ,Request(19, "SetConfiguration",    configuration,       False)
                               ,Request(21, "GetBacktrace",        backtrace_selection, backtrace_frames)
#                               ,Request(7,  "ExamineFrame",        frame_selection,     object_info)
# TODO ExamineFrame does not seem to exists, remove it
                               ,Event(0,  "OnRuntimeStarted",  runtime_info)
                               ,Event(2,  "OnRuntimeStopped",  runtime_id)
                               ,Event(4,  "OnNewScript",       script_info)
                               ,Event(6,  "OnThreadStarted",   thread_info)
                               ,Event(8,  "OnThreadFinished",  thread_status)
                               ,Event(10, "OnThreadStoppedAt", thread_stopinfo)
                               ,Event(12, "OnHandleEvent",     dom_event)
                               ,Event(14, "OnObjectSelected",  object_selection)
                               ],
                      cpp_class="ES_ScopeDebugFrontend", cpp_hfile="modules/scope/src/scope_ecmascript_debugger.h")
