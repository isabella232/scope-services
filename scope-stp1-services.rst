================
 Scope services
================

:Author:  Jan Borsodi (jborsodi [at] opera.com)
:Version: 0.3
:Date:    22nd April 2009

System commands
===============

All previous system commands (starting with an `*`) will be now be organized in
a proper service called "scope".

Services and multiple clients
=============================

Some services allows multiple clients to be active while others should
only have one client active at a time.
For instance, the ECMAScript debugger involves getting information about new
threads and scripts, and can change the current state with breakpoints and
continuing execution. If two or more clients do this it would be impossible for
them to know what state the Opera host is in. There can also be conflicting
requests if both try to act on stopped threads in different ways.

Whenever a client enables a service, the service will be able to differentiate
between them with a unique client ID. The service can keep track of which
clients are active and send back information to specific clients if it wants.
It can also deny new clients attempting to be active if one already is active.
If a service denies a client it responds with the status 1 (Conflict).

Service: Scope
==============

This is a special service which is always present and always enabled.

This service replaces the special commands used in STP/0 (started with an asterix).
The only command that is fully compatible with STP/0 is "\*services" (OnServices)
which is actually sent as STP/0 only, any other special command sent to scope
will be ignored.
The system takes care of mapping it to the correct format when sending and
receiving them. However the payload of these messages is no longer the same:
they must now be sent using UMS. This means using either JSON or XML when
sending over STP/0.

The service list is defined as::

  *services <service-list>

Overview
--------

.. note::
   The IDs for the commands and events might change before the final version.

Commands:

  ================= =========
  Name              CommandID
  ================= =========
  Connect           3
  Disconnect        4
  Enable            5
  Disable           6
  Info              7
  Quit              8
  HostInfo          10
  ================= =========

Events:

  ================= =========
  Name              CommandID
  ================= =========
  OnServices        0
  OnQuit            1
  OnConnectionLost  2
  OnError           9
  ================= =========

Event: OnServices
-----------------

CommandID: 0

This event is the first that is sent from the host (and proxy) and contains
all the available services. It is always sent encoded as an STP/0 message.

The event is defined as::

  event OnServices returns ServiceList;
  
  message ServiceList
  {
      repeated string service = 1;
  }

Event: OnQuit
-------------

CommandID: 1

This event is sent by Opera to the proxy or client when Opera terminates its
operation. No communication with Opera is possible once Opera has sent the
event. When the proxy receives this message it broadcasts it to all of its
clients.

The event is defined as::

  event OnQuit returns Default;

Event: OnConnectionLost
-----------------------

CommandID: 2

This is a special event which is used by the proxy (and not by the host) when the connection
to the Opera host is unexpectedly lost, for instance if the Opera host crashes.

The event is defined as::

  event OnConnectionLost returns Default;

Event: OnError
--------------

CommandID: 9

This is a generic event for sending out error messages which are not tied to a specific
command.

The event is defined as::

  event OnConnectionLost returns ErrorInfo;
  
  message ErrorInfo
  {
      required string description = 1;
  }

Command: Connect
----------------

CommandID: 3

This commands is used by the client to initiate connection with the host.
The host will register the client and respond with a numerical client ID
which is then used for subsequent commands and events.
The command also specifies the global settings for the client. Currently this
means setting the format of all messages for this client.

Repeated use of this command will result in the host resetting any settings
and services that the client used earlier.

.. note::
  The uuid field is required both in the STP message and in the payload.
  This ensures that any proxies can relay the information properly and
  that the host or client(s) can read the message uniformly.

The command is defined as::

  command Connect(ClientInfo) returns ConnectionInfo;

  message ClientInfo
  {
      required string format = 1; // "protobuf" | "json" | "xml"
      required string uuid = 2; // Unique ID for the client
  }

  message ConnectionInfo
  {
      required uint32 clientID = 1;
  }

The command responds with the new client ID which is to be used by all
subsequent commands. This client ID is also used when sending out events.

Errors:

* If the requested format is not allowed or does not exist, it will respond
  with the status "Bad Request" (3).

Command: Disconnect
-------------------

CommandID: 4

This disconnects the client by resetting any settings and disabling any services
the client used. This command is primarily meant for proxies which must be
sent if a socket connection with an active client closes.
If the client is able to do this, then it should send the command itself.

.. note::
  The uuid field is required both in the STP message and in the payload.
  This ensures that any proxies can relay the information properly and
  that the host or client(s) can read the message uniformly.

The command is defined as::

  command Disconnect(ClientID) returns ClientID;
  
  message ClientID
  {
      required string uuid; // Unique id for the client.
  }

Command: Enable
---------------

CommandID: 5

This is used to enable one service in the host.

.. note::
   The old behaviour of the proxy which allowed a comma-separated list
   of services is no longer supported.

It is defined as::

  command Enable(ServiceSelection) returns Default;

  message ServiceSelection
  {
      required string name = 1;
  }

It will enable the service and report back the result.

Errors:

* If the service is not found it will return with status
  "Service Not Found" (6).
* If the service could not be enabled it will return with status
  "Service Not Enabled" (8).
* If the client tries to enable the "scope" service it will return with status
  "Bad Request" (3).
* If the client tries to enable a service before the Configure command has been
  used it will return with status "Bad Request" (3).

Command: Disable
----------------

CommandID: 6

This is used to disable a client's access to one service. If the service
has other clients connected the service will stay enabled.
Once the client has been removed the from the service it will no longer
receive events from it, and it will not be able to send commands to it.
The internal "scope" service cannot be disabled since it is always enabled.

It is defined as::

  command Disable(ServiceSelection) returns Default;

  message ServiceSelection
  {
      required string name = 1;
  }

The response contains no data.

Errors:

* If the service is not found it will return with a status of
  "Service Not Found" (6).
* If the service is not yet enabled it will return with a status of
  "Service Not Enabled" (8).
* If the client tries to disable the "scope" service it will return with a
  status of "Bad Request" (3).

Command: Info
-------------

CommandID: 7

This is used to get information about one specific service.

It is defined as::

  command Info(ServiceSelection) returns ServiceInfo;

  message ServiceSelection
  {
      required string name = 1;
  }

  message ServiceInfo
  {
      repeated Command commands = 1;
      repeated Event   events = 2;
  }

  message Command
  {
      required string name = 1;
      required uint32 number = 2;
  }

  message Event
  {
      required string name = 1;
      required uint32 number = 2;
  }

The command list contains all the commands in the service. Each command is
listed with its name and the corresponding command ID (used by STP/1).
The event list is similar to the command list, but is listed for the available
events.

Errors:

* If the service is not found it will return the message with status set
  to "Service Not Found" (6).

Command: Quit
^^^^^^^^^^^^^

CommandID: 8

The quit message is sent to Opera when the proxy or client operation is terminated.
No communication with the proxy will be possible once it has sent the quit
message. When Opera receives this message it should disable all debugging
services that are currently enabled. 

It is defined as::

  command Quit(Default) returns Default;

Command: HostInfo
-----------------

CommandID: 10

This commands is used to get information about the host.

The command is defined as::

  command Connect(Default) returns HostInfo;

  message HostInfo
  {
      required uint32  stpVersion = 1;
      required string  coreVersion = 2;
      required string  platform = 3;
      required string  operatingSystem = 4;
      required string  userAgent = 5;
      repeated Service services = 6;
  }
  
  message Service
  {
      required string name = 1;
      required string version = 2;
      required uint32 activeClients = 3;
      required uint32 maxClients = 4;
  }

The command responds with information on available services, version, and
other relevant information.

The `version` field contains the major and minor version number of the service.
The first number is the major version, the second is the minor, and any additional
numbers/strings are not of relevance but can be shown to the end-user if wanted.

The major version determines major changes (ie. compatibility breaks), while
the minor version determines incremental changes (ie. backwards compatible).
The client must check these two numbers to ensure it is able to communicate
properly with the service. If the major version is different from the
versions the client is compatible with, or the minor version is less than
the required version, it must disconnect.

Let us say a client supports version 1.6 and up and also version 2.0 and up.
It would do::

  if major == 1 and minor >= 6 or major == 2:
    print "We support service version %d.%d" % (major, minor)
  else:
    print "We do not support service version %d.%d" % (major, minor)
