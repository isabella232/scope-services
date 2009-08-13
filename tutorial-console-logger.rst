========================================
Tutorial for a very basic console logger
========================================

It is recommended that you first read `How to setup a Test Environment for STP 1`_ and `Walk through the log entries`_.

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

Edit window_manager.js
=========================

First we need to edit the ``window_manager.js``. Each service has default notification events, ``on_enable_success``, ``on_window_filter_change``, ``on_quit``. We implement ``on_enable_success`` as:

.. code-block:: javascript

  this.on_enable_success = function()
  {
    this.requestListWindows();
    this._window_filter = [1, [], ["*"]];
    this.requestModifyFilter(0, this._window_filter);
  };

``requestListWindows`` will return all windows or tabs of the host. 

Then we need to set a window filter. The ``window-manager`` service blocks all messages by default, or more precisely a given message is only created if it will pass the active filter. The filter we are using here is ``[1, [], ["*"]]``. The ``1`` is a boolean, representing ``true`` and indicates that the existing filter should be cleared. The next element is a list of window-ids to specify for which windows messages should be created. In our case it is empty. Following that is a list of rules. ``"*"`` means that messages shall be created for all windows.

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




  
