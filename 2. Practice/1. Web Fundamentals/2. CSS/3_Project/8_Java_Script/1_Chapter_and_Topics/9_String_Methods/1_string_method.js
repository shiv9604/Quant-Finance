// String Methods

var str = "Shiv is a front-end devloper";

// String Methods

// 1.lenth method (Gives us the lenth of sting including spaces)
console.log(str.length);

// 2. Indexof Method (Gives the first index of  the first charecter or word including spaces)
console.log(str.indexOf("front"));
console.log(str.lastIndexOf("front")); // gives the last occurance of the word or charecter

// 3. String slicing (It will give us the part of string about which we mentioned the values of its index)
console.log(str.slice(0,18));


// 4. Replace method in string 
var replaced_str = str.replace("front-end", "back-end");
console.log(str);
console.log(replaced_str);
