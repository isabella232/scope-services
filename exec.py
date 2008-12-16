# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

# Service: Exec

exec_data = Message("Exec",
                    fields=[Field(Proto.Message, "Actions", 1, q=Quantifier.Repeated,
                                  message=Message("Action", is_global=False,
                                                  fields=[Field(Proto.String, "Name",  1)
                                                         ,Field(Proto.String, "Value", 2)
                                                         ]))                                                          
                           ])

exec_service = Service("Exec",
                       commands=[Request(1,  "Exec", exec_data, False)
                                ],
                       cpp_class="OpScopeExec", cpp_hfile="modules/scope/src/scope_exec.h")
