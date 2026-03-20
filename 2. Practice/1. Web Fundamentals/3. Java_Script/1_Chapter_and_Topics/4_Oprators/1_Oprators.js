// Oprators in javascript

document.write("Oprators in Javascript");

// Mathmatical oprators
var a = 100;
var b = 90;

console.log("The value of a + b is ", a+b);
console.log("The value of a - b is ", a-b);
console.log("The value of a * b is ", a*b);
console.log("The value of a / b is ", a/b);

//  Assignment oprator
var c = a; // value of a is assigned to C.

//c = 4;//We can change the value of c by without using var to the variable.
c +=2;  // it will add the 2 in the value of c 
c -=2;  // it will substract  2 in the value of c 
c *=2;  // it will multiply the 2 in the value of c 
c /=2;  // it will divide the 2 in the value of c 

// Comparision oprators (It will return the true or false for the compairions)
d = 3;
e = 2;
console.log(d==e); 
console.log(e==d);
console.log(a>=b); 
console.log(a<=b);
console.log(a>b);
console.log(a<b);

// Lofgical Oprators (IT will never return true till both will be true ) (Matlab ye bhi and wo bhi)
// Logical and (&&)
console.log(true && true);
console.log(false && false);
console.log(false && true);
console.log(true && false);

// It will return true if only one value will be true (Ye nahi to ye)

// Logical or (||)
console.log(true || true);
console.log(false || false);
console.log(false || true);
console.log(true || false);

// Logical Not (!) (Sach ko jhuth and jhuth ko sach)
console.log(!false); // it will reverse the value
console.log(!true); // it will reverse the value

