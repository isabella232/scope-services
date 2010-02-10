=============================
Walk through the log entries
=============================


Set up the `STP/1` connection
====================================

The main DOM API for the debugger is:

.. code-block:: javascript

  interface opera {
    scopeAddClient(connect_callback, receive_callback, quit_callback, port_number)
    scopeTransmit(service_name, message)
    scopeEnableService(service_name, response_callback)
    stpVersion
  }

For details see `Scope DOM API`_.

This interface is only exposed to privileged windows. If ``opera`` or ``opera.scopeAddClient`` does not exist, the interface is implemented by the ``ScopeHTTPInterface`` class. As the name suggests this is a HTTP interface to scope. It requires a local proxy which also acts as a server. For our test set up this is dragonkeeper. It translate STP to HTTP. For the events the client always keeps open one connection to the proxy so that an event can be returned instantly to the client.

Calling ``scopeAddClient`` will cause the implementation to set up the STP connection. This happens in three steps:

* On the lowest level the STP 1 protocol gets initialised by the proxy. This happens in the test setup in ``ScopeConnection`` of ``dragonkeeper`` and is needed for compatibility reasons with the STP 0 protocol.
* The ``Connect`` command is then sent to the host. If successful, this will establish an unique connection between the host and the client. 
* The service list is then returned to the client as a payload of the ``connect`` callback of the ``scopeAddClient`` call. 

For more details, see `Scope transport protocol`_ and `Scope services`_.


Enabling the services
=====================

Running ``hob js --js-test-framework`` creates a service class for each scope service on top of the Scope DOM API. Each command and event is implemented as::

  <service name> {
    // to execute a command
    request<CommandClassName>(tag, message)
    // to handle the response
    handle<CommandClassName>(status, message)
    // events
    <EventClassName with first char lowercase>(status, message)
  }

e.g.:

.. code-block:: javascript

  cls.services.EcmascriptDebugger = function()
  {
    /**
      * The name of the service used in scope in ScopeTransferProtocol
      */
    this.name = 'ecmascript-debugger';

    // e.g. for the ListRuntimes command
    this.requestListRuntimes = function(tag, message)
    {
      opera.scopeTransmit('ecmascript-debugger', message || [], 1, tag || 0);
    }
    this.handleListRuntimes = function(status, message)
    {
      const
      RUNTIME_LIST = 0,
      /* sub message RuntimeInfo */
      RUNTIME_ID = 0,
      HTML_FRAME_PATH = 1,
      WINDOW_ID = 2,
      OBJECT_ID = 3,
      URI = 4;
      // code to handle the message, 
      // e.g. the runtimeList of the message is message[RUNTIME_LIST]
    }

    // e.g. for the OnObjectSelected event
    this.onObjectSelected = function(status, message)
    {
      const
      OBJECT_ID = 0,
      WINDOW_ID = 1,
      RUNTIME_ID = 2;
      // code to handle the message
    }
  }


The created ``const``-ants are identifiers to read and handle the response message.



To handle responses more specifically there is also a ``tagManager``. This works like:

.. code-block:: javascript

  var tag = tagManager.setCallback(callbackObject, callbackMethod, [/* array with callback context */]);
  services[<the name of the service>].request<CommandName>(tag, message);

Such a callback will have the arguments as:

.. code-block:: javascript

  [status, response_message].concat([/* array with callback context */])


The service list which is returned as the payload of the ``connect`` callback is only needed for compatibility reasons with the `STP/0` protocol. As soon as the client gets it, it will call ``services.scope.requestHostInfo()`` in ``client`` in ``on_host_connected``. The scope service is enabled by default so that it can be used immediately. This should cause the following log entries:

.. code-block:: none

  sent: 
    service: scope 
    command: HostInfo 
    tag: 0 
    payload: []

  received: 
    service: scope 
    command: HostInfo 
    status: OK 
    tag: 0 
    payload: [1,​"2.​4",​"WinGogi",​"WinGogi",​"Opera/9.​70 (​WinGogi; U; en)​ Presto/2.​3.​0",​[["scope",​"1.​0.​0",​0,​1],​["console-logger",​"1.​0.​0",​0,​1],​["ecmascript-logger",​"1.​0.​0",​0,​1],​["http-logger",​"1.​0.​0",​0,​1],​["exec",​"1.​0.​0",​0,​1],​["window-manager",​"1.​0.​0",​0,​1],​["url-player",​"1.​0.​0",​0,​1],​["ecmascript-debugger",​"1.​0.​0",​0,​1],​["core-2-4",​"1.​0.​0",​0,​1],​["stp-0",​"1.​0.​0",​0,​1],​["stp-1",​"1.​0.​0",​0,​1]]]

The scope service will read that message and enable each service in the list with:

.. code-block:: javascript

  if(service[NAME] in services && service[NAME] != "scope" )
  {
    services['scope'].requestEnable(0,[service[NAME]]);
  }

This should cause the following entries in the log:

.. code-block:: none

  sent: 
    service: scope 
    command: Enable 
    tag: 1 
    payload: ["console-logger"]

  sent: 
    service: scope 
    command: Enable 
    tag: 2 
    payload: ["http-logger"]

  sent: 
    service: scope 
    command: Enable 
    tag: 3 
    payload: ["exec"]

  sent: 
    service: scope 
    command: Enable 
    tag: 4 
    payload: ["window-manager"]

  sent: 
    service: scope 
    command: Enable 
    tag: 5 
    payload: ["ecmascript-debugger"]

  received: 
    service: scope 
    command: Enable 
    status: OK 
    tag: 1 
    payload: []

  received: 
    service: scope 
    command: Enable 
    status: OK 
    tag: 2 
    payload: []

  received: 
    service: scope 
    command: Enable 
    status: OK 
    tag: 3 
    payload: []

  received: 
    service: scope 
    command: Enable 
    status: OK 
    tag: 4 
    payload: []

  received: 
    service: scope 
    command: Enable 
    status: OK 
    tag: 5 
    payload: []


Although not in that order, the communication is asynchronous.


Setting the Debug Context
=========================

The service class has also the following methods:

.. code-block:: javascript

  ServiceBase {
    // called if the service was enabled successfully
    onEnableSuccess()
    // called when ever a new debug context is set
    onWindowFilterChange(windowFilterObject)
    // called if the client quits the connection
    onQuit()
  }

The ``window-manager`` service will call ``requestListWindows()`` in the ``onEnableSuccess()`` callback. If a debug context has not been selected it will call ``requestGetActiveWindow()`` in ``handleListWindows(status, message)``. It will then set the active window ( the one which has focus ) as the debug context. This should give the following log entries, depending on the opened tabs:

.. code-block:: none

  sent: 
    service: window-manager 
    command: ListWindows 
    tag: 0 
    payload: []

  received: 
    service: window-manager 
    command: ListWindows 
    status: OK 
    tag: 0 
    payload: [[[1,​"Blank page",​"normal",​0],​[2,​"Connect to Debugger",​"normal",​0],​[3,​"Blank page",​"normal",​0]]]

  sent: 
    service: window-manager 
    command: GetActiveWindow 
    tag: 0 
    payload: []

  received: 
    service: window-manager 
    command: GetActiveWindow 
    status: OK 
    tag: 0 
    payload: [2]

  sent: 
    service: window-manager 
    command: ModifyFilter 
    tag: 0 
    payload: [1,[2]]

  received: 
    service: window-manager 
    command: ModifyFilter 
    status: OK 
    tag: 0 
    payload: []
  
Next, the ``window-manager`` service will call ``onWindowFilterChange(windowFilterObject)`` on each service.


Getting the runtimes and retrieving the DOM
===========================================

The ``ecmascript-debugger`` will call ``requestListRuntimes(0, [[], 1])`` in the ``onWindowFilterChange`` callback. This will retrieve any runtime in the debug context and also create one for documents which do not have one by default, e.g., documents without scripts.

It then extracts the top runtime of the returned list in ``handleListRuntimes(status, message)``. Before being able to retrieve the DOM, the service has to ensure that the runtime has finished loading to identify that there is a DOM. This is done with the ``Eval`` command like:

.. code-block:: javascript

  this._check_top_runtime_loaded = function(status, message)
  {
    const 
    VALUE = 2;

    if( message && message[VALUE] == "complete" )
    {
      this._on_top_runtime_loaded();
    }
    else
    {
      setTimeout( function(){
        var tag = tagManager.setCallback(self, self._check_top_runtime_loaded);
        var script = "return document.readyState";
        self.requestEval(tag, [self._top_runtime_id, 0, 0, script]);
      }, 100);
    }
  }

That means it checks for ``document.readyState`` as long as that value is not ``"complete"`` ( or as long as the document has not finished loading ). This should give the following log entries:

.. code-block:: none

  sent: 
    service: ecmascript-debugger 
    command: ListRuntimes 
    tag: 0 
    payload: [[],1]

  received: 
    service: ecmascript-debugger 
    command: ListRuntimes 
    status: OK 
    tag: 0 
    payload: [[[3,​"_top",​2,​53,​"opera:debug"]]]

  sent: 
    service: ecmascript-debugger 
    command: Eval 
    tag: 1 
    payload: [3,0,0,"return document.readyState",[]]

  received: 
    service: ecmascript-debugger 
    command: Eval 
    status: OK 
    tag: 1 
    payload: ["completed",​"string",​"complete"]
  
The method

.. code-block:: javascript

    this._on_top_runtime_loaded = function(status, message)
    {
      var tag = tagManager.setCallback(this, this._on_root_id);
      var script = "return document.documentElement";
      self.requestEval(tag, [this._top_runtime_id, 0, 0, script, []]);
    }

retrieves the root element of the top document. The according log entries are:

.. code-block:: none

  sent: 
    service: ecmascript-debugger 
    command: Eval 
    tag: 2 
    payload: [3,0,0,"return document.documentElement",[]]

  received: 
    service: ecmascript-debugger 
    command: Eval 
    status: OK 
    tag: 2 
    payload: ["completed",​"object",​null,​[54,​0,​0,​"object",​null,​"HTMLHtmlElement"]]


With the message definition for the ``Eval`` command it is easier to read this message:

.. code-block:: c

  message EvalResult
  {
    message ObjectValue
    {
      required uint32 objectID    = 1; 
      required bool   isCallable  = 2; 
      required bool   isFunction  = 3; 
      // type, function or object
      required string type        = 4; 
      optional uint32 prototypeID = 5; 
      // Name of class (object) or function
      optional string name        = 6; 
    }
    required string      status      = 1; 
    required string      type        = 2; 
    // Only present for `Number`, `String` or `Boolean`
    optional string      value       = 3; 
    // Only present for `Object`
    optional ObjectValue objectValue = 4; 
  }

Object are handled with an unique id. In the given example it is a ``HTMLHtmlElement`` element with the id ``54``. This is now used to retrieve the DOM for the root element:

.. code-block:: javascript

  this._on_root_id = function(status, message)
  {
    const
    /* EvalResult */
    STATUS = 0, 
    TYPE = 1, 
    EVAL_RESULT = 3, 
    /* ObjectValue */
    OBJECT_ID = 0;

    if( status == 0 && message[STATUS] == "completed" && message[TYPE] == "object" )
    {
      var root_id = message[EVAL_RESULT][OBJECT_ID];
      this.requestInspectDom(0, [root_id, "subtree"])
    }
    else
    {
      // TODO
    }
  }

And the log entries for a blank page are:

.. code-block:: none

  sent: 
    service: ecmascript-debugger 
    command: InspectDom 
    tag: 0 
    payload: [92,"subtree"]

  received: 
    service: ecmascript-debugger 
    command: InspectDom 
    status: OK 
    tag: 0 
    payload: [[[92,​1,​"HTML",​1,​"",​[["",​"dir",​"ltr"]],​2],​[98,​1,​"HEAD",​2,​"",​[],​3],​[99,​3,​"",​3,​null,​null,​null,​"\n "],​[100,​1,​"TITLE",​3,​"",​[],​1],​[101,​3,​"",​4,​null,​null,​null,​"Blank page"],​[102,​3,​"",​3,​null,​null,​null,​"\n"],​[103,​1,​"BODY",​2,​"",​[],​0]]]

This message is displayed in ``handleInspectDom`` as:

.. code-block:: html

  <html dir="ltr"> [92]
    <head> [98]
      <title>Blank page</title> [100]
    </head>
    <body/> [103]
  </html>

The numbers in brackets are the object-ids of the according elements.


Submit a command manually
=========================

Exec
----

With the Exec service it is possible to submit any Opera UI command. Select "Exec" in the "Service List". That will display the available commands and events for that service. To get the available UI commands select "GetActioInfoList" in the "Command List". That will display an overview of the selected command ``Command GetActionInfoList``. The definition of the argument of the command  is:

.. code-block:: c

  message Default
  {
  }

This means that the command has no argument. With the text field below the definition, commands can be submitted manually. A message without arguments is an empty list ``[]``, so that is the given case for the whole message. Pressing "Send" will return the command list, which is displayed below the definition of the returned message. The response should look similar to:

.. code-block:: javascript

  response:
    status: OK
    payload: [[["Activate element"],​["Adaptive Zoom In"],​["Adaptive Zoom Out"],​["Back"],​["Backspace"],​["Backspace word"],​["Change direction to LTR"],​["Change direction to RTL"],​["Check item"],​["Clear"],​["Click button"],​["Click default button"],​["Close cycler"],​["Close dropdown"],​["Close page"],​["Pan document"],​["Convert hex to unicode"],​["Copy"],​["Copy label text"],​["Copy to note"],​["Cut"],​["Decrease visual viewport height 16px"],​["Decrease visual viewport width 16px"],​["Delay"],​["Delete"],​["Delete to end of line"],​["Delete word"],​["Deselect all"],​["Disable Handheld Mode"],​["Disable mediumscreen mode"],​["Disable scroll bars"],​["Disable tv rendering mode"],​["Download URL"],​["Enable Handheld Mode"],​["Enable mediumscreen mode"],​["Enable scroll bars"],​["Enable tv rendering mode"],​["External action"],​["Find inline"],​["Find next"],​["Find previous"],​["Focus address bar"],​["Focus current tab"],​["Focus form"],​["Focus next frame"],​["Focus next radio widget"],​["Focus next widget"],​["Focus previous frame"],​["Focus previous radio widget"],​["Focus previous widget"],​["Forward"],​["Go"],​["GOGI Paste and Go"],​["Go to Content Magic"],​["Go to end"],​["Go to homepage"],​["Go to line end"],​["Go to line start"],​["Go to speed dial"],​["Go to start"],​["Go to Top CM Bottom"],​["Highlight current block"],​["Highlight next block"],​["Highlight next element"],​["Highlight next heading"],​["Highlight next URL"],​["Highlight previous block"],​["Highlight previous element"],​["Highlight previous heading"],​["Highlight previous URL"],​["Increase visual viewport height 16px"],​["Increase visual viewport width 16px"],​["Insert"],​["Left adjust text"],​["Lock visual viewport size"],​["Make Readable"],​["Move rendering viewport down"],​["Move rendering viewport down 16px"],​["Move rendering viewport left"],​["Move rendering viewport left 16px"],​["Move rendering viewport right"],​["Move rendering viewport right 16px"],​["Move rendering viewport up"],​["Move rendering viewport up 16px"],​["Navigate down"],​["Navigate leave down"],​["Navigate leave left"],​["Navigate leave right"],​["Navigate leave up"],​["Navigate left"],​["Navigate page down"],​["Navigate page up"],​["Navigate right"],​["Navigate up"],​["New page"],​["Next character"],​["next character spatial"],​["Next item"],​["Next line"],​["next line spatial"],​["Next word"],​["Open link"],​["Open link in background page"],​["Open link in background window"],​["Open link in new page"],​["Open link in new window"],​["Page down"],​["Page left"],​["Page right"],​["Page up"],​["Pan document X"],​["Pan document Y"],​["Paste"],​["Paste and go"],​["Paste mouse selection"],​["Paste to note"],​["Previous character"],​["previous character spatial"],​["Previous item"],​["Previous line"],​["previous line spatial"],​["Previous word"],​["Quit"],​["Range go to end"],​["Range go to line end"],​["Range go to line start"],​["Range go to start"],​["Range next character"],​["Range next item"],​["Range next line"],​["Range next word"],​["Range page down"],​["Range page left"],​["Range page right"],​["Range page up"],​["Range previous character"],​["Range previous item"],​["Range previous line"],​["Range previous word"],​["Redo"],​["Reload"],​["Reload stylesheets"],​["Right adjust text"],​["Scroll"],​["Scroll down"],​["Scroll left"],​["Scroll right"],​["Scroll up"],​["Search"],​["Select all"],​["Select item"],​["Set desktop layout viewport size"],​["Show dropdown"],​["Show hidden popup menu"],​["Show link popup menu"],​["Show popup menu"],​["Stop"],​["SVG pause animation"],​["SVG reset pan"],​["SVG set quality"],​["SVG start animation"],​["SVG stop animation"],​["SVG zoom"],​["SVG zoom in"],​["SVG zoom out"],​["Switch to next window"],​["Switch to previous window"],​["Toggle overstrike"],​["Toggle presentation mode"],​["Toggle style bold"],​["Toggle style italic"],​["Toggle style underline"],​["Uncheck item"],​["Undo"],​["Unfocus form"],​["Unfocus plugin"],​["Unlock visual viewport size"],​["Unset desktop layout viewport size"],​["Wand"],​["Zoom in"],​["Zoom out"],​["Zoom point"],​["Zoom step in"],​["Zoom step out"],​["Zoom to"],​["_keydown"],​["_keyup"],​["_type"]]]


To execute one of the commands, select the ``Exec`` command in the command list. The argument is a list of Actions, each Action with a required name, an optional parameter, and an optional `ID` of the target window. The id is displayed in the "Window List" for the selected window. A simple command is ``"Go"``, which means to an `URL` in the case of a browser. So the command argument should resemble:

.. code-block:: javascript

  [[["Go", "http://www.opera.com", 1]]] 

The three objects are message, actionList, and action. The action itself is ``"Go"``, where to is ``"http://www.opera.com"`` and the target window id is ``1``. Submitting the command will cause Opera to load that URL. The response in this case is short:

.. code-block:: javascript

  response:
    status: OK
    payload: []

EcmascriptDebugger
------------------

The EcmascriptDebugger exposes a powerful interface to the ECMA engine and the DOM. Setting breakpoints, retrieving the DOM, highlighting elements, and much more can be done with it. Let us have a look at the Eval command. We will create a simple function on the host side and execute it with some values. The message to create the function is:

.. code-block:: javascript

   [1, 0, 0, "return function(string){alert(string)}"]

The first value is the ``runtimeID``. It is displayed in the "Window List" for the selected window. The two following values are ``threadID`` and ``frameIndex``. They are used to evaluate code while stepping trough code, e.g., when the runtime hits a breakpoint. For the given case they are both not set, which means ``0``. ``"return function(string){alert(string)}"`` is the script to be evaluated and is a simple function to call alert. The response will look similar to:

.. code-block:: c

  response:
    status: OK
    payload: ["completed",​"object",​null,​[10,​1,​1,​"function",​null,​""]]

That means the code was executed successfully and the returned value is an object. The interesting part is the ``ObjectValue``, ``[10,​1,​1,​"function",​null,​""]``. The first number in that object is the internal id for the returned object as shown in the above example ``10``. Now we are able to call that function with the Eval command:

.. code-block:: javascript

  [1, 0, 0, "_f(\"hello\")", [["_f", 10]]]


The syntax is the same as before, but with a variable list with one variable ``["_f", 10]``, a key value pair, where the key is an identifier used in the script string, and the value is the object id of the function. Submitting that message will show an alert box in the host with the message "hello".



.. _Scope DOM API: ./scope-dom-interface.html
.. _Scope transport protocol: ./scope-transport-protocol.html
.. _Scope services: ./scope-stp1-services.html

