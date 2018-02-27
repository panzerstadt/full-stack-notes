# Big O notation
### O means slOwness
- https://rob-bell.net/2009/06/a-beginners-guide-to-big-o-notation/

## TODO: code examples of notations with timing
- python code examples of Big O
- https://www.khanacademy.org/computing/computer-science/algorithms/asymptotic-notation/a/big-o-notation

### What is an algorithm? An algorithm is a finite series of steps to solve a problem.
### How to guess slOwness ? Take the slowest part of the algorithm and measure from that.

## some simple Big O notations
```
O(1) = slOwness x 1, meaning slOwness stays the same regardless of data input size
E.g a check first element if statement (regardless of size, only ever checks first thing)

O(n) = slOwness x n, meaning for 10 data it’s 10 times as slow
E.g a for loop (does something to each and every point of data)

O(n^2) = slOwness x n squared, meaning for 10 data it’s 10x10 times as slow. 
E.g nested loops (3nestings = n3, etc)

O(2^n) = slOwness x exponential growth
E.g recursive calculation of Fibonacci numbers (calling the same function twice at every recurse)

O(logN) = 
E.g slow at first then faster and faster (like binary search, because after each iteration, you deal with half as much of the data)
- it seems that any log base just simplifies to logN, which is actually log base 2, because of something called the asymptotic bound)
```

## Good explanation from reddit by Desmeraldoo
```
/u/BigSerene is very close to correct, but I want to rephrase what they said an add some clarification. Buckle up, because this is knee-deep in college-level computer science.

Big-Oh notation is used to compare algorithms and determine which ones take more time than others to complete. But what is an algorithm? Well, it's a finite series of steps to solve a problem. Very handy in computing. Some algorithms are really slow, though. Some are fast. We want to find the fast ones and avoid the slow ones (assuming both of them get the right answer in the first place). In order to do that, we need to have a standard to compare them by. That's Big-Oh.

Say I want to find a pair of matching socks. Once thing I could do is, for every sock I own, compare it to every other sock I own (at a rate of one sock per minute, for simplicity) until I find a match. In the worst case, I'd need to go through every sock I own, _for every sock I own_, to find a match. Let's write it in Big-Oh. The notation is written relative to the size of your input. Usually this size is represented as _n_, and in this case, it represents the number of socks I own, which can vary over time. We want our algorithms to run reasonably well regardless of the size of the inputs. This one runs in O( n^2 ).

One nice thing Big-Oh does for us is get rid of clutter. I'm going to avoid the actual definitions because this isn't /r/askscience, but the jist of it is that we can ignore any _constant-time processing_ that isn't related to how many socks we're looking through. Say I putzed around on my phone for an hour for no reason before I picked my socks. We could speed up by _not_ doing that, but it won't change or Big-Oh expression, because O( 60 + n^2 ) = O( n^2 ). Same story if I wanted to count up all my socks beforehand. O( n + n^2 ) = O( n^2 ). Or if I wanted to double-check something about each pair of socks I looked at. O( 2n^2 ) = O( n^2 ). It's really nifty and helps us compare algorithms without having to know the specifics of how the data is handled or preprocessed. Obviously the algorithms with the additional expressions will run a tad slower, but when you're processing a hundred million socks, those expressions are eclipsed (known as the asymptotic running time).

These next few explanations are a distillation of the definitions, to keep things a little simpler. Unless you want to get in deeper, just take it at face value that constants are ignored, and that all members of an addition expression _except the one with the greatest magnitude_ are also ignored, a la O( 1000 + n + 1000n + n^2 ) = O( n^2 ).

Big-Oh says that, _at worst_, the approximated running time of an algorithm (how long it will take me to find my matching pair of socks) will be _no higher than_ the approximation given in parentheses (in this case, n^2 ).

Big-Omega is similar and says that, _at best_, the approximated running running time of an algorithm will be _no better than_ the approximation given in parentheses.

For an algorithm to be Big-Theta( n^2 ), it has to be Big-Oh( n^2 ) _and_ Big-Omega( n^2 ).

Those last two are mainly used in analysis, or to find the Big-Oh notation of algorithms that don't play quite as nicely as my socks example (say, algorithms that recurse). Hope that helps!
```