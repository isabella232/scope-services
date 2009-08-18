========================================
Tutorial for a very basic console logger
========================================

It is recommended that you first read `How to setup a Test Environment for STP 1`_ and `Walk through the log entries`_. The tutorial will show how you can create a very simple console logger with the Opera scope interface. The console logger is a part of Opera which logs any type of errors which can occur during browsing and exposes them through the scope interface.

Create the files
================

To create a basic framework run ``opprotoc --js console-logger``. The argument ``console-logger`` specifies that we only want to create the console logger :term:`service`. Without any argument it would create all services. ``scope`` and ``window-manager`` are always created. 

That creates in the current directory a new ``js-out`` repository. These are the created files:

::

  client.html
  build_application.js  
  client.js  
  console_logger.js 
  scope.js  
  window_manager.js
  helper_const_ids.txt
  lib/
    clientlib_async.js 
    http_interface.js
    interface_console_logger.js  
    interface_scope.js
    interface_window_manager.js
    json.js 
    namespace.js
    service_base.js
    stp_0_wrapper.js   
    tag_manager.js

Only files in the relative root should be edited. In short, the files contain:

client.html
  The main document.

build_application.js  
  To build the application. Any instantiation happens here.

client.js  
  Definition of the client class.

console_logger.js, scope.js, window_manager.js
  Implementations of the services. These files are the starting points to create your own application.

helper_const_ids.txt
  A helper file to copy-paste constants for all services and messages.

lib/clientlib_async.js 
  Convenience library for interacting with the scope proxy.

lib/http_interface.js
  Implementation of the scope DOM API as an HTTP interface.

lib/interface_console_logger.js  

lib/interface_scope.js

lib/interface_window_manager.js
  Definitions of the services with documentation of the messages.

lib/json.js 
  Implementation of JSON in Javascript.

lib/namespace.js
  To register instantiated objects in a given namespace.

lib/service_base.js
  The basic interface of any service.

lib/stp_0_wrapper.js   
  Re-implements the scope DOM API on top of a STP/0 protocol STP/1 compatible (e.g. if the proxy in the middle only talks STP/0).

lib/tag_manager.js
  To handle responses to request individually, separated of the default response handlers.

Now we are ready to try it out. Start the Opera gogi build, the ``dragonkeeper`` proxy and open with any browser the created ``client.html`` as described in `How to setup a Test Environment for STP 1`_. You should see the following output in the console:

.. code-block:: none

  services available:
    scope
    console-logger
    ecmascript-logger
    http-logger
    exec
    window-manager
    url-player
    ecmascript-debugger
    core-2-4
    stp-0
    stp-1

  send to scope: *enable stp-1
  send to host:
    message type: command
    service: scope
    command: Connect
    format: json
    uuid: 1250186862378
    tag: 0
    payload: ["json","1250186862378"]

  client connected:
    message type: response
    service: scope
    command: Connect
    format: json
    status: OK
    cid: 1
    uuid: 1250186862378
    tag: 0
    payload: [1]

  send to host:
    message type: command
    service: scope
    command: HostInfo
    format: json
    tag: 0
    payload: []

  send to client:
    message type: response
    service: scope
    command: HostInfo
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: [1,"2.4","WinGogi","WinGogi","Opera/9.70 (WinGogi; U; en) Presto/2.3.0",[["scope","1.0.0",0,1],["console-logg
  er","1.0.0",0,1],["ecmascript-logger","1.0.0",0,1],["http-logger","1.0.0",0,1],["exec","1.0.0",0,1],["window-manager","1
  .0.0",0,1],["url-player","1.0.0",0,1],["ecmascript-debugger","1.0.0",0,1],["core-2-4","1.0.0",0,1],["stp-0","1.0.0",0,1]
  ,["stp-1","1.0.0",0,1]]]

  send to host:
    message type: command
    service: scope
    command: Enable
    format: json
    tag: 0
    payload: ["console-logger"]

  send to host:
    message type: command
    service: scope
    command: Enable
    format: json
    tag: 0
    payload: ["window-manager"]

  send to client:
    message type: response
    service: scope
    command: Enable
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: ["console-logger"]

  send to client:
    message type: response
    service: scope
    command: Enable
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: ["window-manager"]

There are three points where we can hook up to this process:

* the load event
* a frame work specific ``on_services_created`` event
* an other frame work specific ``on_services_enabled`` event

The load event callback is defined in ``build_application.js`` at the bottom:

.. code-block:: javascript

  window.onload = function()
  {
    window.app.build_application();
  }

The ``window.app.build_application`` call creates default objects, setups the connection with the :term:`host`, requests the ``HostInfo`` and enables the available services according to the response as shown in the log above. 

A callback for the ``on_services_created`` event can be passed as first argument to the ``build_application`` call or it can be defined in the ``app`` namesapce as:

.. code-block:: javascript

  window.app.on_services_created = function(service_descriptions)
  {
    
  }

As the name suggests this event gets dispatched after all services are build but not jet enabled. It has as argument the ``service_descriptions`` of the of the ``HostInfo`` message.

A callback for the ``on_services_enabled`` event can be passed as second argument to the ``build_application`` call or it can be defined in the ``app`` namesapce as:

.. code-block:: javascript

  window.app.on_services_enabled = function()
  {

  }

Write the SimpleConsolLogger class
==================================

Now we can start to create our console logger in e.g. ``simpleconsolelogger.js``. We make a simple class like:

.. code-block:: javascript

  var SimpleConsolLogger = function()
  {

    this.setup = function()
    {

    }

  }

We instantiate and setup it in the ``build_application.js`` by adding the following code at the bottom of the file:

.. code-block:: javascript

  window.onload = function()
  {
    window.app.build_application();
    window.simple_consol_logger = new SimpleConsolLogger();
  }
   
  window.app.on_services_enabled = function()
  {
    window.simple_consol_logger.setup();
  }

The ``window.onload`` callback was already there. We instantiate our class here because it does not depend in any way on the created services. We define the ``window.app.on_services_enabled`` callback and add the ``setup`` call to our ``simple_consol_logger`` here.

As mentioned before ``scope`` and ``window-manager`` services are created always. They are special. 


``scope`` and ``window-manager`` services
-----------------------------------------

``scope`` is a system service to setup the connection with the host and to control the other services. Normally you will not have to interact with this service directly.

``window-manger`` gets events about all changes regarding windows or tabs and can also query general informations about them. It also controls the messages for all other services. By default it blocks all messages, or more precisely a given message is only created if it will pass the active filter. That is the reason that we first must set a filter to define which messages shall be created. 

set a window filter
-------------------

We do that in the ``setup`` call of our ``SimpleConsoleLogger`` class like:

.. code-block:: javascript

  this.setup = function()
  {
    window_manager.requestModifyFilter(0, [1, [], ['*']]);
  }

The filter we are using here is ``[1, [], ["*"]]``. The ``1`` is a boolean, representing ``true`` and indicates that the existing filter should be cleared. The next element is a list of window-ids to specify for which windows messages should be created. In our case it is empty. Following that is a list of rules. ``"*"`` means that messages shall be created for all windows.


.. topic:: Sidenote

  That filter is to get quickly something up and running. Normally we are only interested in the messages of a specific window, e.g. the one with the document we are working one, all other messages should just not show up. But with the knowledge of this tutorial and the code in the test frame work ( see `Walk through the log entries`_ ) it should be possible to create your own application which will fit exactely your needs.

We can now run again ``client.html``. There should be some more entries:

.. code-block:: none

  send to host:
    message type: command
    service: window-manager
    command: ModifyFilter
    format: json
    tag: 0
    payload: [1,[],["*"]]

  send to client:
    message type: response
    service: window-manager
    command: ModifyFilter
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: []

If you now type in the address field of the Opera gogi build for example:

::

  javascript:opera.postError("hello world")

you should see the according message in the console:

.. code-block:: none

  send to client:
    message type: event
    service: console-logger
    command: OnConsoleMessage
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: [8,1250183583,"hello world","","Javascript URL thread: \"javascript:void(opera.postError(\"hello world\"))\""
  ,"ecmascript","information"]

get all windows
---------------

The service interfaces are build around messages. A message can either be an event, a command or a response to a command. All messages for the ``window-manager`` are specified `here`_. 

A command is exposed in the framework as ``window.<service name>.request<command class>(tag, message)``. 

A callback to handle the response can be registered in the ``tag_manager``. That requires that the according ``tag`` was passed in the request call. 

A default request handler can be implemented as ``window.<service name>.handle<command class>(status, message)``. These methods will only get called if the ``tag_manager`` has not an according ``tag`` registered. By default all these methods yield an error warning if the according handlers are not implemented.

We like to sort out in our simple console logger the messages per window. For that reason we use the ``ListWindows`` command and the ``OnWindowUpdated`` event of the ``window-manager`` service.

We implement them in our class like:

.. code-block:: javascript

  var SimpleConsolLogger = function()
  {
   
    var _get_container = function(window_id)
    {
      var container = document.getElementById('window-id-' + window_id);
      if (!container)
      {
        container = document.body.appendChild(document.createElement('div'));
        container.id = 'window-id-' + window_id;
      }
      return container;
    }
   
    var _display_window_title = function(win)
    {
      const WINDOW_ID = 0, TITLE = 1;
      _get_container(win[WINDOW_ID]).
        appendChild(document.createElement('h2')).textContent = win[TITLE];
    }
   
    this.setup = function()
    {
      var window_manager = window.services['window-manager'];
      window_manager.handleListWindows = function(status, message)
      {
        const WINDOW_LIST = 0;
        message[WINDOW_LIST].forEach(_display_window_title);
      }
      window_manager.onWindowUpdated = function(status, message)
      {
        _display_window_title(message);
      }
      window_manager.requestListWindows();
      window_manager.requestModifyFilter(0, [1, [], ['*']]);
    }
   
  }

``_get_container`` is a helper function which ensures that there is always a container with the passed window id and returns that container.

``_display_window_title`` is a function to display the title of a window in the according container, using the ``_get_container`` helper.

The implementation of the ``handleListWindows`` request handler and the ``onWindowUpdated`` event is done in the ``setup`` call. We can open ``window_manager.js`` and search for ``handleListWindows``. The according code looks like:

.. code-block:: javascript

  this.handleListWindows = function(status, message)
  {
    const
    WINDOW_LIST = 0,
    /* sub message WindowInfo */
    WINDOW_ID = 0,
    TITLE = 1,
    WINDOW_TYPE = 2,
    OPENER_ID = 3;
 
    // implement the handling of the message here
    opera.postError("NotImplementedError: WindowManager, ListWindows, " +
              "message: " + JSON.stringify(message) );
  }

Here is the default error warning dispatched in the case of a missing implementation. We also see all the constants to read the message. For our implementation we need only ``const WINDOW_LIST = 0;`` to get the actual list of windows from the message. We pass each window object to our ``_display_window_title`` method.

We can search in the same file for ``onWindowUpdated``. That code looks like:

.. code-block:: javascript

  this.onWindowUpdated = function(status, message)
  {
    const
    WINDOW_ID = 0,
    TITLE = 1,
    WINDOW_TYPE = 2,
    OPENER_ID = 3;
 
    // implement the handling of the message here
    opera.postError("NotImplementedError: WindowManager, OnWindowUpdated, " +
              "message: " + JSON.stringify(message));
  }

We see again the default warning. The message represents a single window. So we can pass the message directly to our ``_display_window_title`` method.

If we now run ``client.html`` again we should see all the titles of all the tabs in the :term:`client`.


Implement the ``OnConsoleMessage`` event
----------------------------------------

Now we only need to implement the ``OnConsoleMessage`` event handler of the ``console-logger`` service. We do that in the ``setup`` call like:

.. code-block:: javascript

    window.services['console-logger'].onConsoleMessage = function(status, message)
    {
      const
      WINDOW_ID = 0,
      TIME = 1,
      DESCRIPTION = 2,
      URI = 3,
      CONTEXT = 4,
      SOURCE = 5,
      SEVERITY = 6;
 
      var pre = _get_container(message[WINDOW_ID]).appendChild(document.createElement('pre'));
      pre.textContent = new Date(message[TIME]) + '\n' +
        "source: " + message[SOURCE] + '\n' +
        "uri: " + message[URI] + '\n' +
        "context: " + message[CONTEXT] + '\n' +
        "severity: " + message[SEVERITY] + '\n' +
        message[DESCRIPTION];
      pre.scrollIntoView();
    }

We can search as before in ``console_logger.js`` for ``onConsoleMessage``. This time we use all of the constant identifiers. We get the according container with our helper function and display all available information in a preserved text block. Then we scroll the new created text block into view.

If we reload ``client.html`` and type again in the address field of the Opera gogi build:

::

  javascript:opera.postError("hello world") 

we should see the according message in our client.

The whole class looks now:

.. code-block:: javascript

  var SimpleConsolLogger = function()
  {
   
    var _get_container = function(window_id)
    {
      var container = document.getElementById('window-id-' + window_id);
      if (!container)
      {
        container = document.body.appendChild(document.createElement('div'));
        container.id = 'window-id-' + window_id;
      }
      return container;
    }
   
    var _display_window_title = function(win)
    {
      const WINDOW_ID = 0, TITLE = 1;
      _get_container(win[WINDOW_ID]).
        appendChild(document.createElement('h2')).textContent = win[TITLE];
    }
   
    this.setup = function()
    {
      var window_manager = window.services['window-manager'];
      window_manager.handleListWindows = function(status, message)
      {
        const WINDOW_LIST = 0;
        message[WINDOW_LIST].forEach(_display_window_title);
      }
      window_manager.onWindowUpdated = function(status, message)
      {
        _display_window_title(message);
      }
      window.services['console-logger'].onConsoleMessage = function(status, message)
      {
        const
        WINDOW_ID = 0,
        TIME = 1,
        DESCRIPTION = 2,
        URI = 3,
        CONTEXT = 4,
        SOURCE = 5,
        SEVERITY = 6;
   
        var pre = _get_container(message[WINDOW_ID]).appendChild(document.createElement('pre'));
        pre.textContent = new Date(message[TIME]) + '\n' +
          "source: " + message[SOURCE] + '\n' +
          "uri: " + message[URI] + '\n' +
          "context: " + message[CONTEXT] + '\n' +
          "severity: " + message[SEVERITY] + '\n' +
          message[DESCRIPTION];
        pre.scrollIntoView();
      }
      window_manager.requestListWindows();
      window_manager.requestModifyFilter(0, [1, [], ['*']]);
    }
   
  }
 

We can add minimal style in ``client.html`` to separate the log messages with e.g. something like:

:: 

  <style> pre { border-bottom: 1px solid #999; padding-bottom: 1em; } </style>


This is our very basic ``console-logger``. It should be easy to extend it from here to your own needs.

You can run ``opprotoc --js --console-logger-tutorial console-logger`` to generate all code described in the tutorial as part of the default framework.



.. _How to setup a Test Environment for STP 1: walk-through.html
.. _Walk through the log entries: walk-through.html
.. _here: WindowManager.html

