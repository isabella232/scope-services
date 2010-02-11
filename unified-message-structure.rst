===========================
 Unified Message Structure
===========================

:Author:  Jan Borsodi (jborsodi [at] opera.com)
:Version: 0.2
:Status:  Draft
:Date:    23th June 2009

Unified Message Structure, or UMS for short, is a system for defining message
structures in a generic format which can be exported to and imported from
multiple formats.

The main requirement for the system was to be able to work with XML, JSON and
Protocol Buffers. This is possible by defining a sub-set of all supported
formats.

In addition the system is also meant to assist with code-generation of parsers
and serializers for various languages, reducing the need for manually
crafted code.

The main component is the messages. They define a set of fields which make
up the message. Each field defines a specific type (integer or string)
and information on whether it is required, optional or repeated, in
addition to meta-information like name and a number.
The structure of the message is defined by the name and tag of each field
and the order of the fields.
Name is important for XML, tag is important for Protocol Buffers, and order is important for JSON.
The tag is a number which is unique to that field within each message. Tags
are defined in the range of 1 to (2^31)-1.
The name is a non-empty string written in camel-case.

A tool written in Python is available for dealing with UMS data:
http://bitbucket.org/scope/hob/


Types
=====

The types in the system are based upon the types in Protocol Buffers which
consist of a set of integer types, boolean, string and binary.
Nested messages are also possible with a special type called Message.

More details on types can be read in the `Protocol Buffer documentation`_.

.. _`Protocol Buffer documentation`: http://code.google.com/apis/protocolbuffers/docs/proto.html

.. note::
      Currently floating-point numbers are not supported due to the
      different nature of floating numbers between different processors.
.. note::
      64 bit types are not yet supported due to incomplete support for
      them in the Opera core.
.. note::
      Enums are not yet supported, should be easy as they are basically sent
      as numbers but require some extra handling in the generated code.

Quantifier
==========

.. todo::
      Find a better name for this?

The quantifier defines whether the field is required or not. If the field
is not required it can be defined as either optional or as being repeated.
A repeated field with zero elements and an optional field which is missing
are considered the same.

Style guide
===========

The style guide for services and all related elements are explained in
detail in in :doc:`style-guide-stp1`.

Syntax
======

The syntax for defining messages is based upon the Protocol Buffers syntax:
http://code.google.com/apis/protocolbuffers/docs/proto.html

.. note::
      Currently there is no parser for this, and everything is written in pure
      Python. A parser will be added once STP/1 and UMS stabilizes.

Supported formats
=================

UMS is designed to work with XML, JSON and Protocol Buffers. XML and JSON
are text-based formats while Protocol Buffers is an efficient binary format.

XML
---

XML is the least efficient format to use among the supported ones, and is
mainly kept as a way for getting output that is easy-to-read, for instance
for debugging or inspection.

Types
^^^^^

- All integer types are encoded/decoded as textual numbers. Size and signs are
  checked for when decoding numbers. For instance:

  .. code-block:: javascript

    0
    1
    -1
    65536

- *double* and *float* are encoded similar to integers but allows for
  fractions. For instance:

  .. code-block:: javascript

    0
    3.14
    -200.6

- *bool* is encoded/decoded as a textual number with **0** being **false** and **1** being
  **true**, other values are not allowed.
- *string* is encoded as UTF-8 XML text with XML entities for certain
  characters. For instance:

  .. code-block:: html

    Foo
    &lt;element&gt;

- *bytes* is encoded as UTF-8 XML text containing the base-64 representation
  of the binary data.

Structure
^^^^^^^^^

The name of the message is used in the root element of the XML_ structure.
Each field in the message is placed as a sub-element with the same name as the
field. If the field is optional and missing no element is made. It is the same with
repeated fields which are empty.

A message representing a *user*::

  message User {
    required int32  id = 1;
    required bool   isActive = 2;
    required string firstName = 3;
    required string lastName = 4;
    required float  height = 5;
    optional uint32 age = 6;
  }

would be encoded like this:

.. code-block:: xml

  <User>
    <id>42</id>
    <isActive>1</isActive>
    <firstName>John</firstName>
    <lastName>Doe</lastName>
    <height>1.80</height>
  </User>

For repeated fields the element also contains a sub-element for each item
in the repeated field, the name of the sub-element is taken from the field
name by removing the suffix *List*. This means that a field named *windowList*
will have sub-elements named *window*.

For instance representing a height map like this::

  message HeightMap {
    required uint32 width = 1;
    required uint32 height = 2;
    repeated int32  valueList = 3;
  }

would result in this:

.. code-block:: xml

  <HeightMap>
    <width>2</width>
    <height>2</height>
    <valueList>
     <value>1</value>
     <value>10</value>
     <value>7</value>
     <value>3</value>
    </valueList>
  </HeightMap>

The same is true for nested messages. Each *item* will contain the fields
for the sub-message::

  message PhoneBook {
    message PhoneNumber {
        required string number = 1;
        optional string extension = 2;
    }
    repeated PhoneNumber phoneNumberList = 1;
  }

would end up as:

.. code-block:: xml

  <PhoneBook>
    <phoneNumberList>
      <phoneNumber>
        <number>12345678</number>
        <extension>+47</extension>
      </phoneNumber>
      <phoneNumber>
        <number>555-768</number>
      </phoneNumber>
    </phoneNumberList>
  </PhoneBook>

JSON
----

JSON uses the order of the fields to pack messages into JSON lists. Lists
were chosen to cut down on the amount of information that is needed to send.

All integer types are encoded/decoded as textual numbers. Size and sign are
checked for when decoding numbers.
Boolean type is encoded/decoded as a textual number with 0 being false and
1 being true. Other values are not allowed.
Strings are encoded as UTF-8 JSON strings. 
Binary data is encoded as JSON strings containing the base-64 representation
of the binary data.
Messages are encoded as JSON lists with the order of the fields being kept.
Missing elements are sent as the null type. In addition, trailing elements
which are missing are cut off from the list.
Repeated types are encoded as JSON lists.

For more details on JSON see :rfc:`4627` or visit http://json.org

For instance this structure::

  message DummyData {
    required int32 id = 1;
    required string name = 2;
    repeated int32 fib = 3;
  }

Could be encoded like this:

.. code-block:: javascript

  [1,"foo",[1,1,2,3,5]]

Using more optional fields::

  message DummyData {
    required int32 id = 1;
    optional string name = 2;
    message SubData {
      required uint32 field1 = 1;
      optional uint32 field2 = 2;
      optional uint32 field3 = 3;
    }
    required SubData msg = 4;
  }

Could be encoded like this:

.. code-block:: javascript

  [1,null,[4]]

While this would be just as valid:

.. code-block:: javascript

  [1,null,[4,null,null]]

Protocol Buffers
----------------

PB is the most efficient way to transport data for languages that excel
at encoding/decoding binary data (e.g. C/C++). Other languages like JavaScript
and Python might be better off with using JSON.

PB is explained in detail at the main site:
http://code.google.com/apis/protocolbuffers/docs/overview.html

Code generation
===============

The system supports code generation of the message structures and encoders/
decoders.

C++
---

The C++ generator translates the message structures into C++ classes. This
allows C++ code to interact with messages using native structures. Encoding
and decoding is handled as a separate layer and is generated.

.. todo::
      More details on the generated C++ code.

.. note::
      We do not use the protoc compiler from Protocol Buffers since the
      generated code is not compatible with the limited C++ usage in
      the Opera core.

Javascript
----------

Code generation for JavaScript is designed around the fact that JavaScript code will
use JSON for formatting messages on the wire. This means that there
is little need for encoding/decoding of data. Extended code generation
is available when RPC (services) are in use.

To aid in debugging incoming JSON data the system can generate code that
outputs JSON data to a human-readable form.

Python
------

.. todo::
      Either use a similar style as JavaScript, or allow for proper classes
      to be made for the different messages.

Java
----

.. todo::
      Need to figure what is needed here for the various java projects.

.. XML: http://www.w3.org/XML/
