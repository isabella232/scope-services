Scope DOM API
=============

Most of the changes related to `STP/1` will be handled by the backend of
the ``JS``/``DOM`` API. This means that scope will decide features based on what is
available in the host.

When only `STP/0` is available in host, scope will perform these steps.

- Receive initial service list.
- Initiate `STP/0` fallback if the host runs core-2.4 or higher,
  otherwise it is up the JS client to handle older core versions.
  The fallback will be setup to send data as ``JSON``.

For `STP/1` scope will perform these steps.

- Receive initial service list.
- Initiate `STP/1` handshake.
- Initiating contact with the host to receive a client ID (scope.Connect).
- When selecting format for messages, it will use protocol buffer for `STP/1`
  and ``JSON`` for `STP/0`.

Determine DOM API version
-------------------------
  
The new ``DOM`` API can be detected by checking if the ``stpVersion`` function
is available on the ``opera`` object. This can be called to get
the version of the built-in transport layer.

For instance, calling it on core-2.4 would return::

  "STP/1"

Adding a client
---------------

``scopeAddClient`` is used to register a new client to scope. It will remove any
existing client before adding the new one as the current client.
The call will initiate contact with scope. If ``port`` is set to 0 it will contact
the built-in scope, otherwise it will use it as a port number on a remote host
and await connections from it. After this the remote host must start the
debugger through the URL opera:debug.

The call also registers callbacks when the host is connected, when messages
are received (responses or events), and when the remote host disconnects.

The signature is:

.. function:: scopeAddClient(connected: callback, receive: callback, quit: callback [, port: number])

``port` is optional and 0 by default.

The ``connected`` callback is called when the service list has been sent from the
host and is available for the client to look at. For `STP/0` that means right
after the service list is received, for `STP/1` it will happen after the
handshake and client connect phase is complete.

The service list will be modified to only show the currently used STP version.
For instance if `STP/1` was chosen it would contain "stp-1" while if `STP/0`
was chosen it would contain "stp-0-json".

The signature of the callback is:

.. function:: connected(services: string)
  
The ``receive`` callback exists in two versions, one of which is `STP/0` where only
the service name and message payload is known.

The `STP/0` signature is:

.. function:: receive(service: string, message: string)

For `STP/1` additional arguments are present which reflect the extra fields that
are part of the transport message.
They are:

``command``:
  The numeric value of the command in use. The actual value is unique per
  service, and can be found by looking at the specific service definition.

``status``:
  The numeric value of the status value. See the `STP/1` document for explanation. A
  value of 0 means everything is ok, while any other value means an error.

``tag``:
  The synchronization tag that was initially sent to the host. If the command
  is an even numeric value, the tag value will be 0.

In addition the message payload will be decoded by scope, and will contain JavaScript
objects as opposed to those in `STP/0` where the message is just a string.
Scope will decode the data from the incoming protocol buffer data by 
first requesting message definitions from the host and then using that to decode.

The `STP/1` signature is:

.. function:: receive(service: string, message: datastructure|string, command: integer, status: integer, tag: integer)

The ``quit`` callback is called when the remote host disconnects.
The signature is:

.. function:: quit()

Example code for `STP/1`:

.. code-block:: javascript

  var connected = function(services)
  {
    services = services.split(","); // TODO: Does this exist?
    for service in services
    {
      if (service.substring(0, 5) == "stp-0")
      {
        alert("Connected to STP/1 host but using STP/0 fallback");
        return;
      }
      else if (service == "stp-1")
      {
        alert("Connected to STP/1 host");
        return;
      }
      alert("Connected to STP/0 host");
    }
  }

  var receive = function(service, message, command, status, tag)
  {
    if (status != 0)
    {
      alert("Error in command " + command);
      return;
    }
    if (tag != 0)
    {
      // Handle response to previous command
    }
    else
    {
      // Handle event
    }
  }

  var quit = function()
  {
  }

  opera.scopeAddClient(connected, receive, quit, 0)

Enabling a service
------------------

For `STP/0` the client must use ``scopeEnableService`` to enable a service.

The function signature is:

.. function:: scopeEnableService(service: string)

For `STP/1` the client must enable the service by sending a message to the
``scope`` service, using ``scopeEnableService`` will do nothing.
The command `Enable` has integer value 5 and uses the following structure::

  message ServiceSelection
  {
    required string name = 1;
  }

For instance to enable the WindowManager one would do:

.. code-block:: javascript

  scopeTransmit("scope", ["window-manager"], 5 /*scope.Enable*/, tag);

The client will receive a normal message in the `receive` callback when the
service is enabled.

Transmitting data
-----------------

``scopeTransmit`` will now accept data into services in native JavaScript objects
if the host is running core-2.4 or higher. If the host is core-2.3 or lower,
it will be transmitted as a string as before.

For `STP/0` the signature is:

.. function:: scopeTransmit(service: string, message: string)

For `STP/1` there are extra arguments available which will be put in the
`STP/1` transport message.

``command``:
  The numeric value of the command in use. The actual value is unique per
  service and can be found by looking at the specific service definition.

``tag``:
  The synchronization tag which is sent to the host and later sent to the
  ``receieve`` callback. The tag can contain the values in the range
  1 to 2^32-1. A value of 0 or negative values are not allowed.

The signature is:

.. function:: scopeTransmit(service: string, message: datastructure|string, command: integer, tag: integer)
  
Example code for `STP/0`:

.. code-block:: javascript

  var receive = function(service, message)
  {
  }

  opera.scopeTransmit("ecmascript-debugger", "<get-runtimes></get-runtimes>");

Example code for `STP/1`:

.. code-block:: javascript

  var receive = function(service, message, command, status, tag)
  {
  }

  opera.scopeTransmit("ecmascript-debugger", [], 1, 42);




