Scope DOM API
=============

This describes the DOM interfaces for ``scope``. The interfaces are divided
into three parts, a common interface which can be used at any time and two
specific interfaces. Which one to use depends on the *STP* version which is
currently active.

Accessing the DOM interface is done via the ``opera`` object and is only
available for the special *developer tools* window.

Scope
^^^^^

This is the common interface and is used to create a new client and to
query the *STP* version in use, either :ref:`STP/0<stp0>` or :ref:`STP/1<stp1>`.

.. _Scope:

The Scope interface
-------------------

.. code-block:: java

  interface Scope {
    readonly attribute DOMString stpVersion;
    boolean scopeAddClient(in ConnectListener onconnect, in ReceiveListener onreceive, in DisconnectListener ondisconnect, [Optional] in unsigned long port);
  };

.. _stpVersion:
.. attribute:: stpVersion

    Contains the *STP* version of the current connection. The string
    contains either ``"STP/0"`` or ``"STP/1"`` for an active connection and
    ``"STP/0"`` when no connection has been made.

.. _scopeAddClient:
.. function:: scopeAddClient(onconnect, onreceive, ondisconnect, port)

    Registers a new client in scope along with the callbacks `onconnect`,
    `onreceive` and `ondisconnect`. The call will initiate contact with the
    builtin scope or a remote host depending on the `port` parameter.
    If a remote host debugging is used then scope will await a connection from
    the remote host, in other words the remote host must connect using
    *opera:debug*.

    :note: It will remove any existing client before setting the new one as
           the current client

    :param onconnect:    ConnectListener_ which is called when connection to host is established.
    :param onreceive:    ReceiveListener_ which is called when new messages arrive from the host.
    :param ondisconnect: DisconnectListener_ which is called when connection to host is lost.
    :param port:         The port on to the remote host or *0* if the builtin host is to be used.
    :returns: `true` if the client was successfully created, `false` otherwise.

.. _ConnectListener:

The ConnectListener interface
-----------------------------

.. code-block:: java

  [Callback=FunctionOnly] interface ConnectedListener {
    void onconnected(in DOMString services);
  };

.. function:: onconnected(services)

    Called when the connection with the (remote or builtin) host has been made.
    For an *STP/0* host this means right after the service list is received,
    for *STP/1* it will happen after the handshake and client connect phase is
    complete.

    :param services: A string containing a comma separated list of services
                     available in the host. e.g. ``"scope,ecmascript-debugger,exec"``

.. _DisconnectListener:

The DisconnectListener interface
--------------------------------

.. code-block:: java

  [Callback=FunctionOnly] interface DisconnectListener {
    void ondisconnect();
  };

.. function:: ondisconnect()

    Called when the connection to the host is disconnected.

.. _stp0:

STP/0
^^^^^

.. _stp0-if:

The STP/0 interface
-------------------

.. code-block:: java

  interface Stp0 : Scope {
    boolean scopeEnableService(in DOMString service);
    boolean scopeTransmit(in DOMString service, int DOMString payload);
  };

.. _scopeTransmit-stp0:
.. function:: scopeTransmit(service, payload, command, tag)

    Perform a remote call in specific service.

    :param service: Name of service to make the call in.
    :param payload: Data for the command, structure depends on the command.
                    Usually an array in the form *[arg1, arg2, ...]*
    :param command: ID of the command to call, lookup the service definition
                    to find the command ID.
    :param tag: Assign a `tag` value for the message, this will be present in
                the response (``ReceiveListener``). The value of the tag
                carries no special meaning for the host so any value is
                possible, however the client should avoid conflicts by ensuring
                a unique value for each active request.
    :returns: `true` if the data was successfully sent, `false` otherwise.

.. _scopeEnableService-stp0:
.. function:: scopeEnableService(service)

    :param service: Name of service to enable.
    :returns: `true` if the request to enable a service was succesfully sent,
              `false` otherwise.

.. _ReceiveListener-stp0:

The ReceiveListener interface
-----------------------------

.. code-block:: java

  [Callback=FunctionOnly] interface ReceiveListener {
    void onreceived(in DOMString service, in DOMString payload);
  };

.. function:: onreceived(service, payload, command, status, tag)

    Called when a new message has been sent to the client, this can either
    be a response, an event or an error.

    :param service: The service which sent the response or event.
    :param payload: The response from service as a string.
                    If the host is capable of using *STP/1* the payload will
                    also contain the STP header before the actual payload.
                    See :doc:`scope-transport-protocol` for more details.

.. _stp1:

STP/1
^^^^^

.. _stp1-if:

The STP/1 interface
-------------------

.. code-block:: java

  interface Stp1 : Scope {
    boolean scopeTransmit(in DOMString service, in any payload, in unsigned long command, in unsigned long tag);
  };

.. _scopeTransmit:
.. function:: scopeTransmit(service, payload, command, tag)

    Perform a remote call in specific service.

    :param service: Name of service to make the call in.
    :param payload: Data for the command, structure depends on the command.
                    Usually an array in the form *[arg1, arg2, ...]*
    :param command: ID of the command to call, lookup the service definition
                    to find the command ID.
    :param tag: Assign a `tag` value for the message, this will be present in
                the response (``ReceiveListener``). The value of the tag
                carries no special meaning for the host so any value is
                possible, however the client should avoid conflicts by ensuring
                a unique value for each active request.
    :returns: `true` if the data was successfully sent, `false` otherwise.

.. _ReceiveListener:

The ReceiveListener interface
-----------------------------

A callback which is used whenever a new message (response, event or error)
is received from the host.

.. code-block:: java

  [Callback=FunctionOnly] interface ReceiveListener {
    void onreceived(in DOMString service, in any payload, unsigned long command, unsigned long status, unsigned long tag);
  };

.. function:: onreceived(service, payload, command, status, tag)

    Called when a new message has been sent to the client, this can either
    be a response, an event or an error.

    :param service: The service which sent the response or event.
    :param payload: The response from the service as an array, structure
                    depends on the service and command. Usually in the form
                    *[res1, res2, ..]*
    :param command: ID of the command which triggered the response or the ID
                    of the event which was triggered. The actual value is
                    unique per service, and can be found by looking at the
                    specific service definition.
    :param tag:    The `tag` value which was previously sent in scopeTransmit_.
                   If the message does not contain a tag or it was an event it
                   will be set to ``0``.
    :param status: The status of the response. A value of ``0`` means the call
                   was successful while a non-zero value means an error occured.
                   Refer to the :doc:`scope-transport-protocol` document for
                   error codes.

Examples
^^^^^^^^

Adding a client
---------------

Adding a new client is done with the scopeAddClient_ call but some
additional checking is required once the connection has been made.
Two things must be checked, first the capability of the *DOM* interface
then the capability of the (remote or builtin) host.

1. The property stpVersion_ will be present if the new *DOM* interface
   is present.

2. The host can be checked by seeing if the service **"stp-1"** is present
   in the service list.

Example code:

.. code-block:: javascript

  var onconnect = function(services)
  {
    alert("Services " + services);
    if ("stpVersion" in opera)
    {
        // We are using the STP/1 dom interface
        // check which version is in use
        if (opera.stpVersion == "STP/1")
            alert("Connected to STP/1 host");
        else
            alert("Connected to STP/0 host but using STP/1 dom interface");
    }
    else
    {
      // We are using a pre-STP/1 dom interface
      // check for stp-1 in the service list
      for (service in services.split(","))
      {
        if (service == "stp-1")
        {
            alert("Connected to STP/1 host but using STP/0 dom interface");
            return;
        }
      }
      alert("Connected to STP/0 host");
    }
  }

  var onreceive = function(service, message, command, status, tag)
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
      // Handle event or non-tagged response
    }
  }

  var ondisconnect = function()
  {
    alert("Host has been disconnected");
  }

  opera.scopeAddClient(onconnect, onreceive, ondisconnect, 0)

Enabling a service
------------------

For *STP/0* connections the client must use :ref:`scopeEnableService<scopeEnableService-stp0>` to enable a service,
otherwise it must do a normal call using scopeTransmit_ using the Scope.Enable
command.

Example code to enable :doc:`WindowManager` in an STP/0 host:

.. code-block:: javascript

  scopeEnableService("window-manager");

No response is received for this.

Example code to enable :doc:`WindowManager` in an STP/1 host:

.. code-block:: javascript

  scopeTransmit("scope", ["window-manager"], 5 /*scope.Enable*/, tag);

The client will receive a normal message in the `onreceive` callback when the
service is enabled.

Transmitting data
-----------------

scopeTransmit_ is used to send data to the host. For the *STP/1* *DOM* interface
this is done using native JavaScript objects, where-as the *STP/0* *DOM* interface
requires data as a string and must be manually serialized.

Example code for *STP/0*:

.. code-block:: javascript

  var onreceive = function(service, message)
  {
  }

  opera.scopeTransmit("ecmascript-debugger", "<get-runtimes></get-runtimes>");

Example code for *STP/1*:

.. code-block:: javascript

  var onreceive = function(service, message, command, status, tag)
  {
  }

  opera.scopeTransmit("ecmascript-debugger", [], 1, 42);
