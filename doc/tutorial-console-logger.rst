==============================================
Tutorial for a very basic error message logger
==============================================

It is recommended that you first read `How to setup a Test Environment for STP 1`_ and `Walk through the log entries`_. The tutorial will show you how you can create a very simple error message logger with the Opera Scope interface. We will use for that the ``ConsoleLogger`` :term:`service`, the part of the Scope interface which exposes any type of errors and warnings which can occur during browsing.

Scope exposes an interface to an Opera instance. More detailed it looks like:

.. raw:: html
  
  <div class="illustration">
    <p class="main">Opera Host
    <p>Scope
    <p>UMS
    <p class="optional">STP/1
    <p class="optional">(Standalone) Proxy
    <p class="optional">HTTP Interface 
    <p>DOM API
    <p>Service API
    <p class="main">Opera Client
  </div>

The layers with a question mark exist only if they are really needed. For example in a debug session on desktop, where the :term:`client` and :term:`host` are the same instance, the UMS layer is bound directly to the DOM API, no socket connection is created. Similarly remote debugging with the Opera built-in proxy does not use an HTTP interface. For more details see `Scope Interface Version 1`_.

The DOM API is, like any good API, small. Normally it is a native part of Opera, exposed to a privileged window. It can be implemented in ECMAScript on top of an HTTP interface to a standalone proxy. The main methods are ``scopeTransmit(service: string, message: datastructure|string, command: integer, tag: integer)`` and the ``receive(service: string, message: datastructure|string, command: integer, status: integer, tag: integer)`` callback of ``scopeAddClient``. For more details about the API see `Scope DOM API`_.

The service API unfolds the DOM API to different services. They are counterparts of the according services on the host side and expose there interface as an ECMAScript API. They are part of the basic framework which is generated with ``hob``, a code generation command line utility. For more details about ``hob`` see `How to setup a Test Environment for STP 1`_.

It is of course also possible to work directly with the DOM API, the service API layer is in this regard only a convenience.

Create the files
================

To create a basic framework run ``hob js --js-test-framework ConsoleLogger Scope WindowManager`` inside the scope-services repository. The argument ``ConsoleLogger`` specifies that we only want to create the ``ConsoleLogger`` :term:`service`. Without any argument it would create all services. ``Scope`` and ``WindowManager`` are required.

That creates in the current directory a new ``js-out`` repository. These are the created files:

::

  client.html
  build_application.js
  client.js
  lib/
    clientlib_async.js  
    http_interface.js  
    messages.js   
    scope.js         
    stp_0_wrapper.js  
    window_manager.js
    console_logger.js   
    json.js            
    namespace.js  
    service_base.js  
    tag_manager.js

Only files in the relative root should be edited. In short, the files contain:

client.html
  The main document.

build_application.js
  To build the application. Any instantiation happens here.

client.js
  Definition of the client class.

lib/console_logger.js, lib/scope.js, lib/window_manager.js
  The service APIs to bind your application to the Scope interface with documentation links and constant identifiers to handle messages.

lib/clientlib_async.js
  Convenience library for interacting with the Scope proxy.

lib/http_interface.js
  Implementation of the Scope DOM API as an HTTP interface.

lib/json.js
  Implementation of :term:`JSON` in ECMAScript.

lib/namespace.js
  To register instantiated objects in a given namespace.

lib/messages.js
  A message broker singleton for framework specific events.

lib/service_base.js
  The abstract base class for any service.

lib/stp_0_wrapper.js
  Re-implements the Scope DOM API on top of a :term:`STP/0` protocol :term:`STP/1` compatible (e.g. if the proxy in the middle only talks STP/0).

lib/tag_manager.js
  To handle responses to request individually, separated of the default response handlers.

Now we are ready to try it out:

* Open the ``dragonkeeper`` proxy: ``dragonkeeper -dfr <path>`` (or ``python -m dragonkeeper.dragonkeeper -dfr <path-to-js-out>`` if you have not installed the module).
* Start a recent Opera build and connect to ``dragonkeeper`` through opera:debug
* In a browser, open the created ``client.html``: http://localhost:8002/client.html

See `How to setup a Test Environment for STP 1`_ for details on the setup. You should see the following output in the ``dragonkeeper`` console window:

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

This log documents that the client connects to the host, requests the ``HostInfo`` and enables the required services. 

This happens as part of the building process of the client application. There are three points where we can hook up to it:

* the load event
* a framework specific ``services-created`` event
* another framework specific ``services-enabled`` event

The load event callback is defined in ``build_application.js`` at the bottom:

.. code-block:: javascript

  window.onload = function()
  {
    window.app.build_application();
  }

The ``window.app.build_application`` call creates default objects, setups the connection with the :term:`host`, requests the ``HostInfo`` and enables the available services according to the response as shown in the log above.

A callback for the ``services-created`` event can be passed as first argument to the ``build_application`` call. ``window.app`` has also the method ``addListener`` to register callbacks for this event:

.. code-block:: javascript

  window.app.addListener('services-created', function(msg){});

The event gets dispatched after all services are built but not yet enabled. The ``msg`` has a property ``service_descriptions`` with the ``service_descriptions`` of the ``HostInfo`` :term:`message`.

A callback for the ``services-enabled`` event can be passed as second argument to the ``build_application`` call or it can be registered as above:

.. code-block:: javascript

  window.app.addListener('services-enabled', function(msg){});

Write the SimpleLogger class
============================

Now we can start to create our logger in for example ``simpleconsolelogger.js``. You will have to create that file and add a script tag in ``client.html`` like:

.. code-block:: html

  <script src="simpleconsolelogger.js"></script>

We make a simple class in the new file like:

.. code-block:: javascript

  var SimpleLogger = function()
  {

  }

We instantiate it in the ``build_application.js`` by adding the following code at the bottom of the file:

.. code-block:: javascript

  window.onload = function()
  {
    window.app.build_application();
    window.simple_logger = new SimpleLogger();
  }

The ``window.onload`` callback was already there. We add the instantiation of our class here.

.. topic:: Sidenote

  The hookup in the application building process is done here in the most simple way. Depending on your needs there is a more advanced way with ``window.app.builders`` and event callbacks per service object. For details see the comments in ``build_application.js`` and the common methods of all services in ``service_base.js``.

As mentioned before, the ``Scope`` and ``WindowManager`` services are always created. They are special.


``Scope`` and ``WindowManager`` services
-----------------------------------------

``Scope`` is a system service to setup the connection with the host and to control the other services. Normally you will not have to interact with it directly.

``WindowManager`` gets events about all changes regarding windows or tabs and can also query general information about them. It also controls the messages for all other services. By default it blocks all messages, or, more precisely, a given :term:`message` is only created if it will pass the active filter. That is the reason that we must first set a filter to define which messages shall be created.

Set a window filter
-------------------

We do that by setting a callback for the ``services-enabled`` event in our ``SimpleLogger`` class like:

.. code-block:: javascript

  window.app.addListener('services-enabled', function(msg)
  {
    window.services['window-manager'].requestModifyFilter(0, [1, [], ['*']]);
  });

The filter we are using here is ``[1, [], ["*"]]``. The ``1`` is a number, representing the boolean ``true`` and indicates that the existing filter should be cleared. The next element is a list of window-ids to specify for which windows messages should be created. In our case it is empty. Following that is a list of rules. ``"*"`` means that messages shall be created for all windows.


.. topic:: Sidenote

  This specific filter is used to get something up and running quickly. Normally we are only interested in the messages from a specific window, for example the one with the document we are working on. All other messages should just not show up. But with the knowledge from this tutorial and the code in the test framework (see `Walk through the log entries`_) it should be possible to create an application which will fit your needs better.

We can now reload ``client.html``. There should be some more entries:

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

If you now for example type the following in the address field of the Opera Gogi build:

::

  javascript:opera.postError("hello world")

you should see the according message in the ``dragonkeeper`` console window:

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

Get all windows
---------------

The service interfaces are build around messages. A message can either be an event, a command, a response to a command, or an error. A command is sent from the client to the host, the others the other way around. All messages for the ``window-manager`` are specified `here`_.

A command is exposed in the framework as ``window.services[<service name>].request<command name>(tag, message)``.

A callback to handle the response can be registered in the ``tag_manager``. That requires that the respective ``tag`` was passed in the request call.

A default request handler can be implemented as ``window.services[<service name>].handle<command name>(status, message)``. These methods will only get called if the ``tag_manager`` does not have an according ``tag`` registered. By default all these methods yield a warning if the according handlers are not implemented.

An event is exposed as ``window.services[<service name>].<event name>(status, message)``. It has the same rules as a response handler.

We would like to sort the messages per window in our simple logger. To do that, we use the ``ListWindows`` command and the ``OnWindowUpdated`` event of the ``window-manager`` service. The ``OnWindowUpdated`` event is dispatched when a new window or tab is opened or the main document of an existing window changes so that the window gets a new title.

We implement them in our class as follows:

.. code-block:: javascript

  var SimpleLogger = function()
  {

    var _get_or_create_container = function(window_id)
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
      _get_or_create_container(win[WINDOW_ID]).
        appendChild(document.createElement('h2')).textContent = win[TITLE];
    }

    // service API bindings

    window.services['window-manager'].handleListWindows = function(status, message)
    {
      const WINDOW_LIST = 0;
      message[WINDOW_LIST].forEach(_display_window_title);
    }

    window.services['window-manager'].onWindowUpdated = function(status, message)
    {
      _display_window_title(message);
    }

    // 'services-enabled' event listener

    window.app.addListener('services-enabled', function(msg)
    {
      window.services['window-manager'].requestListWindows();
      window.services['window-manager'].requestModifyFilter(0, [1, [], ['*']]);
    });

  }

``_get_or_create_container`` is a helper function which ensures that there is always a container with the passed window id and returns that container.

``_display_window_title`` is a function to display the title of a window in the according container, using the ``_get_or_create_container`` helper.

The binding of the ``handleListWindows`` response handler and the ``onWindowUpdated`` event is done directly in our class. We can open ``lib/window_manager.js`` and search for ``handleListWindows``. The according code:

.. code-block:: javascript

  this.handleListWindows = function(status, message)
  {
    /*
    const
    WINDOW_LIST = 0,
    // sub message WindowInfo 
    WINDOW_ID = 0,
    TITLE = 1,
    WINDOW_TYPE = 2,
    OPENER_ID = 3;
    */
    opera.postError("NotBoundWarning: WindowManager, ListWindows");
  }

Here is the default error warning dispatched in the case of a missing binding. We also see all the constants to read the message. For our implementation we need only ``const WINDOW_LIST = 0;`` to get the actual list of windows from the message. We pass each window object to our ``_display_window_title`` method. Above is the implementation of the according request call and the url `http://dragonfly.opera.com/app/scope-interface/WindowManager.html#listwindows`_, linking to the the documentation of the whole command.

We can search in the same file for ``onWindowUpdated``. The code:

.. code-block:: javascript

  this.onWindowUpdated = function(status, message)
  {
    /*
    const
    WINDOW_ID = 0,
    TITLE = 1,
    WINDOW_TYPE = 2,
    OPENER_ID = 3;
    */
    opera.postError("NotBoundWarning: WindowManager, OnWindowUpdated");
  }

We see again the default warning. The message represents a single window. So we can pass the message directly to our ``_display_window_title`` method as it is done with:


.. code-block:: javascript

    window.services['window-manager'].onWindowUpdated = function(status, message)
    {
      _display_window_title(message);
    }

in our ``SimpleLogger``.

If we now reload ``client.html`` again we should see all the titles of all the tabs in the :term:`client`.


Implement the ``OnConsoleMessage`` event
----------------------------------------

Now we only need to implement the ``OnConsoleMessage`` event handler of the ``ConsoleLogger`` service. We do that by adding the following code:

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

      var pre = _get_or_create_container(message[WINDOW_ID]).appendChild(document.createElement('pre'));
      pre.textContent = new Date(message[TIME]) + '\n' +
        "source: " + message[SOURCE] + '\n' +
        "uri: " + message[URI] + '\n' +
        "context: " + message[CONTEXT] + '\n' +
        "severity: " + message[SEVERITY] + '\n' +
        message[DESCRIPTION];
      pre.scrollIntoView();
    }

We can search as before in ``lib/console_logger.js`` for ``onConsoleMessage``. This time we use all of the constant identifiers. We get the according container with our helper function and display all available information in a preserved text block. Then we scroll the new created text block into view.

If we reload ``client.html`` and type again in the address field of the Opera Gogi build:

::

  javascript:opera.postError("hello world")

we should see the according message in our client.

The whole class looks now:

.. code-block:: javascript

  var SimpleLogger = function()
  {
   
    var _get_or_create_container = function(window_id)
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
      _get_or_create_container(win[WINDOW_ID]).
        appendChild(document.createElement('h2')).textContent = win[TITLE];
    }
   
    // service API bindings

    window.services['window-manager'].handleListWindows = function(status, message)
    {
      const WINDOW_LIST = 0;
      message[WINDOW_LIST].forEach(_display_window_title);
    }

    window.services['window-manager'].onWindowUpdated = function(status, message)
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

      var pre = _get_or_create_container(message[WINDOW_ID]).appendChild(document.createElement('pre'));
      pre.textContent = new Date(message[TIME]) + '\n' +
        "source: " + message[SOURCE] + '\n' +
        "uri: " + message[URI] + '\n' +
        "context: " + message[CONTEXT] + '\n' +
        "severity: " + message[SEVERITY] + '\n' +
        message[DESCRIPTION];
      pre.scrollIntoView();
    }

    // 'services-enabled' event listener

    window.app.addListener('services-enabled', function(msg)
    {
      window.services['window-manager'].requestListWindows();
      window.services['window-manager'].requestModifyFilter(0, [1, [], ['*']]);
    });
   
  }


We can add minimal style in ``client.html`` to separate the log messages with e.g. something like:

.. code-block:: html

  <style> pre { border-bottom: 1px solid #999; padding-bottom: 1em; } </style>


This is our very basic ``console-logger``. It should be easy to extend it from here to your own needs.

.. topic:: Sidenote

  If you open or close a tab in the host you will see the following errors in the error console of the client:

  ::

    JavaScript
    Unknown thread
    NotBoundWarning: WindowManager, OnWindowClosed

    JavaScript
    Unknown thread
    NotBoundWarning: WindowManager, OnWindowActivated

  This is because we have only bound the messages which we need for our simple logger. If you like to get rid of these warnings, you could add something like the following:

  .. code-block:: javascript

    window.services['window-manager'].onWindowClosed = 
    window.services['window-manager'].onWindowActivated = 
    function(status, message){};

  This is an explicit statement that we will not handle these events.




  

You can run ``hob js --console-logger-tutorial ConsoleLogger Scope WindowManager`` to generate all code described in the tutorial as part of the default framework.



.. _How to setup a Test Environment for STP 1: walk-through.html
.. _Walk through the log entries: walk-through.html
.. _here: WindowManager.html
.. _Scope Interface Version 1: index.html#scope-interface-version-1
.. _Scope DOM API: scope-dom-interface.html
.. _http://dragonfly.opera.com/app/scope-interface/WindowManager.html#listwindows: http://dragonfly.opera.com/app/scope-interface/WindowManager.html#listwindows

