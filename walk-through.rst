=============================
Walk Through the Log Entries
=============================

.. class:: docdata

Status
  Draft

Introduced
  Core 2.4

.. role:: code


Setup the `STP/1` Connection
====================================

The main DOM API for the debugger is::

  interface opera {
    scopeAddClient(connected: callback, receive: callback, quit: callback, port: number)
    scopeTransmit(service: string, message: string)
    scopeEnableService(service: string, response: callback)
    stpVersion
  }

for details see `Scope DOM API`_.

This interface gets only exposed to privileged windows. If ``opera`` or ``opera.scopeAddClient`` does not exist, the interface is implemented by the ``ScopeHTTPInterface`` class. As the name suggests this is a http interface to scope. It requires a local proxy which also acts as server. For our test setup this is dragonkeeper. It translate STP to HTTP. For the events the client keeps always one connection to the proxy open so that an event can be returned instantly to the client.

Calling ``scopeAddClient`` will cause the implementation to setup the STP connection. This happens in three steps:

* On the lowest level the STP 1 protocol gets initialised by the proxy. This happens in the test setup in ``ScopeConnection`` of ``dragonkeeper`` and is needed for compatibility reasons with STP 0 protocol.
* Then the ``Connect`` command is sent to the host. This will establish on success  an unique connection between the host and the client. 
* Then the service list is returned to the client as payload of the ``connected`` callback of the ``scopeAddClient`` call. 

For more details see `Scope transport protocol`_ and `Scope services`_.


Enabling the Services
=====================

Running ``opprotoc --js --js-test-framework`` does create on top of the Scope DOM API a service class for each scope service. Each command and event is implemented as::

  <service name> {
    // to execute a command
    request&lt;CommandClassName>(tag, message)
    // to handle the response
    handle&lt;CommandClassName>(status, message)
    // events
    on&lt;EventClassName>(status, message)
  }

e.g.::

  cls.services.EcmascriptDebugger = function()
  {
    /**
      * The name of the service used in scope in ScopeTransferProtocol
      */
    this.name = 'ecmascript-debugger';
    // snipp snipp
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
      
    }
    // snipp snipp
    // e.g. for the OnObjectSelected event
    this.onObjectSelected = function(status, message)
    {
      const
      OBJECT_ID = 0,
      WINDOW_ID = 1,
      RUNTIME_ID = 2;

    }
  }

The created consts are identifiers to read and handle the response message.

To handle responses more specifically there is also a ``tagManager`` singleton. That works basically like::

  var tag = tagManager.setCallback(<callbackObject>, <callbackMethod>, <array with callback context>);
  services[<service-name>].request<CommandName>(tag, <message>);

Such a callback will have the arguments as ``[status, response_message].concat(&lt;array with callback context>)``.

The service list which is returned as the payload of the ``connected`` callback is basically only needed for compatibility reasons with the STP 0 protocol. As soon as the client gets it it will call ``services.scope.requestHostInfo()`` in the ``client`` singleton in ``on_host_connected``. The scope service is enabled by default so that it can be used always. This should cause the following log entries:

.. class:: log

::

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

The scope service will read that message and enable each service in the list with::

  if(service[NAME] in services && service[NAME] != "scope" )
  {
    tag = tagManager.setCallback(this, this.handleEnableService, [service[NAME]]);
    services['scope'].requestEnable(tag,[service[NAME]]);
  }

This should cause the following entries in the log:

.. class:: log

::

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


Perhaps not in that order, the communication is asynchronous.


Setting the Debug Context
=========================

The service class has also the following methods::

  ServiceBase {
    // called if the service was enabled successfully
    onEnableSuccess()
    // called when ever a new debug context is set
    onWindowFilterChange(&lt;filter>)
    // called if the client quits the connection
    onQuit()
  }

The ``window-manager`` service will call ``this.requestListWindows()`` in the ``onEnableSuccess()`` callback. If there is not jet an debug context selected it will call ``requestGetActiveWindow()`` in ``handleListWindows(status, message)``. It will then set the active window ( the one which has focus ) as the debug context. This should give the following log entries, depending on the opened tabs:

.. class:: log

::

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
  
Now the ``window-manager`` service will call ``onWindowFilterChange(<filter>)`` on each service.


Getting the runtimes and retrieving the DOM
===========================================

The ``ecmascript_debugger`` will call ``requestListRuntimes(0, [[], 1])`` in the ``onWindowFilterChange`` callback. This will retrieve any runtime in the debug context and also create one for documents which don't have one by default, e.g. documents without scripts.

It then extracts the top runtime of the returned list in ``handleListRuntimes(status, message)``. Before being able to retrieve the DOM the service has to ensure that the runtime has finished loading to be sure that there is a DOM. This is done with the ``Eval`` command like::

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
        self.requestEval(tag, [self._top_runtime_id, 0, 0, script, []]);
      }, 100);
    }
  }

That means it checks for ``document.readyState`` as long as that value is not ``"complete"`` ( or as long as the document has not finished loading ). This should give the following log entries:

.. class:: log

::

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
  
The function ``_on_top_runtime_loaded``

::

    this._on_top_runtime_loaded = function(status, message)
    {
      var tag = tagManager.setCallback(this, this._on_root_id);
      var script = "return document.documentElement";
      self.requestEval(tag, [this._top_runtime_id, 0, 0, script, []]);
    }

does retrieve the root element of the top document. The according log entries:

.. class:: log

::

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


With the message definition for the ``Eval`` command it's easier to read that message::


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

Object are handled with an unique id, in the given example it's a ``HTMLHtmlElement`` element with the id ``54``. This is now used to retrieve the DOM for the root element::

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

And the log entries for a blank page:

.. class:: log

::

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

.. raw:: html

  <div class="dom">
  <div><div style='margin-left:16px;'><node>&lt;html <key>dir</key>=<value>"ltr"</value>&gt;</node> <span class='object-id'>[92]</span></div><div style='margin-left:32px;'><node>&lt;head&gt;</node> <span class='object-id'>[98]</span></div><div style='margin-left:48px;'><text ref-id='99'>
   </text></div><div style='margin-left:48px;' ><node>&lt;title&gt;</node><text>Blank page</text><node>&lt;/title&gt;</node> <span class='object-id'>[100]</span></div><div style='margin-left:48px;'><text ref-id='102'>
  </text></div><div style='margin-left:32px;'><node>&lt;/head&gt;</node></div><div style='margin-left:32px;'><node>&lt;body/&gt;</node> <span class='object-id'>[103]</span></div><div style='margin-left:16px;'><node>&lt;/html&gt;</node></div></div>
  </div>

The numbers in brackets are the object-ids of the according elements.


Submit a command manually
=========================
TODO


.. _Scope DOM API: /scope-interface/scope-dom-interface.html
.. _Scope transport protocol: /scope-interface/scope-transport-protocol.html
.. _Scope services: /scope-interface/scope-stp1-services.html

