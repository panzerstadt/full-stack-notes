# WEB HOSTING
## (with related terminologies)
- to host something on the web, you need web servers (thing that sends you your website when you type your website url)
- [how the web works](https://jeffknupp.com/blog/2014/03/03/what-is-a-web-framework/)

## types of web server technologies
- dedicated servers
	- Apache
	- Nginx
- cloud servers
	- AWS
	- Google Cloud

## TODO: deploy something on each service
- how to setup and deploy server (both on Nginx and Cloud)
- how to connect an API

## static and dynamic websites
- static - web server grabs files and returns them
- dynamic - web server runs programs to generate content and returns them

## Apache vs Nginx
[link to Nginx readme](./Physical/Nginx/nginx-readme.md)

###### Apache
- 1 page web request = 1 process_thread (of the CPU)
- a *forked threaded* solution, or *keep-alive*, where one connection is opened for one user.

###### Nginx
- event driven


	flask is NOT a webserver, but it includes one for local testing
	Gunicorn is a webserver



## webserver workflow (with python)
- [good explanation](https://stackoverflow.com/questions/4929626/what-are-wsgi-and-cgi-in-plain-english)
- [ref for below](https://www.quora.com/What-are-the-differences-between-nginx-and-gunicorn)

#### Assuming 3 main technologies and your app
- **Nginx** - listens on port 80 for incoming HTTP requests from the internet
- **Gunicorn** - listens on another port (8000 usually) for HTTP requests from Nginx
- **Flask/Django (your app)** - configured with Gunicorn
- **Database** - some DB tech (Postgres/MySQL/GraphQL)

1. someone makes a request to your web app (a browser / a bot)
2. Nginx receives the HTTP request.
	- If it is a static resource (css/js/images), Nginx serves it without bothering gunicorn.
	- If it is a dynamic one, Nginx receives all the [TCP](https://www.reddit.com/r/explainlikeimfive/comments/1ahc5s/eli5_tcpip/?st=jecis62f&sh=f2739e80) packets belonging to the HTTP request efficiently, and then forwards the request to Gunicorn once the entire request is received.
		- this frees your Gunicorn provesses from handling slow clients.
3. Gunicorn receives the request from Nginx, translates it into a [Web Server Gateway Interface](https://www.fullstackpython.com/wsgi-servers.html) and calls the connected Flask/Django app (web framework)'s *request handler method*(which means calls a function from the app based on what you wrote in it)
	- *WSGI* is a python-only thing. *See CGI and FastFGI below*

4. The Web Framework (Flask/Django/others) implements business logic (does what it needs to do) and sends back a HTTP response.
	- you can configure Gunicorn to make network calls to your database and other external services concurrently using ***non-blocking I/O*** so that the application can do the main thing while waiting on the socket for other requests.

5. Gunicorn then returns the response to Nginx and Nginx sends the response to the client (the browser or bot)

## default webservers (in Flask or Django) vs production webservers

When interfacing with the external world, you need to:
- handle slow clients
- tune the number of worker processes according to the number of available CPU cores and RAM
- incorporate asynchronous I/O using gevents
- other optimizations. 

***The default web servers provided by popular web frameworks like Django or Flask are optimized for development and perform poorly on production. (like Flask's test server)***

**So Nginx and Gunicorn make your Python web app production-ready.**


## on concurrency
- concurrency = **two or more events** or circumstances **happening** or existing **at the same time**
- http://www.aosabook.org/en/nginx.html

##### Why is high concurrency important for web servers?
1. **slow clients** (ADSL/dialup connections/mobile)

To illustrate the problem with slow clients, imagine a simple Apache-based web server which produces a relatively short **100 KB response—a web page with text or an image**. It can be merely **a fraction of a second to generate** or retrieve this page, but it takes **10 seconds to transmit over a 80 kbps connection** to a client.

Essentially, the *web server would relatively quickly pull 100 KB of content, and then it would be busy for 10 seconds slowly sending this content to the client before freeing its connection.*

Now imagine that you have **1,000 simultaneously connected clients** who have requested similar content. **every client needs to be given memory to run their request.** If only 1 MB of additional memory is allocated per client, it would result in **1000 MB (about 1 GB) of extra memory devoted to serving just 1000 clients 100 KB of content.** 

In reality, a typical web server based on Apache commonly allocates more than 1 MB of additional memory per connection, and regrettably tens of kbps is still often the effective speed of mobile communications.

2. **persistent connections** (notifications, news and friend feeds, modern browsers that open 4-6 simultaneous connections to speed up loading)

With persistent connections the problem of handling concurrency is even more pronounced, because **to avoid latency associated with establishing new HTTP connections, clients would stay connected**, and for each connected client there's a certain amount of memory allocated by the web server.

> Thus, the web server needs to scale nonlinearly with the growing number of simultaneous connections and requests per second. (linear scaling = 1MB per person x 1000 person = 1GB to transmit 100KB of content to everyone)



## the LAMP stack
- components of a web application solution stack
- [source](https://www.reddit.com/r/explainlikeimfive/comments/14lmw6/eli5_please_explain_the_roles_of_the_components/)



## CGI, FastCGI, WSGI (the thing in between web servers and you the client)
- [source](https://www.digitalocean.com/community/tutorials/a-comparison-of-web-servers-for-python-based-web-applications)

##### CGI
1. User makes a request (e.g. clicks on something in the browser)
2. web server CGI program (e.g. starts a Python Interpreter), feeds the request, then returns request

	Programs using CGI to communicate with their web server need to be started by the server for every request. So, every request starts a new Python interpreter – which takes some time to start up – thus making the whole interface only usable for low load situations.

	The upside of CGI is that it is simple – writing a Python program which uses CGI is a matter of about three lines of code. This simplicity comes at a price: it does very few things to help the developer.

##### FastCGI
1. web server runs a long-running background process (the program)
2. User makes a request and the webserver processes it through the already-running program

##### WSGI
0. Some other programmer solves your CGI web programming problem.
1. has plugins to do
	- session management (same user, multiple http requests)
	- compression (into gzip) to same server bandwidth
	- [SSL](https://www.reddit.com/r/explainlikeimfive/comments/jsq3m/eli5_what_are_online_security_certificates_ssl/?st=jecix7hq&sh=1cfb1f8b) encryption

#### what is a WSGI?
- an **extra layer** in between your interface (browser) of your app and the web.
- mainly for generating dynamic webpages before putting it in the browser (because it seems there are many different settings needed for the app to change to make it work with different web servers. WSGI does them for you.)

![wsgi](./images/web-browser-server-wsgi)

