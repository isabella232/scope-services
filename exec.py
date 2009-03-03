# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

# Service: Exec

exec_data = Message("ActionList",
                    fields=[Field(Proto.Message, "Actions", 1, q=Quantifier.Repeated,
                                  message=Message("Action", is_global=False,
                                                  doc="""Executes a series of actions in the opera host, each action consists of a name identifying the action and a value for the action. The value depends on the type of action.""",
                                                  fields=[Field(Proto.String, "Name",  1,
                                                                doc="""The name of the action to execute, can be one of:\n"""
                                                                    """keydown | keyup: The `Value` is either a key-name ("ctrl", "down", etc.) or a single character ("a", "b", etc.)\n"""
                                                                    """type: Types the text present in `Value`.\n"""
                                                                    """action: Perform action which is stored in `Value` ("Page Down", "New Page", etc.)""")
                                                         ,Field(Proto.String, "Value", 2)
                                                         ]))                                                          
                           ])

exec_service = Service("Exec", version="2.0", coreRelease="2.4",
                       doc="""The Opera Exec protocol can be used to control an Opera instance from the outside, and various operations can be initiated. This functionality is mainly useful for QA testing.""",
                       commands=[Request(1,  "Exec", exec_data, False)
                                ],
                       cpp_class="OpScopeExec", cpp_hfile="modules/scope/src/scope_exec.h")
