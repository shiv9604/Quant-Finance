// Loops in javascript

// Most imp thing to be remember is we need to put the ; after on term in for loop statement instead of ,

// sturcture = for(initialize;condition;step){}
// for(var i=0;i<10;i++){
//     console.log(i);
// }

// for each loop  best for arrays

// var arr = [1,2,3,4,5,6,7,8,9,10];
// console.log(arr);

// Its bit complicated we need to close the bracket of statement after the loop the end
arr.forEach(function(element){
    console.log(element);
})

arr.forEach(function(element){
    console.log(element);
})
// while loop which is a type of loop and its just syntax is bit different
// let i = 0;
// while(i<10){
// console.log(i);
// i++;
// }

// do while loop just the difference of syntax nothing else. (it will run at least once even after condition will be false as well. )
// do {
//   console.log(i);
//   i++;
// } while (i < 10);

// break statement (which stops the running of loop if condition meets or when condion will be true)
    
// for(i=0;i<10;i++){
//     if(i==3){
//         break;
//     }
//     console.log(i);
// }

// continue statement (it will continue the statement loop by skipping below part when condition will be true )

for(i=0;i<10;i++){
    if(i==3){
        continue;
    }
    console.log(i);
    }