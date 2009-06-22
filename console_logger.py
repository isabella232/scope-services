# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

console_message = Message("ConsoleMessage",
                          fields=[Field(Proto.Uint32, "windowID",    1)
                                 ,Field(Proto.Uint32, "time",        2)
                                 ,Field(Proto.String, "description", 3)
                                 ,Field(Proto.String, "uri",         4, q=Quantifier.Optional)
                                 ,Field(Proto.String, "context",     5, q=Quantifier.Optional)
                                 ,Field(Proto.String, "source",      7, q=Quantifier.Optional) # TODO: Make enum
                                 ,Field(Proto.String, "severity",    8, q=Quantifier.Optional) # TODO: Make enum
                                 ])

console_logger = Service("ConsoleLogger", version="2.0", coreRelease="2.4",
                         commands=[Event(1,  "OnConsoleMessage",  console_message)
                                  ],
                         cpp_class="OpScopeConsoleLogger", cpp_hfile="modules/scope/src/scope_console_logger.h")
