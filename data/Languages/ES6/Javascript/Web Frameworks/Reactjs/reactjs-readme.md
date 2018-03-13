# REACTjs
- another framework like node

## TODO: react apps
- todo app (quick) https://medium.freecodecamp.org/how-to-build-a-real-time-todo-app-with-react-native-19a1ce15b0b3
- learning webpack with react https://github.com/MikaelCarpenter/ReactWebpack

## DONE
- [react + sass menu](https://codepen.io/panzerstadt/pen/rdONWV?editors=0010)


## facebook's react app creator (like cookiecuter template)
- https://github.com/facebook/create-react-app/tree/master

## React did some changes to Javascript
### the heart of Javascript - DOM
- https://www.codecademy.com/articles/react-virtual-dom
- manipulating DOM is slow. most Javascript frameworks also UPDATE THEM MORE THAN THEY NEED TO
	- checklist app
		- when you tick one item, javascript rebuilds the ENTIRE list
- therefore React popularized something called *virtual DOM*

#### Virtual DOM
- [more](http://reactkungfu.com/2015/10/the-difference-between-virtual-dom-and-dom/)
- in React, for every DOM object, there is a corresponding *virtual DOM object*. a virtual DOM object is a ***representation*** of a DOM object (a lightweight copy)
- exactly same as DOM, but can't change anything on the screen
- manipulating virtual DOM is much faster, like editing a blueprint, vs moving rooms in the entire house (DOM).
- when a JSX element is rendered, *every single virtual DOM* gets updated, then **React compares the virtual DOM with the previuos virtual DOM**, like Git, and **only updates the changes**.
- it is called **diffing**

> Programming in React means constantly working with event listeners


## Event Listeners
- onClick, onMouseOver and etc
- [full list](https://reactjs.org/docs/events.html#supported-events)
- when you feed an event listener, its attribute must be a function (without brackets it seems)
- `<img src="#" alt="kitty" onClick={makeDoggy} />` is valid


## JSX is not compulsory to write React
	You can write React code without using JSX at all!

	The majority of React programmers do use JSX, and we will use it for the remainder of this tutorial, but you should understand that it is possible to write React code without it.

	The following JSX expression:

	const h1 = <h1>Hello world</h1>;
	can be rewritten without JSX, like this:

	const h1 = React.createElement(
	  "h1",
	  null,
	  "Hello, world"
	);
	When a JSX element is compiled, the compiler transforms the JSX element into the method that you see above: React.createElement(). Every JSX element is secretly a call to React.createElement().

	We won't go in-depth into how React.createElement() works, but you can start with the documentation if you'd like to learn more!
