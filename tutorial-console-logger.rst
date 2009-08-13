========================================
Tutorial for a very basic console logger
========================================

It is recommended that you first read `How to setup a Test Environment for STP 1`_ and `Walk through the log entries`_. The tutorial will show how you can create a very simple console looger with the Opera scope interface. The console logger is a part of Opera which logs any type of errors which can occure during browsing and exposes them throgh the scope interface.

Create the files
================

To create a basic framework run ``opprotoc --js console-logger``. The argument ``console-logger`` specifies that we only want to create the console logger service. Without any argument it would create all services. ``scope`` and ``window-manager`` are always created. 

It will create in the current directory a new ``js-out`` repository. These are the created files:

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

Now we are ready to try it out. Start the Opera gogi build, the ``dragonkeeper`` proxy and open with any browser the created ``client.html`` as decribed in `How to setup a Test Environment for STP 1`_. You should see the following output in the console:

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

That shows that the client has connected successfully, requested the ``HostInfo`` and enabled the available services according to the response. 

Now we need to edit some files and write some code.

Edit window_manager.js
=========================

First we need to edit the ``window_manager.js``. This file contains a single class, the ``cls.WindowManager["2.0"].Service``. Each service has default notification events, ``on_enable_success``, ``on_window_filter_change``, ``on_quit``. As we can see in the log above the last messages are the confirmations that the enable command has succseeded. The framework tells that each service with the ``on_enable_success`` call. We implement this call as:

.. code-block:: javascript

  this.on_enable_success = function()
  {
    this.requestListWindows();
    this._window_filter = [1, [], ["*"]];
    this.requestModifyFilter(0, this._window_filter);
  };

``requestListWindows`` will return all windows or tabs of the host. This is not really necessary, but we would like to know all existing windows. This will allow us to separate the log messages per window. The response to that request is handled in ``handleListWindows``, we will look to that later.

Then we need to set a window filter. The ``window-manager`` service blocks all messages by default, or more precisely a given message is only created if it will pass the active filter. The filter we are using here is ``[1, [], ["*"]]``. The ``1`` is a boolean, representing ``true`` and indicates that the existing filter should be cleared. The next element is a list of window-ids to specify for which windows messages should be created. In our case it is empty. Following that is a list of rules. ``"*"`` means that messages shall be created for all windows.

The above filter is to get quickly something up and running. Normaly we are only interested in the messages of a specific window, e.g. the one with the document we are working one, all other messages should just not show up. But with the knowalege of this tutorial and the code in the test frame work ( see `Walk through the log entries`_ ) it should be possible to create your own application which will fit exactely your needs.

We can now now run again ``client.html``. There should be now some more entries:

.. code-block:: none

  send to host:
    message type: command
    service: window-manager
    command: ListWindows
    format: json
    tag: 0
    payload: []

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
    command: ListWindows
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: [[[1,"Opera Portal BETA","normal",0],[2,"About Opera","normal",0],[8,"Connect to Debugger","normal",0],[13,"O
  pera Developer Community","normal",0],[18,"GOGI Dialog","dialog",0]]]

  send to client:
    message type: response
    service: window-manager
    command: ModifyFilter
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: []

  send to client:
    message type: event
    service: window-manager
    command: OnWindowClosed
    format: json
    status: OK
    cid: 1
    tag: 0
    payload: [18]

If you now type in the addressfield of the Opera gogi build for example:

::

  javascript:void(opera.postError("hello world"))

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


This code is actually enough to get the messages of the ``console-logger``. If you are running ``dragonkeeper`` with the ``d`` and ``f`` flag you will see the messages in the shell console.

To display the messages in the browser we need to write a bit more code. The following code creates for each window a container and adds the title of the current top document of that window.

.. code-block:: javascript

  this.display_window_title = function(win)
  {
    const 
    WINDOW_ID = 0, 
    TITLE = 1;
       
    var container = document.getElementById('window-id-' + win[WINDOW_ID]);
    if (!container)
    {
      container = document.body.appendChild(document.createElement('div'));
      container.id = 'window-id-' + win[WINDOW_ID];
    }
    container.appendChild(document.createElement('h2')).textContent = win[TITLE];
  }

We use this method to handle messages in the ``handleListWindows`` response handler and in the ``onWindowUpdated`` event like this:

.. code-block:: javascript

  this.handleListWindows = function(status, message)
  {
    const WINDOW_LIST = 0;
    message[WINDOW_LIST].forEach(this.display_window_title);
  }
  
  this.onWindowUpdated = function(status, message)
  {    
    this.display_window_title(message);
  }

So far we have achieved a console-logger that will create error messages for all windows and we have created a basic HTML document structure for each window. Now we need to edit ``console_logger.js``.

Edit console_logger.js
======================

``onConsoleMessage`` is the only method of the ``console-logger`` service. We implement it as:

.. code-block:: javascript

  this.onConsoleMessage = function(status, message)
  {
    const
    WINDOW_ID = 0,
    TIME = 1,
    DESCRIPTION = 2,
    URI = 3,
    CONTEXT = 4,
    SOURCE = 5,
    SEVERITY = 6;
       
    var container = document.getElementById('window-id-' + message[WINDOW_ID]);
    if (!container)
    {
      container = document.body.appendChild(document.createElement('div'));
      container.id = 'window-id-' + message[WINDOW_ID];
    }
    var pre = container.appendChild(document.createElement('pre'));
    pre.textContent = new Date(message[TIME]) + '\n' + 
      "source: " + message[SOURCE] + '\n' + 
      "uri: " + message[URI] + '\n' + 
      "context: " + message[CONTEXT] + '\n' +
      "severity: " + message[SEVERITY] + '\n' +
      message[DESCRIPTION];
    pre.scrollIntoView();
  }

That means we are using the document structure which is created by the ``window-manager`` and display any information of the message in a preserved text block.

This is our very basic ``console-logger``. It should be easy to extend it from here to your own needs.



.. _How to setup a Test Environment for STP 1: walk-through.html
.. _Walk through the log entries: walk-through.html




  
