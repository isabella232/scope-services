# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service, Options

# Service: ProbedataServer

probe_data = Message("ProbeData",
                     fields=[Field(Proto.Bytes, "data", 1)
                            ])

probedata_server = Service("ProbedataServer",
                           commands=[Request(1,  "AllData",  False, probe_data)
                                    ],
                           options=Options(version="2.0", core_release="2.4",
                                           cpp_class="OpScopeProbedataServer", cpp_hfile="modules/scope/src/scope_probedata_server.h"))
