# Node JS (Backend)

We cant perform the buissness and major logic to the client side on the browser like front-end it can slowdown your application soo thats why we need backend to perform major tasks and our side and minimum and required only oprations should run on the client side soo the application will be faster.

A compiler which compiles the higher level language can convert the things into machine understandable code and perform the tasks.

Its serverside javascript runtime enviornment.

### Uses of Node Js

1. Node Js is mostly used for api.

2. We can connect the same database with Web App, Mobile App.

3. Node Js is super-fast for API.

4. You can be a full stack developer, you can become full stack developer.


### What api does

When we request an api call it will take data from the database and file server and give it to mobile app and web applications.

### Server :-
When we write the code like in example if we built an software like calculator and someone wants to use it but he is not able to create from scratch soo he will ask you to provide files for the software but we cannot provide our files to everyone who resides in the another corner of the world soo the concept of **Sever** comes up.

### Deployement :-
On the server we can put our local code files of our software called as deployement and with the specific adress now everyone can use it by acessing that adress from their browsers.

A serve converts your local code to global which can be used by rest of the world by acessing it on specific adress.

### How dow we get files from server :-
When we acess the adress of server it will send us the HTML and CSS files and Javascript as well and this files will get executed on the client side and thorugh the javascript it will give the call server for the data and at the server side the code will get executed and it will return data in the form of response.

### API and Cloud Services
Api stands for application programminhg interface but backend can be only called by the front-end soo if another backend code wants interact with another backend code which is built in another language here API comes out.

API's are language independant and platform independat means transfering data in some format which can be understandable with every programming language soo api returns the data in the form of json.

soo with the another backend language as well we can consume the data just by calling its functions and giving the required inputs and will get the data in the form of json.

<img src="./backend.png" style="width:100%;">


### Types of Api's :-

- **SOAP :-** Simple object acess protocol. 

It transfeer the data in small envolop which will be in the format in XML.


- **REST :-** Representational state transfer protocol.

    In REST api it will be designed for any resource which means create,retrive,update and delete.

    Any resource to be created in which we can create,retrive, update and delete can be performed.

    Methods : 
    - Get
    - Post
    - Put
    - Delete

**NPM (Node package Manager) :-**
    We can install packages and libraries with the help of npm.

- It will create node modules folder.
- It will create package.json and package.lock.json in which installed packages details and dependencies will be present there.


# ------------------------------------------------Practical Starts here-------------------------------------------------

### undefined in node js

As node uses chromes v8 engine soo as we get undefined on the chromes javascript compiler we also get the undefined in the node js as well.

`undefined :-` when any line or statement doesnt return something it will say the undefined as well

### Fundamentals of Node Js

- **How to import and export code :-**

    As we do import and export in the javascript it doesnt run in the nodejs as well bcoz its running the bit lower version javascript which doesnt support the import and exports like angular and react and all.

     - **Solution for imports and exports :-**

        In nodejs we can only export and import only objects.

        **Exporting object :-** We can export object by using `module.export={x:20,y:30}` and we can import this object in the project.

        **Importing object :-** We can import object by using `const filename = require(../app)` and we can use the variable as object in the applications as we can acess the values as well.

- **Filter :-** 

    Filter is array method with which we can filter the data from the array adn return the array with the filtered values.

    **How to filter basic :-**
        we can return the value which we want in the return statement as like mentioned below.
    ```
    let a = [1,2,3,4,5]

    let filtered = a.filter((item)=>{
        return item===3
    })
    console.log(filtered) // returns 3
    ```

### Core Modules

Core modules are the modules are predefined modules where we dont need to write it from scratc. like ex : `fs,console,buffer,http,etc`.

- **Global Module :-** The modules we dont need to import and we can use them without importing is called as global modules.

- **Non-Global Module :-** The modules we need to import it before using it is called as non-global modules.

- **Directory and files :-**
    - `__dirname :-`  it will returns the directory path.
    - `__filename :-`  it will returns the files which are mentioned in the directory.

- **Howt to import module with specific function :-**

    Yes we can import the specific function from the module as like mentioned below.

    `let fsWrite = require('fs').writeFileSync` And we can use it.

### Basic Server and Output on browser

We can create server with the help of http module.

- First we need to import the http and store it in variable like `const http = require('http')`

- Then we have `createServer(req,res).listen(port)` this function will create server which will be running on `localhost:4500/` and `createServer()` will take a call back function the first param will be `request` and second will be `response`.

- Then we can write on the server with the help of `response.write()` function.

- And at the end we need to tell the node js as well where to stop soo we have `response.end()` so it will end the process over there.


```
const http = require('http')

http.createServer((req,resp)=>{
    resp.write("Hello World");
    resp.end()
}).listen(4800);

// This will create server on localhost:4800 port and will show what we written on it.
```

**Most Imp :-** When we make changes in our code will not show on the server we need to rerun the our nodejs server for it.

### Package.json

Package.json holds all the packages information and project information and detials about your project and some commands as well about your project.

**Its most important file of project which should not be deleted never. Else the project will be destroyed.**

- **How to create package.json :-** We can create package.json with the command `npm init` soo it will ask you for project detials and it will create package.json.

- **How to create node modules and package.lock.json :-** Whenever we install any node package in our project package.lock.json and node modules folder will be created.

- `package.lock.json :-` package.lock.json file holds the detial information of packages which you installed in your project and if its deleted whenever we do npm install it will be created again.

- `node modules :-` It will hold the folders of the packages and npm will  automatically install its related and dependant packages as well which will be stored in the node modules folder itself.

- **How to ignore node modules while pushing to github :-** For skipping the node modules folder while pushing the project on github or bitbucket we need to create .gitignore file and in that we need to do `/node modules` soo it will ignore all the node modules folder.

### NodeMon
Nodemon is the node package which will used for time saving purpose and which will work as live reload, we dont need to rerun the files again and again it will do it automatically.

 - **Installation :-** `npm i nodemon`

 - **Use :-** Before we used to use the `node filename` soo rather than it we can use now `nodemon filename` soo it will run the server with the nodemon with live reload.


### How to make simple api

We need to create the api with the `http module` and `createServer` function.

**Most Imp :-** We need to stringify the whatever the data will be we need to stringify it first and then we can use it in `response.write()`. 
 
- First we need to create server with http module.
```

http.createServer((req,res)=>{
    res.writeHead(200,{'content-type':'application\json'})
    res.write(JSON.stringify(dt));
    res.end();
}).listen(4800)
```

- Then we need to write headers like `res.writeHead(200,{'content-type':'application\json'})`


- Then we need to use `response.write(stringified data)`.

ex : 
```
// data File

let data = [{ name: "Shiv", age: "18" },{ name: "Shiv", age: "18" },{ name: "Shiv", age: "18" },{ name: "Shiv", age: "18" },{ name: "Shiv", age: "18" }];

module.exports = data;


// main file
const http = require("http");

let dt = require('./data');

http.createServer((req,res)=>{
    res.writeHead(200,{'content-type':'application\json'})
    res.write(JSON.stringify(dt));
    res.end();
}).listen(4800)
```
























































































<!-- ### How to include preinstalled libraries 

For installing the already installed libraries in the code we use `let var = require(libraryname)` and we can use the library methods on that variable.

### How to create package.json

- `npm init` - It will initialize the node enviornment inside out folder directory it will ask some questions and it will create package.lock.json with our commands.

### File system Module
By using `fs` file system we can do all the file oprations write delete read and all the oprations.

First we need to import `require('fs')` and then we can use all the methods of file system,


- **FileSystem Methods :-**

    1. `fs.writeFileSync(filaname,text)` - It will check the file available or not and then it will create a file containing text we passed in the method above.

    2. `fs.readFileSync(filename,format)` - It can read the data mentioned in the file and it will return string format data.

### Http -->




