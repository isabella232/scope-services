=============================
 Scope transport protocol v1
=============================

:Author:  Jan Borsodi (jborsodi [at] opera.com)
:Version: 0.10
:Status:  Draft
:Date:    22nd April 2009

EBNF
====

The following common EBNF_ entries are defined:

.. _EBNF: http://en.wikipedia.org/wiki/Ebnf

.. productionlist::
  pb_uint_short: <32bit unsigned encoded as Protocol Buffer varint>
  number       : `digit`+
  digit        : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
  space        : "\x20"
  newline      : "\x0a"

Unified Message Structure
=========================

The payload of all messages sent from *scope* will follow the specification
:doc:`unified-message-structure`. This specification is abbreviated as UMS
throughout the document.

Protocols
=========

There are currently several different protocols in use by scope and its related
components. To avoid confusion between them and their improvements, they
are summarized in the following sections.

Scope Transport Protocol
------------------------

This is the basic component in the communication layer, abbreviated as STP.
It defines how to send commands with data (arguments) between the
Opera host and the clients.

STP version 0 is defined as:

.. productionlist::
  stp         : `count` `terminator` `keyword` `terminator` <payload>
  terminator  : `space`
  count       : `number`
  keyword     : `command` | `service`
  command     : "*" `command_name`
  command_name: "services" | "enable" | "disable" | "quit" | "hostquit"
  service     : <any source character except ",">+

The flow of the transport protocol currently looks like this::

  Opera                           proxy                    client
  
  *services     ---------------->
                                      ----------------->   *services
                                      <-----------------   *enable
  *enable       <----------------
  data          <--------------------------------------->  data
                                  ....
                                      <------------------  *quit
  *disable      <----------------
  *quit         ---------------->
                                      ------------------>  *hostquit
                                      ------------------>  *quit

STP is used between the Opera host and the proxy as well as between the proxy
and clients speaking STP.

STP version 1 is described in detail in `STP/1`_.

Scope HTTP Adapter Protocol
---------------------------

This is the communication layer between the proxy and the clients
which are limited to HTTP communication. The proxy takes care of transforming
the STP communication to HTTP request/responses. The major difference is how
requests and responses/events are handled. In HTTP the request/response is
synchronous, and you cannot receive data without asking for it.

This protocol is currently implemented in the tool *Dragonkeeper*.

Scope DOM Interface
-------------------

This is the direct communication layer used between the Opera Host and the
JavaScript client. Here the STP is trimmed down to only send the KEYWORD and
DATA elements. All of this is handled by the the *opera.scopeTransmit* and
*opera.scopeAddClient* JavaScript functions.

This is currently used by the built-in Opera Dragonfly client for the Opera
9.5 desktop release.

A new interface is designed to accomodate the changes in STP/1, it is
explained in details in :doc:`scope-dom-interface`.

Problems
========

The current protocol is based around sending *Unicode* strings to and from the
clients, which makes it difficult to send binary data. Also, the encoding is
hardcoded to *UTF-16* for the entire message (STP and payload). This represents
uneccessary overhead for sending data which is often in *US-ASCII* only.

XML is used as primary format which is inefficient when transporting lots
of data. Lightweight alternatives are needed. XML also affects the decoding
process of some clients since it must first decode it to a DOM tree, and
then extract the interesting parts using the DOM interface which is slow and
cumbersome.

The format is predeterminded by each service and there is no way
to change it dynamically. For instance, JavaScript based clients will be
able to decode the responses more quickly if they are sent as JSON.

There is no standardized way to tie (<tag>) a response to a previous
request. This is currently embedded in the content of the request
which is specific to each service and each command in the service. For
instance, if you receive an error message there is no information about
what request caused this error. This is due to the error handler being outside
of the service implementation, and it has no knowledge of the <tag> entry.
There is also a chance of <tag> conflicts when multiple clients are in use.
A better system for handling the tags is needed.

The protocol was designed to handle multiple clients with the use of
the proxy. However, there are problems with multiple clients
in some services (ecmascript-debugger). Multi-client will be removed and the
proxy updated to only allow one client at a time.
  
Overview
========

The various parts of the scope communication chain are:

===================== ====================
Communication         Port/Protocol
===================== ====================
Opera<->Proxy/Client  Port:7001 STP/0
Proxy<->Clients       Port:8001 STP/0
Proxy<->HTTP-Client   Port:8002 HTTP/1.1
Opera<->Opera         Port:49152-65535 STP/0
Opera<->Remote Opera  Port:49152-65535 STP/0
Opera<->JS-Client     DOM interface
===================== ====================

To get a better overview, a few examples follow which display how the various
protocols communicate.

A typical developer setup with Opera Dragonfly communicating with the Proxy
using Dragonkeeper::

  +-------+ STP/0 +--------------+ HTTP/1.1 +-----------+
  |       | 7001  |              |   8002   |   Opera   |
  | Scope |<----->| Dragonkeeper +<-------->| Dragonfly |
  |       |       |              |          |           |
  +-------+       +--------------+          +-----------+

The common usage scenario with Opera Dragonfly connecting to Opera using
the internal JavaScript methods. Internally these methods will
communicate with scope using an internal socket (this will be changed)::

  +-------+ +----------+            +-----------+
  |       | | Opera    | JavaScript |   Opera   |
  | Scope | | Internal |<---------->| Dragonfly |
  |       | | "Proxy"  |            |           |
  +-------+ +----------+            +-----------+
     ^         ^
     |         |
     +---------+
        STP/0
     49152-65535

Another setup follows with Opera Dragonfly for remote debugging on an embedded device,
in this case a mobile phone::

  +-------+ +----------+            +-----------+
  |       | | Opera    | JavaScript |   Opera   |
  | Scope | | Internal |<---------->| Dragonfly |
  |       | | "Proxy"  |            |           |
  +-------+ +----------+            +-----------+
               ^
               |
               |
               | STP/0
  +---------+  | 7001
  |         |  |
  | Phone   |<-+
  | w/Scope |
  |         |
  +---------+

Other clients can communicate directly using STP. In the following case, the Python client 
is shown::

  +-------+ STP/0 +-------+  STP/0   +---------+
  |       | 7001  |       |   8001   |         |
  | Scope |<----->| Proxy +<-------->| PyScope |
  |       |       |       |          |         |
  +-------+       +-------+          +---------+

Backwards compatibility
=======================

The new protocol will introduce a major break in compatibility between the
host, proxy and clients. To ensure that future changes are less disruptive
a set of compatibility rules will be defined. The various components in scope
will be defined to either provide a break between each version change, or
provide only incremental changes for each version.

The transport protocol is the fundemental part. Changes to it will be difficult
to do incrementally, so there is only a need for breaks between versions.
This means that clients must immediately disconnect if they encounter a
version they do not know how to handle.

Services however, will use a combination of incremental and breaking changes.
This is handled by supplying a version number with two components: the first
is the major version and determines changes that will break existing clients, and 
the second is the minor version which will determine incremental (or additional)
changes. This means that clients will not need to be updated if only the minor
version increases. For this to be possible the following rules apply:

1. Events and responses will be sent using the same structure as the previous
   versions.
2. Events and commands can only get new optional parameters. Existing
   parameters cannot change or be removed.
3. If a command requires a change of behaviour (or parameter change), a new
   command must be made and the existing one must be kept.
4. New and optional parameters to commands can be used to trigger extended
   functionality or alternative behaviour. However, this must be confined to
   the client that requests the command.
5. The order of fields can never be changed.
6. New events can be added as long as they are optional. This also means that
   clients must ignore events which they do not recognize.

If the amount of work to keep backwards compatibility increases, or the code
gets bloated, the major version must be increased. This will signal a major
change and allows for older behaviour and code to be cleanup or removed.

The compatibility changes in each service are handled separately. This ensures
that a client which is dependent on one specific service does not need to
change unless that service gets a major change.

Finally, a global version for scope is defined. This will use the current core
version. It allows clients with more complex service dependencies a way to
determine available features on a global scale.

Transport layer
---------------

The transport layer will support both the new protocol (STP/1) and the old
one (STP/0). If not all of the nodes on the transport layer can speak the new protocol,
it will fallback to STP/0 and encode the message. It can then be transported
over STP/0 until it reaches the destination where it can be decoded into
a real STP/1 message. This is known as `Extended STP/0`_.

Opera host
----------

The host will first send out the service list using the old syntax (\*services).
Then it will wait for the first request from the client. If the client sends
the new handshake, the version to use is determined in the handshake message.
Otherwise it means an older client is connecting, and the host will switch
to `Extended STP/0`_.

Proxy
-----

The proxy will also support both protocol versions. The version that will
be used is determined by the client unless the host is running core-2.3 or
lower. In this case all communication is done using STP/0.

The HTTP API as it is today will be removed from the external proxy as it
is only used for internal development of Opera Dragonfly. A separate
implementation will be made for development purposes only.

Client
------

New clients will need to decide the version of the protocol to use. If the host
and proxy supports STP/1 then it can choose to initiate this by performing
the new handshake. If STP/1 cannot be used then the client must fallback to
`Extended STP/0`_.

In addition to checking the transport protocol version, it must also check the
core version of the host. If the host has core-2.4 or higher it means it
supports the new Unified Message Structure. This affects how the messages
are constructed, ie. names of fields and structure.

In short, the following setups will be encountered:

1. STP/1 and UMS
2. STP/0 and UMS formatted as JSON or XML, AKA `Extended STP/0`_
3. STP/0 and old XML structures (core-2.3 and lower)

Newer clients that do not need to consider backwards compatibility will only
need to support case #1.

Opera Dragonfly
---------------

Opera Dragonfly cannot control the transport protocol version that will be used
and must adhere to the message structure that will be in use. Opera Dragonfly
will need to read out the STP and core version and decide from that how
messages are to be formatted and parsed.

When it is possible, Opera Dragonfly will stick to JSON as the format for a message.
This would mean case #1 and #2 as described in the section Client_.

STP/1
=====

The new transport layer is defined as:

.. productionlist::
  connection: `services` `handshake` `messages`
  messages  : `message`*

This shows that the original STP/0 service list SERVICES is the first
entry to be sent. Next comes a handshake which results in the handshake
response `HANDSHAKE` followed by the actual transport messages.

The outer layer of the transport message is defined as:

.. productionlist::
  message : "STP" `stp_ver` `stp_size` `stp_data`
  stp_ver : <single octet>
  stp_size: `pb_uint_short`
  stp_data: <octets equal to stp-size>

This allows for multiple versions of a message to be sent. Each message is
uniquely identified by the string "STP" followed by a version number. The
size of the entire message is followed by the data of the message. This
allows any decoder to check the version and skip data that it does not
understand. The decoding of STP-DATA depends on the version.

An STP/1 message will look like:

.. productionlist::
  stp_one_message: "STP" "\x01" `stp_size` `stp_one_data`

In addition, it is now possible to pass STP/0 messages over the STP/1 protocol.
This is done by setting the STP-VER to 0 and then passing the STP/0 data.
The fields COUNT and SEPARATOR found in STP/0 will be skipped as the size is
already present in the STP/1 layer. This means we only transfer the KEYWORD
and DATA. An STP/0 message wrapped in STP/1 will look like:

.. productionlist::
  stp_zero_message: "STP" "\x00" `stp_size` `keyword` `terminator` <payload>

SERVICES
--------

The very first data sent by the host is a list of services.
This data is encoded in UTF-16-BE (UTF-16 Big Endian) and is the
same format as it was in STP/0. This ensures compatibility with older
clients:

.. productionlist::
  services     : `count` `terminator` "*services" `terminator` `service_list`
  service_list : `service` ["," `service`]+

HANDSHAKE
---------

The handshake is needed to agree on the STP version in use over a socket
connection. This is typically done between the host and the proxy as
well as between the proxy and the client. Each network connection can have a different
STP version in use, and any proxies will ensure that messages are routed according
to the STP version.
For instance, if a client that only supports STP/0 connects to a host supporting
STP/1 through a proxy, the proxy will take care of delivering STP/0 messages
over the STP/1 transport layer.

The side which receives the SERVICES message, aka the network client, must choose
a valid STP version from this list and initiate it.

The network client will then send an "\*enable" request with the specific
stp service which is defined as:

.. productionlist::
  handshake_req: "*enable" `terminator` "stp-" `version`
  version      : "0" | "1"
  handshake    : "STP/" `version` `newline`

The handshake request is encoded in STP/0, while the response is sent as plain
US-ASCII. For now there are only two versions to enable, STP/0 and STP/1.

Once the handshake is sent, the network client and network host must switch to
the specific STP version and parse and send messages in the specific format.

STP1-DATA
---------

For STP/1 messages STP-DATA is defined as:

.. productionlist::
  stp_one_data: `stp_one_type` `headers`
  stp_one_type: `pb_uint_short` # 1 = command, 2 = response, 3 = event, 4 = error
  headers     : <protocol buffer message>

STP1-TYPE represents which type of STP/1 message is found in the HEADERS
which is represented by the protocol buffer message TransportMessage.
The type tells what fields can be expected in the HEADERS, and maps to
a specific protocol buffer message.

The following types are defined:

========= =============
STP1-TYPE Proto message
========= =============
1         Command
2         Response
3         Event
4         Error
========= =============

Protocol buffer definition::

  enum STPType
  {
      COMMAND = 1;
      RESPONSE = 2;
      EVENT = 3;
      ERROR = 4;
  }

Other types can be added in the future, so any unknown type should be ignored
by clients and passed on by proxies.

HEADERS is a PB encoded message containing all the remaining fields for the
header. Any decoder must ignore fields it does not understand. Proxies must
also ensure these fields are transported to the client/host.

The headers are defined using a Protocol Buffer message::

    message TransportMessage
    {
      required string service = 1;
      required uint32 commandID = 2;
      required uint32 format = 3;
      optional uint32 status = 4;
      optional uint32 tag = 5;
      required bytes payload = 8;
    }

Some of the fields are optional and will be present depending on the type of
STP message. 

For commands the message will be::

    message Command
    {
      required string service = 1;
      required uint32 commandID = 2;
      required uint32 format = 3;
      required uint32 tag = 5;
      required bytes  payload = 8;
    }

For responses the message is defined as::

    message Response
    {
      required string service = 1;
      required uint32 commandID = 2;
      required uint32 format = 3;
      required uint32 tag = 5;
      required bytes  payload = 8;
    }

For events it looks like::

    message Event
    {
      required string service = 1;
      required uint32 commandID = 2;
      required uint32 format = 3;
      required bytes  payload = 8;
    }

For errors the message contains::

    message Error
    {
      required string service = 1;
      required uint32 commandID = 2;
      required uint32 format = 3;
      optional uint32 status = 4;
      optional uint32 tag = 5;
      required bytes  payload = 8;
    }

service
-------

The field `service` is the name of the service on the host as reported in
the initial `\*services` message.

commandID
---------

The field `commandID` is a number in the range of 0 to 2^32-1 and corresponds to a
given command in the specific service. The command value is unique only in the
specific service, and is guaranteed to stay the same for all future releases.

status
------

The field `status` is used to send information back to the client when errors
occur. This field is optional and is only sent when the STP1-TYPE is an
error message.

==== ==========================
Code Description
==== ==========================
0    OK
3    Bad Request
4    Internal Error
5    Command Not Found
6    Service Not Found
7    Out Of Memory (OOM)
8    Service Not Enabled
9    Service Already Enabled
==== ==========================

Protocol buffer definition::

  enum Status
  {
    OK = 0;
    BAD_REQUEST = 3;
    INTERNAL_ERROR = 4;
    COMMAND_NOT_FOUND = 5;
    SERVICE_NOT_FOUND = 6;
    OUT_OF_MEMORY = 7;
    SERVICE_NOT_ENABLED = 8;
    SERVICE_ALREADY_ENABLED = 9;
  }

Further details on the error can be read from the payload which uses this
structure::

    message ErrorInfo
    {
        optional string description = 1;
        optional sint32 line        = 2;
        optional sint32 column      = 3;
        optional sint32 offset      = 4;
    }

format
------

The field `format` is used to identify the format of the message body. This
also determines the encoding used on the message body.

=====  =====================  ========
Code   Description            Encoding
=====  =====================  ========
0      Protocol Buffer (UMS)  OCTET
1      JSON structures (UMS)  UTF-8
2      XML structures (UMS)   UTF-8
=====  =====================  ========

Protocol buffer definition::

  enum Format
  {
      PROTOCOL_BUFFER = 0;
      JSON = 1;
      XML = 2;
  }

tag
---

The field `tag` represents a synchronization value which is sent by the client to
bind the request to a response from the host. This field is only used when a
previous tag was sent from the client, so any events will not have this field.

The tag system will be part of the protocol API and provides a standardized
way of doing synchronization. The tag value can be read without knowledge of
the underlying format. This allows the proxy to properly filter responses back
to the correct client, and it also makes it easier for the clients to handle
responses since it can map the tag value to a response handler.

TAG is an unsigned integer in the range 0 to 2^31-1. The client is free to
reuse the Tag value as long as there is no current open requests using it.

payload
-------

The body (or payload) of the message depends on the `format` field but is always
sent in the `payload` field. This means that the payload can only be decoded
once the `format` has been found. Otherwise it must be treated as pure binary
data.

Message flow
============

Before the STP/1 message flow can start an initialization phase is needed.
This phase is performed between the two connecting parts. This would mean
between the host and proxy and the proxy to any clients. This phase
is used to determine the basic capabilites of the host, and to choose the
STP version to use for messages across all connected nodes.

When the client connects to a host or proxy it will receive a list of services.
Some of these services are meta-services and is used to determine capabilities
such as possible STP versions. For instance, the host might send back::

  *services scope,ecmascript-debugger,window-manager,stp-1,core-2-4

This reports back on the STP version available through the service "stp-1".
It also reports the core version in use, in this case core-2.4 ("core-2-4").

A set of examples follows of the message flow between a client, proxy,
and host. The following symbols are used::

  ~~~~~~~~~> Handshake
  ~ ~ ~ ~ ~> Handshake response
  ---------> Command
  - - - - -> Response
  =========> Event

The client must then initiate the handshake which also determines the STP
version to use, for instance to enable STP version 1::

  Host                              client
  
  *services     =================>
                <~~~~~~~~~~~~~~~~~  *enable stp-1
  STP/1\n       ~ ~ ~ ~ ~ ~ ~ ~ ~>
                <~~~~~~~~~~~~~~~~~  scope.Connect
  scope.Connect ~ ~ ~ ~ ~ ~ ~ ~ ~>

A typical message flow between a client, proxy and host looks like this::

  Opera                             proxy                   client
  
  handshake       <~~~~~~~~~~~~~~~~     ~ ~ ~ ~ ~ ~ ~ ~ ~>  handshake
                                        <-----------------  scope.Connect
  scope.Connect   <----------------
                  - - - - - - - - >
                                        - - - - - - - - ->  scope.Connect

  messages        <-------------------  - - - - - - - - ->  messages
  events          =======================================>
                                    ....
                                        <-----------------  scope.Disconnect
  scope.Disconnect<----------------
                  - - - - - - - - >
                                        - - - - - - - - ->  scope.Disconnect

If the client disconnects the socket without telling the host/proxy, then the
proxy will disconnect all clients on the given socket connection. For instance::

  scope.Disconnect <----------------  scope.Disconnect
                   - - - - - - - - >

A STP/0 client will initiate the message flow as described in
`Scope Transport Protocol`_.

Meta services
-------------

Meta services are sent along the regular service list to report back version
numbers and other useful information to the clients. This can then be used
to determine the capabilities of the transport layer and the host.
All meta services consist of a prefix followed by one or more values. This
means that the matching of meta services must be done on the prefix only.

The following meta services are defined:

STP versions are determined by the "stp-" meta service. The host will send
meta-service per version it supports. This means that the client must choose
among the reported versions and use one of them. If there is only one STP version
sent, then it means that another client has already decided which version to
use. The new client must then either start using the selected version or
disconnect if it does not support it.

The service is defined as:

.. productionlist::
  meta_stp: "stp-" `number`

Core version is determined by the "core-" meta service and contains the
core version after the prefix. This core version can be used to determine
the structure of the messages and how the services will act.
It is defined as:

.. productionlist::
  meta_core   : "core-" `dash_version`
  dash_version: `number` ("-" `number`)*

Extended STP/0
==============

When STP/0 is in use it will still use the Unified Message Structure for the
message content. The format will be restricted to XML and JSON as it
will require too much encoding overhead to binary protocols like the protocol
buffer into UTF-16BE.

The basics of the STP/0 transport is in sending a size, service
name and a payload. Only the size and service name is interesting for any
existing proxies (2.3 or lower). This means that it is possible to change
what the payload actually contains and let the receiver decode it.

The extended STP/0 transport will change the payload to contain the extra
fields required by an STP/1 message, but it will encoded to be compatible with
UTF-16BE. That is, it will be sent as pure text. The payload will consist of two
things: the STP/1 header and the real payload. The header can then be decoded
before the actual payload is sent to the next layer.

..
  terminator  : `space`
  count       : `number`
  keyword     : `command` | `service`
  command     : "*" `command_name`
  command_name: "services" | "enable" | "disable" | "quit" | "hostquit"
  service     : <any source character except ",">

Definition:

.. productionlist::
  stp         : `count` `terminator` "scope" `terminator` `data`
  data        : "STP/" `version` `terminator` `header_size` `terminator` `header` <payload>
  version     : `number`
  header_size : `number`
  header      : "[" `service_name` "," `stp_type` "," `command_id` "," `format` ["," `tag` ["," `status` ] ] "]"
  service_name: <json string>
  stp_type    : <json int>
  command-id  : <json int>
  format      : <json int>
  tag         : <json int>
  status      : <json int>

Messages must always be sent to the  "scope" service. This ensures that
there is only one service that needs to be enabled in the old proxies. This
means that a client must first enable the "scope" service by sending
"\*enable scope", or use the appropriate (DOM) API. This call will be ignored
by STP enabled hosts. After this is sent, the client must encode all outgoing
STP/1 messages according to the definition and send it to the "scope" service.
The host will recognize this extended format and decode as an STP/1 message.

