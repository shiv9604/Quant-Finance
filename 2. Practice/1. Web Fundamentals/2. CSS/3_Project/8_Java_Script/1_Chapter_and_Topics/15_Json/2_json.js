// JSON (Javascript object notation )
obj = {name:'shivprasad'};
console.log(obj ,typeof(obj));

// stringify => (stringify changes the datatype of obj into string)
// JSON format requires only doublequotes ("") 
json1 = JSON.stringify(obj);
console.log(json1, typeof(json1));

// parse => (parses the "string" into javascript object) converts the valid string into object
parsed = JSON.parse(json1);
console.log(parsed,typeof(parsed));

// String formatting
// we can replace the var in string.
a = "Shiv"
document.write(`My name is ${a}`);