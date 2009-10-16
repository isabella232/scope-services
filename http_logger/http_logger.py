# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service, Options

# Service: HttpLogger (core-2.2)

header = Message("Header",
                 fields=[Field(Proto.Uint32, "requestID", 1)
                        ,Field(Proto.Uint32, "windowID",  2)
                        ,Field(Proto.String, "time",      3, comment="Float encoded as string")
                        ,Field(Proto.String, "header",    4)
                        ])

http_logger = Service("HttpLogger",
                      commands=[Event(1,  "OnRequest",  header)
                               ,Event(2,  "OnResponse", header)
                               ],
                      options=Options(version="2.0", core_release="2.4",
                                      cpp_class="OpScopeHttpLogger", cpp_hfile="modules/scope/src/scope_http_logger.h"))

# Service: HttpLogger (core-2.3?)
#log_mode = Message("LogMode",
#                   fields=[Field(Proto.String, "type", 1) # TODO: Make enum "profiling" | "logging"
#                          ])
#
#response_selection = Message("ResponseSelection",
#                             fields=[Field(Proto.Uint32, "requestID", 1)
#                                    ,Field(Proto.String, "encoding",  2, q=Quantifier.Optional) # TODO: Make enum "none" | "base64"
#                                    ,Field(Proto.Uint32, "decoding",  3, q=Quantifier.Optional) # TODO: Make enum "none" | "used-by-opera"
#                                    ])
#
#response_body = Message("ResponseBody",
#                             fields=[Field(Proto.Uint32, "requestID", 1)
#                                    ,Field(Proto.String, "time",      2, comment="Float encoded as string")
#                                    ,Field(Proto.String, "encoding",  3, q=Quantifier.Optional)
#                                    ,Field(Proto.String, "decoding",  4, q=Quantifier.Optional)
#                                    ,Field(Proto.String, "body",      5, q=Quantifier.Optional)
#                                    ])
#
#parsed_header = Message("Header",
#                        fields=[Field(Proto.String, "name",  1)
#                               ,Field(Proto.String, "value", 2)
#                               ])
#
#request_header = Message("Request",
#                         fields=[Field(Proto.Uint32, "requestID", 1)
#                                ,Field(Proto.Uint32, "windowID",  2)
#                                ,Field(Proto.Uint32, "runtimeID", 3, comment="this is perhaps not neccessary if we have frame path")
#                                ,Field(Proto.String, "framePath", 4)
#                                ,Field(Proto.String, "time",      5, comment="Float encoded as string")
#                                ,Field(Proto.String, "method",    6)
#                                ,Field(Proto.String, "uri",       7) # Note: Changed to uri (from url) to make it consistent
#                                ,Field(Proto.Message, "headers",  8, q=Quantifier.Repeated, message=parsed_header)
#                                ])
#
#response_header = Message("ResponseHeader",
#                          fields=[Field(Proto.Uint32,  "requestID", 1)
#                                 ,Field(Proto.String,  "time",      2, comment="Float encoded as string")
#                                 ,Field(Proto.String,  "mimeType",  3)
#                                 ,Field(Proto.String,  "encoding",  4)
#                                 ,Field(Proto.Uint32,  "status",    5)
#                                 ,Field(Proto.String,  "rawHeader", 6)
#                                 ,Field(Proto.Message, "headers",   7, q=Quantifier.Repeated, message=parsed_header)
#                                 ])
#
#http_logger = Service("HttpLogger", version="2.0", coreRelease="2.4",
#                      commands=[Request(1,  "SetLogMode",      log_mode, False)
#                               ,Request(3,  "GetLogMode",      False,    log_mode)
#                               ,Request(5,  "GetResponseBody", response_selection, response_body)
#                               ,Event(0,  "Request",        request_header)
#                               ,Event(2,  "ResponseHeader", response_header)
#                               ],
#                      cpp_class="OpScopeHttpLogger", cpp_hfile="modules/scope/src/scope_http_logger.h")
