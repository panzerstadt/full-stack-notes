# external javascript method 2

### serving with nodejs
- by running it with `node server.js`

0. create your html file and save it (e.g. `index.html`)
1. create a server that opens a port and listens (e.g. `server.js`)
2. write your js code in another file (e.g. `client.js`)
3. preprocess that file with `browserify` (e.g. `browserify client-before -o client-after.js`)
4. `server.js` points to **both** `index.html` and `client.js`
5. `index.html` points to `client.js`