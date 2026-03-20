// Set Timeout and Intervels

// 1. Arrow function (It will create function with the different syntax)

function sum(){
    return a+b;
}
sum = (a,b)=>{
    return a+b;
}
sum = (a,b)=>{
    return a+b;
}


// 2. SetTimeout for any element in the webpage. (We set time in miliseconds ms 1sec = 1000ms) function = a = ()=>{statement}
// it will print after 2 seconds
greet = ()=>{
    console.log("Good Morning!");
}
// setTimeout(greet,2000); //2000 is value in ms.


// 3. IF we want to repeat any thing after certain time continouesly soo we can use setinterval.
// it will print after 2 seconds and it will repeat after 2 seconds.
// setInterval(greet,2000); //2000 is value in ms.

// 4. How to stop setintervel ?

// clearIntervel function = if a = setIntervel(greet,2000); it will return a id soo we need to put that in the clearintervel()

// 1. even if we putted in variable setInterval will automatically fire in the webpage.
clr = setInterval(greet,2000); 

// 2. When we need to stop the timeInterval then We need to pass the var inside the clearInterval(clr)

// clearInterval(clr);

// clearInterval and  clearTimeout used for clear timeout and intervals.







