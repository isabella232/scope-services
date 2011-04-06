=========================================
How to setup a Test Environment for STP 1
=========================================


With easy_install and Python scripts in the path variable
=========================================================

* Get hob with ``easy_install hob``
* Get the service definition files with ``hg clone http://bitbucket.org/scope/scope-services``
* Run ``hob js --js-test-framework`` inside the service definition repository to create a HTML test framework. You should see the following output in our console:

  ::

    Wrote service-implementation ConsoleLogger to 'console_logger_2_0.js'
    Wrote message map ConsoleLogger to 'message_map_console_logger_2_0.js'
    Wrote service-implementation Exec to 'exec_2_0.js'
    Wrote message map Exec to 'message_map_exec_2_0.js'
    Wrote service-implementation WindowManager to 'window_manager_2_0.js'
    Wrote message map WindowManager to 'message_map_window_manager_2_0.js'
    Wrote service-implementation EcmascriptDebugger to 'ecmascript_debugger_5_0.js'
    Wrote message map EcmascriptDebugger to 'message_map_ecmascript_debugger_5_0.js'
    Wrote service-implementation HttpLogger to 'http_logger_2_0.js'
    Wrote message map HttpLogger to 'message_map_http_logger_2_0.js'
    Wrote service-implementation Scope to 'scope_1_0.js'
    Wrote message map Scope to 'message_map_scope_1_0.js'
    Wrote service-implementation UrlPlayer to 'url_player_2_0.js'
    Wrote message map UrlPlayer to 'message_map_url_player_2_0.js'
    Wrote service-implementation EcmascriptLogger to 'ecmascript_logger_2_0.js'
    Wrote message map EcmascriptLogger to 'message_map_ecmascript_logger_2_0.js'
    Wrote js-out\client.js
    Wrote js-out\client.html
    Wrote js-out\lib\service_base.js
    Wrote js-out\lib\http_interface.js
    Wrote js-out\lib\stp_0_wrapper.js
    Wrote js-out\build_application.js
    Wrote js-out\lib\message_maps.js
    Wrote js-out\lib\service_descriptions.js
    Wrote js-out\runtimes.js
    Wrote js-out\dom.js
    Wrote js-out\windows.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\clientlib_async.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\tag_manager.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\json.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\namespace.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\messages.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\style.css
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\test_framework.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\logger.js
    Copied C:\Python26\lib\site-packages\hob-0.1-py2.6.egg\templates\js\utils.js

* Get dragonkeeper with ``easy_install dragonkeeper``
* Run ``dragonkeeper -dfr <path to the created test framework>`` to start a local server / proxy. You should see the following output in your console:

  ::

    server on: http://localhost:8002/

* Start a recent Opera build and go to ``opera:debug``. Press the Connect button. You should see the following output in the dragonkeeper console:

  ::

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

* Go to ``http://localhost:8002/`` with any Browser and open the link ``js-out/client.html``. 

  The test framework should start. It should set the active tab in the gogi build as debug context and retrieve the DOM from the top document of that tab. In the "Log" section you can see the communication with scope. "Window List" shows the tabs of the debugged Opera, and "Service List" the available services. Click any service name to get the "Command List" and "Event List" for the selected service. Click any command in the "Command List" to display a description of the data structure for that command and its response. Try out the command by typing the message manually and see the corresponding response.

  See `Walk Through the Log Entries`_ for more details.
  


With other setups
=================

You need at least `Python`_ and `Mercurial`_. To get ``hob`` and ``dragonkeeper``, in the commandline type:

::
  
  hg clone http://bitbucket.org/scope/hob/
  hg clone http://bitbucket.org/scope/dragonkeeper/

To create the test frame go to the cloned hob direcory and type:

::

  hg up
  python -m hob.script js --js-test-framework

To start dragonkeeper, change to the dragonkeeper directory and type:

::

  hg up
  python -m dragonkeeper.dargonkeeper -dfr <path to the created test framework> 

Other than that, it is the same as done in the preceding instructions.

.. _Python: http://www.python.org/
.. _Mercurial: http://mercurial.selenic.com/wiki/
.. _Walk Through the Log Entries: ./walk-through.html
