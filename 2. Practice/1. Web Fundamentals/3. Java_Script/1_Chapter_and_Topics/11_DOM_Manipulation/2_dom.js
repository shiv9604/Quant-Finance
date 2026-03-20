//DOM = Document Object Model

// document.write("Hello World!");

// 1.  Location (It will give us the location of the document )
// document.location;

// 2. Click on on the button by using the js
// document.getElementById('click').click();

//  3. Style Element (We Can give the styling to the element in js by this way)
// document.getElementsById('click').style.border = '2px solid red';

// 4. ID will be the unique value of the HTML element.
// document.getElementsById('click').style.border = '2px solid red';

// 5. We can do anything with the DOM

// 6. How to add class inside the element
// var item =  document.getElementsByClassName("container"); // we need to put the double semicolon here while targeting the classsbname
// console.log(item);

// item[0].classList.add('item_container');
// item[0].classList.remove('container');

// 7. To Get ineer HTMl of any class
// console.log(item.innerHTML);

// 8. To Get ineer Text of any class
// console.log(item.innerText);

// 9. Get element by tagname
tag  = document.getElementsByTagName('div'); //it wil give all the div's inside our webpage 
console.log(tag);

// 10. Create HTML element in DOM (Append Child)

createdElement = document.createElement('h3');
createdElement.innerText = "This heading is create in Javascript";

tag[0].appendChild(createdElement);

// 11. Remove the HTML Element in DOM.
createdElement2 = document.createElement('p');
createdElement2.innerText = "This Paragraph is create in Javascript";

// replaceChild() = (New element, old element)
tag[0].replaceChild(createdElement2,createdElement); 

// 12. removeChild() = (element to remove)
tag[0].removeChild(createdElement2); 

// 13. document.title => Returns the title of the document 
document.title

// 14. document.URL => gives us the URL of the webpage 
document.URL

// 15. document.scripts => gives us the all the scripts in the webpage
document.scripts

// 16. document.images => gives us the all images inside the webpage.
document.images

// 17 document.forms => gives us the all forms inside the webpage.
document.forms

// 18. document.domain => gives us the domain of the webpage without port and all.
document.domain

// 19. Query Selector => returns us the elements as per selectors

select = document.querySelector('.container');
console.log(select);

// 20. all Query Selector => returns us the nodelist of the elements as per selectors
select = document.querySelectorAll('.container');
console.log(select);






