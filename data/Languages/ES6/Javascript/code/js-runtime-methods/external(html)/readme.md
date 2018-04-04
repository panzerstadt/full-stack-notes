# external javascript method 1

### serving with html
- by opening `index.html`

0. create your html file and save it (e.g. `index.html`)
1. write your js code in a file (e.g. `client.js`)
2. preprocess that file with `browserify` (e.g. `browserify client-before -o client-after.js`)
3. `index.html` points to `client.js`