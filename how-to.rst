=========================================
How to setup a Test Environment for STP 1
=========================================


With easy_install and Python scripts in the path variable
=========================================================

* Get an `Opera Gogi Core 2.4 build`_ .
* Get hob with ``easy_install hob``
* Run ``hob js --js-test-framework`` to create a HTML test framework. You should see the following output in our console:

  ::

    Wrote service-interface ConsoleLogger to 'js-out\console_logger_interface.js'
    Wrote service-interface ConsoleLogger to 'js-out\console_logger_implementation.js'
    Wrote service-interface HttpLogger to 'js-out\http_logger_interface.js'
    Wrote service-interface HttpLogger to 'js-out\http_logger_implementation.js'
    Wrote service-interface Scope to 'js-out\scope_interface.js'
    Wrote service-interface Scope to 'js-out\scope_implementation.js'
    Wrote service-interface WindowManager to 'js-out\window_manager_interface.js'
    Wrote service-interface WindowManager to 'js-out\window_manager_implementation.js'
    Wrote service-interface Exec to 'js-out\exec_interface.js'
    Wrote service-interface Exec to 'js-out\exec_implementation.js'
    Wrote service-interface EcmascriptDebugger to 'js-out\ecmascript_debugger_interface.js'
    Wrote service-interface EcmascriptDebugger to 'js-out\ecmascript_debugger_implementation.js'
    Wrote js-out\client.js
    Wrote js-out\client.html
    Wrote js-out\service_base.js
    Wrote js-out\http_interface.js
    Wrote js-out\command_map.py
    Wrote js-out\helper_const_ids.js
    Wrote js-out\service_descriptions.js
    Copied templates\js\clientlib_async.js
    Copied templates\js\tag_manager.js
    Copied templates\js\json.js
    Copied templates\js\style.css

* Get dragonkeeper with ``easy_install dragonkeeper``
* Run ``dragonkeeper -dfr <path to the created test framework>`` to start a local server / proxy. You should see the following output in your console:

  ::

    server on: http://localhost:8002/

* Start the Opera gogi build and go to ``opera:debug``. Press the Connect button. You should see the following output in the dragonkeeper console:

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

* Go to ``http://localhost:8002/`` with any Browser and open ``js-out/client.html``. 

  The test framework should start. It should set the active tab in the gogi build as debug context and retrieve the DOM from the top document of that tab. In the "Log" section you can see the communication with scope. "Window List" shows the tabs of the debugged Opera, and "Service List" the available services. Click any service name to get the "Command List" and "Event List" for the selected service. Click any command in the "Command List" to display a description of the data structure for that command and its response. Try out the command by typing the message manually and see the corresponding response.

  See `Walk Through the Log Entries`_ for more details.
  


With other setups
=================

You need at least `Python`_ and `Mercurial`_. To get ``hob`` and ``dragonkeeper``, in the commandline type:

::
  
  hg clone http://code.opera.com/scope/hob
  hg clone http://code.opera.com/scope/dragonkeeper

To create the test frame go to the cloned hob direcory and type:

::

  hg up
  python -m hob.script js --js-test--framework

To start dragonkeeper, change to the dragonkeeper directory and type:

::

  hg up
  python -m dragonkeeper -dfr <path to the created test framework> 

Other than that, it is the same as done in the preceding instructions.

.. _Python: http://www.python.org/
.. _Mercurial: http://mercurial.selenic.com/wiki/
.. _Opera Gogi Core 2.4 build: https://homes.oslo.osa/jborsodi/stp1/
.. _Walk Through the Log Entries: ./walk-through.html
