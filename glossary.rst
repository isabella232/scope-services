.. _glossary:

Glossary
========

.. glossary::

  client
    An application which acts as debugger.

  host
    An Opera instance to be debugged. The same as debugee. 

  message
    In the context of ``STP`` or the scope interface it is an entity in the communication between a :term:`host` and a :term:`client`. It is either a command, a response, an event or an error. 

  service
    The meaning depends on the context. A service on the :term:`host` is a domain specific part of the scope interface. It can be enabled and disabled. So far there is ``Scope``, ``WindowManager``, ``ConsoleLogger``, ``HTTPLogger``, ``Exec``, ``EcmascriptDebugger`` and ``URLPlayer``. 
    On the :term:`client` it means normally an object which exposes the specific interface as a counterpart of the host service as an API. 


