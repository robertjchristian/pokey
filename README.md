Pokey
=====
An easy to use HTTP test client

What is Pokey?
============================
Pokey is an HTTP Client of sorts which allows you to specify HTTP endpoints, request headers, request body, and make assertions about the response.  It can be used for regression testing, unit testing, TDD, stress testing, health checks, or even as a friendly alternative to curl.

Why Pokey?
============================
See the "How to Setup Tests" section... hopefully it's obvious!

Prerequisites
============================
* Python 2.6.6 or greater.
* Requests Python module available [here] (http://docs.python-requests.org/en/latest/index.html) or just run the setup.sh script included within this project.

How to Run
============================
* Run pokey: python pokey.py (use -h for help)
* Use --path option to specify test folder (otherwise "tests" is assumed)

How to Setup Tests
============================
First let's look at a tree view of this project:

<pre>
├── MIT-LICENSE.txt
├── README.md
├── pokey.py
├── setup.sh
└── tests
    └── examples
        ├── GET
        │   ├── custom_headers
        │   │   ├── about
        │   │   ├── headers
        │   │   └── url
        │   ├── regex
        │   │   ├── about
        │   │   ├── regex
        │   │   └── url
        │   ├── rest_call_with_assertions
        │   │   ├── about
        │   │   ├── expected_response_body
        │   │   ├── expected_response_message
        │   │   └── url
        │   └── simplest
        │       ├── about
        │       └── url
        └── POST
            └── custom_headers_with_payload
                ├── about
                ├── headers
                ├── payload
                └── url
</pre>
_Instead of using configuration files, pokey lets the file structure do most of the talking.  In this example, a simple "tree" command in the terminal tells us a lot about our test suite:_

* See that we have examples that are organized into GET and POST... there are three GET examples and one POST example.
* The "simplest" test is the simplest possible example of a pokey test.  It contains only an url.  Later we'll see that since there is no payload, a "GET" is implied, and since there is no assertion made about the response, a "200 OK" is expected.
* The "custom_headers" test uses custom request headers.  So it's like simplest, but here we provide a basic authentication header among others.
* The "rest_call_with_assertions" is an example negative-case test, where we expect something other than a "200 OK" returned from the server.
* The "custom_headers_with_payload" test includes a request body (payload).  The existence of a payload file tells pokey we want to perform a POST.  The payload file can be of any content type.

_Other notes about structure:_

* The about files are just there for humans, and provide some notes about the test.  It's just a suggested convention.
* Folders containing tests should be named for the test.
* By default, pokey scans the "tests" folder recursively, and marks all folders containing an url as test folders.  This can be overridden with the --path parameter.
* Some file managers, including the native file manager in Windows 7, will automatically peek at the contents of a text file and display them in a preview pane.  This means you can completely explore your pokey test suite without opening a text editor.

What does the test output look like?
============================
<pre>

-----------------------------------------------
Inspecting: ./tests/examples/GET/simplest
URL: http://www.google.com
Seconds elapsed: 0.115347
Response Expected: [200 OK]
Response Actual:   [200 OK]
Test passed.
-----------------------------------------------

-----------------------------------------------
Inspecting: ./tests/examples/GET/rest_call_with_assertions
URL: http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&api_key=bad_key
Seconds elapsed: 0.551011
Response Expected: [403 Forbidden]
Response Actual:   [403 Forbidden]
Test passed.
-----------------------------------------------

-----------------------------------------------
Inspecting: ./tests/examples/GET/custom_headers
URL: http://www.google.com
Seconds elapsed: 0.104213
Response Expected: [200 OK]
Response Actual:   [200 OK]
Test passed.
-----------------------------------------------

-----------------------------------------------
Inspecting: ./tests/examples/POST/custom_headers_with_payload
URL: http://www.yahoo.com
Seconds elapsed: 0.374665
Response Expected: [200 OK]
Response Actual:   [200 OK]
Test passed.
-----------------------------------------------

***********************************************
All tests passed!
Overall seconds elapsed: 1.145236
***********************************************

Done.
</pre>

Roadmap
============================

* Allow use of regular expressions in assertions.
* Provide richer test examples.  This most likely means building a web app that authenticates, and examines headers and payloads.
* Add in support for spawning many tests instances at a time to facilitate stress testing.
* Allow use of tokens in metadata files for greater flexibility.  For example url could contain http://${host}${port}/foo/bar and the values for host and port could be passed in on the command line or via properties file.  This would work the same way for payloads, headers, and assertions.
* Consider certificate support for SSL. (currently no client cert support, and always trusts host cert)
* Consider building a set of penetration tests based on OWASP.
* Consider removing requests in favor of urllib2 so that there are no prerequisites other than Python.

Support
============================
* Report issues [here] (https://github.com/robertjchristian/pokey/issues)
* [Wiki] (https://github.com/robertjchristian/pokey/wiki)
* Also see the [pokey project page] (http://robertjchristian.github.com/pokey)
