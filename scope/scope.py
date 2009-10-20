# hob
from hob.proto import Proto, Quantifier, Field, Message, Request, Event, Service, Options

client_info = Message("ClientInfo",
                      fields=[Field(Proto.String, "format", 1),
                              Field(Proto.String, "uuid", 2)
                             ])

connection_info = Message("ConnectionInfo",
                          fields=[Field(Proto.Uint32,  "clientID",  1)
                                 ])

service = Message("Service",
                  fields=[Field(Proto.String, "name",          1)
                         ,Field(Proto.String, "version",       2)
                         ,Field(Proto.Uint32, "activeClients", 3)
                         ,Field(Proto.Uint32, "maxClients",    4)
                         ])

command = Message("CommandInfo",
                  fields=[Field(Proto.String, "name",       1)
                         ,Field(Proto.Uint32, "number",     2)
                         ,Field(Proto.Uint32, "messageID",  3)
                         ,Field(Proto.Uint32, "responseID", 4)
                         ])

event = Message("EventInfo",
                fields=[Field(Proto.String, "name",      1)
                       ,Field(Proto.Uint32, "number",    2)
                       ,Field(Proto.Uint32, "messageID", 3)
                       ])

service_info = Message("ServiceInfo",
                       fields=[Field(Proto.Message, "commandList", 1, message=command, q=Quantifier.Repeated)
                              ,Field(Proto.Message, "eventList",   2, message=event, q=Quantifier.Repeated)
                              ])

service_selection = Message("ServiceSelection",
                            fields=[Field(Proto.String, "name", 1)
                                   ])

field_info = Message("FieldInfo",
                     fields=[Field(Proto.String, "name",       1)
                            ,Field(Proto.Uint32, "type",       2, doc="""The protocol buffer type for this field. The types are:

== ============================
1  Double
2  Float
3  Int32
4  Uint32
5  Sint32
6  Fixed32
7  Sfixed32
8  Bool
9  String
10 Bytes
11 Message
12 Int64 (not supported yet)
13 Uint64 (not supported yet)
14 Sint64 (not supported yet)
15 Fixed64 (not supported yet)
16 Sfixed64 (not supported yet)
== ============================
""")
                            ,Field(Proto.Uint32, "number",     3, doc="The unique protocol buffer number for this field.")
                            ,Field(Proto.Uint32, "quantifier", 4, q=Quantifier.Optional, default=0, doc="""Specifies whether the fields is required, optional or repeated:

= ========
0 Required
1 Optional
2 Repeated
= ========
""")
                            ,Field(Proto.Uint32, "messageID",  5, q=Quantifier.Optional, doc="ID of message this field references, only set for Message fields")
                            ])

message_info = Message("MessageInfo", doc="Introspection result for a given message.", children=[field_info],
                       fields=[Field(Proto.Uint32,  "id",        1)
                              ,Field(Proto.String,  "name",      2)
                              ,Field(Proto.Message, "fieldList", 3, q=Quantifier.Repeated, message=field_info)
                              ,Field(Proto.Uint32,  "parentID",  4, q=Quantifier.Optional)
                              ])

message_list = Message("MessageInfoList",
                       fields=[Field(Proto.Message, "messageList", 1, q=Quantifier.Repeated, message=message_info)
                              ])

message_selection = Message("MessageSelection", doc="Selects which messages to introspect.",
                            fields=[Field(Proto.String, "serviceName", 1, doc="Name of service to fetch messages from. Message ids are unique per service.")
                                   ,Field(Proto.Uint32, "idList",      2, q=Quantifier.Repeated, doc="Contains ids of message which should be fetched.")
                                   ,Field(Proto.Bool,   "includeRelated", 3, q=Quantifier.Optional, doc="""Set to true to automatically include messages which are referenced (fields of type Message). This makes it easy to fetch the entire message chain for a given message.""")
                                   ,Field(Proto.Bool,   "includeAll",     4, q=Quantifier.Optional, doc="""Set to true if all message in the service should be included. Overrides includeRelated and idList.""")
                                   ])

service_result = Message("ServiceResult",
                         fields=[Field(Proto.String, "name", 1)
                                ])

host_info = Message("HostInfo",
                      fields=[Field(Proto.Uint32,  "stpVersion",      1)
                             ,Field(Proto.String,  "coreVersion",     2)
                             ,Field(Proto.String,  "platform",        3)
                             ,Field(Proto.String,  "operatingSystem", 4)
                             ,Field(Proto.String,  "userAgent",       5)
                             ,Field(Proto.Message, "serviceList",     6, message=service, q=Quantifier.Repeated)
                             ])

client_id = Message("ClientID",
                    fields=[Field(Proto.String, "uuid", 1)
                           ])

service_list = Message("ServiceList",
                       fields=[Field(Proto.String, "serviceList",    1, q=Quantifier.Repeated)
                              ])

error_info = Message("ErrorInfo",
                     fields=[Field(Proto.String, "description", 1)
                            ])

window_manager = Service("Scope",
                         commands=[Request(3, "Connect",    client_info,       connection_info)
                                  ,Request(4, "Disconnect", client_id,         False)
                                  ,Request(5, "Enable",     service_selection, service_result)
                                  ,Request(6, "Disable",    service_selection, service_result)
                                  ,Request(7, "Info",       service_selection, service_info)
                                  ,Request(8, "Quit",       False,             False)
                                  ,Request(10, "HostInfo",  False,             host_info)
                                  ,Request(11, "MessageInfo", message_selection, message_list)
                                  ,Event(0, "OnServices",       service_list)
                                  ,Event(1, "OnQuit",           False)
                                  ,Event(2, "OnConnectionLost", False)
                                  ,Event(9, "OnError",          error_info)
                                  ],
                         options=Options(version="1.0", core_release="2.4",
                                         cpp_class="OpScopeProtocolService", cpp_hfile="modules/scope/src/scope_protocol_service.h"))
