# OpProtoc
from opprotoc.proto import Proto, Quantifier, Field, Message, Request, Event, Service

# Service: EcmascriptLogger
# Is this service even used, and does it even work?
esl_new_script = Message("ScriptInfo",
                         fields=[Field(Proto.String, "context", 1)
                                ,Field(Proto.String, "url",     2)
                                ,Field(Proto.String, "source",  3)
                                ])

esl_configure = Message("Config",
                        fields=[Field(Proto.Bool, "reformat", 1, q=Quantifier.Optional)
                               ])

ecmascript_logger = Service("EcmascriptLogger", version="2.0", coreRelease="2.4",
                            commands=[Request(1, "Configure", esl_configure, False)
                                     ,Event(0,   "OnNewScript", esl_new_script)
                                     ],
                            cpp_class="OpScopeEcmascriptLogger", cpp_hfile="modules/scope/src/scope_ecmascript_logger.h")
