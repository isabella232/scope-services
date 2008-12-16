# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

# Service: ProbedataServer

probe_data = Message("ProbeData",
                     fields=[Field(Proto.Bytes, "data", 1)
                            ])

probedata_server = Service("ProbedataServer",
                           commands=[Request(1,  "AllData",  False, probe_data)
                                    ],
                           cpp_class="OpScopeProbedataServer", cpp_hfile="modules/scope/src/scope_probedata_server.h")
