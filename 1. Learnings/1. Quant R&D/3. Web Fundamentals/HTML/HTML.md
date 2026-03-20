<h1 style="text-align:center">Brief about the HTML Tags</h1>

1. <img src ="" height="" width="" alt="" id="" name="" class=""/>

src = source(for providing the source of the image) , alt = alternative (if image will not be shown then what should be text)
height = we can give the height of the image inside the html element.
width = we can give the width of the image inside the html element.

2. Tags inside the head tag are for the browsers information understanding for the browsers.
   =>  `<style></style>` = Usefull to provide styling to our webpage.
   `<meta name="author" content="shiv">`

   <script></script> = usefull for provide js to the webpage.

   `<link rel='' href=''>` = usefull to provide external links to the webpage.
   `<link rel='' href=''>` = { rel=relationship , href=Hypertext refrence}
3. `<meta charset = 'utf-8'>`
   =>  Meta tags are information about page
   charset describes which charecter are allowed on the webpage
   utf-8 stands for = unicode transformation format
4. <pre></pre>

=> Pre tag is used to preserve our indentations spaces symbols as it is on the webpage.
`<pre>`
This is the
Intended
Text...
`</pre>`

5. h1,h2,h3,h4,h5,h6
   => All are the headings tags in the html.
   all heading tags starts on the new line and they are block level elements and take 100% heading.
6. <p title="This is the title"></p> {p = paragraph tag}

=>  p tags are used for any kind of the text on the webpage
title attribute = it will give us the popup of that text we putted in the title attribute.

7. <div hidden></div> and <span></span>

=> Both are container type of tags but :
1. div is the block level element = takes 100% width and blocks the space left and right of the div.
2. span is the inline level element = only takes space only as per the content and required.

```
hidden attribute = element will not be visible on the page it will hidden. 
```

8. <select></select> and <option></option> tag

=>  select tags = created dropdown for us and it will show the options below mentioned in the option tag
option tag = option tag became option of that dropdown line by line as we mentioned.

9. <option selcected disabled></option>

=>  selcected attribute = show the default selceted option on the webpage
disabled attribute = disable the option and it cannot be selcected it will apper there but with low opacity which indicates it cannot be selcected.

Forms are used to create contact forms and lead genration forms

1. div

=>  div  =  creates everything on the next line

```

```

span = creates in front of elements

2. <input type= "text" > </input>

=>  input tag creates input box for the forms.
text attribute = text attribute allowes values which values are allowed in that input box.

3. List of attributes {text, number, date, file,password.image etc...}
   =>text = allows us to give the input in the text form.

   number = allows us to give the input in the number.

   date = allows us to give the input in the date.

   file = allows us to give the input in the file by opening your local directory.

   password = it will not show the text and it will show the text as . or *.
4. input attributes {maxlenth, minlenth,name,value,required,selected,disabled,hidden,checked}
   =>  minlenth = it will submit the input only if length will be greater than minlenth.

   name = it will provide identity to that input element and it will helpful in js to access the elements in the form.

   value =

   1. it provide value to thigs like button and all,if we provide the value to some input element it will apper in the element on the screen.
   2. we can provide the value to the kind of element where user cant provide value else it makes selection in such tags like radio,option,checkbox and all we can get the users input in the selections in the form of perticular value by providing value to html element.

   required = it wont allow to submit the form without filling the details and it will show a popup on the screen "field cannot be blanked"

   selected = selected attribute make selection of option or checkbox or radio button by default which appers on the screen but user can change it.

   disabled = user can see the value but cannot choose it it will turn into fent grey text which cannot be selected.

   hidden = element will exist there but it will not be visibel to user.

   maxlenth = it will submit the input only if length will be lower than maxlenth.

   checked = it will check the thigs by default as per our choices.
5. input types = {button,text,date,number,password..etc}
   ==> each type attribute have their different values and apperance on the webpage.
   type can make the element different from others
   we can take different kind of inputs from the user
6. `<label>`First Name`</label>`
   ==> as we know it is harder to style the content which is not in some specific tag soo by using lable we can style it as well and we can give label to the input element.
7. <textarea></textarea>

==> This element creates a input box greater than input tag and we can provide the longer text than normal to it

8. <input type="radio" name="gender"><input type="radio" name="gender">

==> we can make selection to the only one by providing the same name to the radio button.

9. `<span><label>`First Name`</label>`
   ==> We can provide label inside the span tag soo the text will automatically come beside the input element.
10. <fieldset></fieldset>

==> We can provide the border and sectionize the form by fieldset tag.

11. <fieldset> <legend>Personal Details</legend></fieldset>

==> inside that border we can give the name of the section or we can add text inside that borde by legend tag inside the fieldset.

12. `<button></button>`
    ==> We can make simple buttons for different functionalities by button tag.
13. <input type="submit">

==> By pressing enter button submit button will automatically oprate and page will reload.

14. `<input type="reset"></input>`
    ==> type reset will reset the form values as default when the button is pressed.
15. <button name="click" form="form1"(id of associated form)>

==> it will associate this button to the nearest ancestor form if we dont provide the form id in the form attribute.

16. `<input type = "text" maxlen="" minlenth="" required>`
    ==> to show the msg related to the maxlen you have to give the attribute required to that input element.
17. we cannot provide the value to the textarea and some other input elements if is it given it will not appear on the screen.

# User Strories

### 1. Anchor Tag

`<a href=""><a>`

**Anchor Tag is used to Navigate the user inside the page or outside of the page**

- Used to add external or internal links to the word.
- we can focus inside our page on some element by providing its id inside the href.

1. **Website**
`<a href="https://google.com">Website</a>`

2. **Email**
`<a href="mailto:shivkounsalye@gmail.com">Email</a>`

3. **Phone**
`<a href="tel:+918421289433">Phone</a>`

4. **To focus on some part**
`<a href="#footer">`Go to footer `</a>`


### 2. HTML Lists

`<ul> <li></li> </ul>`
`<ol> <li></li> </ol>`

**HTML lists are used to show lists of anything on the webpage you can use html lists.**

- ul = Unordered list

- ol = Ordered list

- li = list item
  
**- Manipulation of unordered list**
   
   1. We can manipulate the list numbering style by giving type attriute.
- disc = Normal filled black circle
- square = Normal filled black square
- circle = unfilled bordered circle


**- Manipulation of ordered list**
1. We can manipulate the list numbering style by giving type attriute.
 
    `<ol type="1"></ol>`
    - "1" = Numbering system
    - "a" = Small alphabetical order
    - "A" = Capital alphabetical order 
    - "i" = Small roman numbering order
    - "I" = Capital roman numbering order


2. We can start numbering from any perticular number in any kind of numbering style.

   `<ol type="1" start="5"></ol>`
   
   By providing the value inside the start attribute list numbering will start from there.

### 3. Iframe tag
`<irame src="https://www.wikipidia.com"></iframe>`

- Used to add a whole website to our page in a box.
- we can add another our webapge to it.



