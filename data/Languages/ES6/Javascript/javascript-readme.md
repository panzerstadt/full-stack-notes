# JAVASCRIPT

### TODO: learn a lot of javascript
- [actually learn javascript](https://stackskills.com/courses/javascript-complete/lectures/903458) [source2](https://www.udemy.com/the-complete-javascript-course/)
- short javascript tutorial https://medium.com/codingthesmartway-com-blog/pure-javascript-building-a-real-world-application-from-scratch-5213591cfcd6
- learn javascript through [rapydscript](https://github.com/atsepkov/RapydScript)? It's like python so its cheating a bit.
- learn react and gulp through an [app with flask](https://realpython.com/blog/python/the-ultimate-flask-front-end/)
- callback functions goddamnit

## DONE
- [instagram viewing app](https://drive.google.com/file/d/1JjvlIy4bwWJdbM8jc1NczbVyTpZqC69R/view?usp=sharing)
	- [code](https://github.com/panzerstadt/tut-instagram-app)
- [coding train twitter bot](https://www.youtube.com/watch?v=ZvsqQjwrISQ)
	- [code](https://github.com/panzerstadt/tut-twitter-bot)

## things to know (vs python)
- javascript is an ***ASYNCHRONOUS*** programming language
	- [callback](https://www.google.co.jp/search?client=safari&rls=en&q=learning+callback+structure+javascript&ie=UTF-8&oe=UTF-8&gfe_rd=cr&dcr=0&ei=-d6fWuGbB7P98Af--bngDg) functions are a big thing.
	- things like error handling are a *Pain In The Ass* (PITA) because its hard to find out which method went wrong at what time (because they don't follow an order)
- C# and F# is also asynchronous (but they have design patterns called 'async/wait' which make it easier apparently)
- to deal with it properly, learn how to use `promise` or `future` or `task`
	- with JQuery, use `$.Deferred()`
	- with AngularJS, use `$q.defer()`

## javascript history
- https://codeburst.io/javascript-wtf-is-es6-es8-es-2017-ecmascript-dca859e4821c
Here’s what happened long, long ago:
1. JavaScript was originally named JavaScript in hopes of capitalizing on the success of Java.
2. Netscape then submitted JavaScript to ECMA International for Standardization. (ECMA is an organization that standardizes information)
3. This results in a new language standard, known as ECMAScript.
4. Put simply, ECMAScript is a standard. While JavaScript is the most popular implementation of that standard. JavaScript implements ECMAScript and builds on top of it.

## useful things
- progress bars https://docs.travis-ci.com/api#overview
- simple progress bar https://github.com/fehmicansaglam/progressed.io
- other charts http://luizperes.github.io/status-projects/
- ejs package is like jinja2, expressJS templating engine
	- for hairy things like running dynamic code on html

## how to run javascript
- on the browser - use the browser
	- [quora](https://www.quora.com/How-do-I-run-a-JavaScript-file)
	1. use [jsbin](http://jsbin.com/?html,output)
	2. save the file as .HTML, .HTM and open in google chrome, right click, inspect element, and click console. You should be able to see the results of your code running.

- off the browser - use node.js
	- in terminal: **node myapp.js**


## NODEJS

>just like when you do ***python myapp.py*** in terminal,
> now you can do ***node myapp.js*** in terminal.

> apparently you couldn't before.

[eli5](https://www.reddit.com/r/learnjavascript/comments/3d4hs5/eli5_what_in_the_heck_is_nodejs/?st=jedngbld&sh=7bd840a1)
- a lightweight server that allows you to run Javascript outside the browser
- perform actions on your local machine
- has the ability to run HTTP applications written in Javascript
	- essentially doing what Apache httpd does (meaning Node.js acts like a webserver)
- meaning, there are now applications using Javascript to run front end ***AND*** backend.
- but Node is single threaded, so its not super fast

	The main advantage is the asynchronous nature of the language, which is caused by the single-threaded event-loop, which is a fancy way of saying "I can schedule a bunch of jobs simultaneously, and I'll be able to answer them as soon as they are done processing - no job that is done will have to wait around for me to get around to it because I'll know instantly".

## command cheat sheet

#### console.log() and cousins (like print() in python)
- 4 ways to display data, by writing into:
1. html element - **innerHTML**
	1. ask javascript to find the element
2. html output - **document.write()**
3. alert box (pop up in browser) - **window.alert()**
4. browser console - **console.log()**

#### load html (the final output usually) when working in js
- use [ExpressJS](http://expressjs.com)
- https://stackoverflow.com/questions/4720343/loading-basic-html-in-node-js

#### callback functions
	It's like calling a business on the phone and leaving your "callback" number, so they can call you when someone is available to get back to you. That's better than hanging on the line for who knows how long and not being able to attend to other affairs.

- https://stackoverflow.com/questions/824234/what-is-a-callback-function

	A callback function is a function which is:

	passed as an argument to another function, and,
	is invoked after some kind of event.

-https://stackoverflow.com/questions/9596276/how-to-explain-callbacks-in-plain-english-how-are-they-different-from-calling-o/9652434#9652434

Consider how programmers normally write to a file: (LQ: like python)

	fileObject = open(file)
	# now that we have WAITED for the file to open, we can write to it
	fileObject.write("We are writing to the file.")
	# now we can continue doing the other, totally unrelated things our program does

Here, we WAIT for the file to open, before we write to it. This "blocks" the flow of execution, and our program cannot do any of the other things it might need to do! What if we could do this instead:

	# we pass writeToFile (A CALLBACK FUNCTION!) to the open function
	fileObject = open(file, writeToFile)
	# execution continues flowing -- we don't wait for the file to be opened
	# ONCE the file is opened we write to it, but while we wait WE CAN DO OTHER THINGS!

It turns out we do this with some languages and frameworks. It's pretty cool! Check out Node.js to get some real practice with this kind of thinking.


## links
- https://webapplog.com/es6/