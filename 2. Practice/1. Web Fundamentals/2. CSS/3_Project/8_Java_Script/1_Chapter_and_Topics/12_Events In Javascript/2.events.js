// Events in the javascript (All the actions taken by the client side users on the webpage called as events)

// 1.Button click event ('click')
function clicked(){
    // console.log("Click hua");
    document.write("The button is clicked \n");

}

// 2. page reload event in the webpage ('onload')
window.onload = function(){
    document.write('Page Reloaded');
}


// 3. Button event addition by targeting the button by its id and adding event in it. ('click')
// We can directly acces the element by its id

container.addEventListener('click',function(){

    console.log('click hua');
});

btn.addEventListener("click",function(){
    document.write("Button Clicked");
})

// 4. Mouse over event ('mouseover)
container.addEventListener('mouseover',function(){
    // console.log("Mouse Hovered on the container");
    container.style.backgroundColor = 'Teal';
    container.style.color = 'white';
    
})

// 5. Mouse out container
container.addEventListener('mouseout',function(){
    // console.log("Mouse Hovered out of the container");
    container.style.backgroundColor = 'black';
    container.style.color = 'white';
})

// 6. when we loose the mouse click
container.addEventListener('mouseup',function(){

    console.log('click chod diya');
});

// 7. Mouse Hold event
container.addEventListener('mousedown',function(){

    console.log('click Hold  Kiya');
});


// Change the HTML on click (when we hold the the mouse click)
container.addEventListener('mousedown',function(){
    // In Query selector you must enter css selector or Class.
    document.querySelectorAll('.container')[0].innerHTML = "<h1>Mouse click Holded on the container</h1>";

});

// Change the HTML on click (when we leave the mouse click)
container.addEventListener('mouseup',function(){
    // In Query selector you must enter css selector or Class.
    document.querySelectorAll('.container')[0].innerHTML = "<h1> Mouse click left From the container</h1>";
    
});
