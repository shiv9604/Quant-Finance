# CSS

CSS stands for casacading style sheets which styles our web(HTML) page by using different various properties.

### How to add CSS to our HTML Files

- Inline CSS :

  Which we include in style attribute in HTML tag in opening part like `<h1 style="color:red"></h1>`.

- Internal CSS :

  Which we include inside the `<style></style>` tag inside the head tag.

- External CSS :

  In which we create **style.css** file
  and we link that file through
  `<link rel="stylesheet" href="style.css">`

### CSS Selectors

We have 3 types of CSS selectors as mentioned below.

- Class Selector :

  we can select the element by its class by **.header** as like mentioned below `.header{color:red;}`.

- ID Selector :

  we can select the element by its id by using **#header** as like mentioned
  `#header{color:red;}`.

- Element Selector :

  We can select the elements by simply element name and properties inside the **{}** like `h1{color:red;}`.

- Universal Selector :

  we can apply one style to the all the elements in our webpage universally by using **\*{font-family:sans-serif}**.

- WE can group the sectors by just putting **,** in multiple classes,id's and elements. like

  **h1,.header,#footer{color:black;}**

### Dimensions in CSS

Dimension properties in CSS are for providing the dimensions to the HTML elements like **`height,width,max-width,min-width,max-height,min-heighyt`** to an HTML Container or elements.

- height : It provides height to the elements.
- width : It provides an width to the element.
- max-width : It provide the maximum width to the HTML element.
- min-width : It provide the minimum width to the HTML element.
- max-height : It provide the maximum height to the HTML element.
- min-height : It provide the minimum width to the HTML element.

### Display in CSS

By default we have most of the elements are block level elements in HTML expecting the span. To manipulate their displays on the webpage we use the display properties.

We have display properties as like mentioned below : 

- **`block`** : It's a by default display property to all the HTML elements. Block level elements will takes all the 100% viewport width and we cannot place any other element beside that.

- **`inline`**: In inline elements we can place elements next to the one other and it will take the only required width as per element. And in the inline element we can't provide height,width,margin,padding to the element.It will take automatically as per the content available in the HTML element.

- **`inline-block`**: In inline block elements we can place elements next to the one other and it will take the only required width as per element. And in the inline element we can provide height,width,margin,padding to the element.

- **`none`** : In the display none property the element the element will not exist anymore on its position and other element can take its space.


### Background in CSS

- **`background-color:red`** - It provides the backgeround color to the element.

- **`background-image:url(path)`** - We can add the image to the background of element.

- **`background-repeat:repeat-x;`** - By default when we give the image to the background it will repeat all the way horizontally and vertically as per its size but we can control the repetation of the image by this property in **`repeat-x`**,**`repeat-x`** and **`repeat-x`**.

- **`background:color url(path) no-repeat right top`** - this is the shorthand property for the background and we can all assign into one single property.

### Position in CSS

We have CSS positioning properties to position and HTML element like **static**,**relative** and **absolute**.

1. **`position:static`** - It will place the element as per our given order line by line or inline.

2. **`position:relative`** - It doesn't make any changes to their placements but we can apply properties like **top,bottom,left,right** to move its from its rendered positioned but the place will be reserved as it is over their.

    **It will apply top left and all to its rendered position.**

3. **`position:absolute`** - **First of all its reserved place will be taken by other by considering nothing exists at that positon.And Second thing will be it we can apply top,left and all values to it which it will apply first positioned ancestor Which will be *<u>non-static</u>* HTML by default soo it will be positioned from the browsers window and when it will be in a container which will be postioned it will apply those values from it bcoz first positioned parent ancestor will be its parent container.**

4. **`postion:fixed`** - When we give the position as fixed it will be fixed over their at any cost like scroll or anything else we can see that bcoz its fixed over their.

### Z-index in CSS
Z-index is the property to stack your positioned elements in z-axis.

We can only apply the z-index property to the positioned elements with the following properties:
- relative
- absolute
- fixed

```
<div style="position:absolute;z-index:1;">
</div>
```

### Font Styling in CSS
We can achieve font styling in the CSS by this following properties.

We have font-styling properties as like mentioned below : 

- **`font-family`** : We can provide font-family to the text like arial,noto-sans and all.

- **`font-style`** : We can provide the styline like italic and all with the font-style property.

- **`font-size`** : We can provide the font-size to the HTML paragraphs and heading and all.

- **`font-weight`** : By providing this property we can control the boldness of the fonts in the values from **100-900**.

- **`text-align`** : We can achieve the horizontal alignment of the text in the container with the help of text-align property.

### Border in CSS

We can provide border to the HTML elements by this property.

We have following properties for the border-styling.

- **`border`** : We have border shorthand in which we can provide the border properties values in single property as like mentioned below.
```
<div style="borde:1px solid red"></div>
```
So we are providing the border-size,border-style,and color for the border above.

### CSS Box Model

We have CSS box model in which we get to know how the margin-padding works on an HTML element.

We just need to remeber the sequence : 
- M : Mere  (Magin- Top most layer on the element)
- B : Bhai (Border - Outer layer of the content)
- P : Padhle (Padding - The layer between content and border)
- C : Chote (Content - Inner most part of the box-model)

### Margin in CSS
We can move one element from the another element with the margin property which have values as like mentioned below.

- margin-top : It provide the spacing from the top to the element. 

- margin-bottom : It provide the spacing from the bottom to the element. 

- margin-left : It provide the spacing from the left to the element. 

- margin-right : It provide the spacing from the right to the element. 


### Padding in CSS
We can move one element from the another element with the padding property which have values as like mentioned below.

- padding-top : It provide the spacing internally from the border till the conent from the top to the element. 

- padding-bottom : It provide the spacing internally from the border till the conent from the bottom to the element. 

- padding-left : It provide the spacing internally from the border till the conent from the left to the element. 

- padding-right : It provide the spacing internally from the border till the conent from the right to the element. 

### Grid Systems in CSS




### Media Queries in CSS

Media queries are the key features and properties to use while making our webpage responsive on all screen sizes there the media queries used.

We can use the media queries with **@media(){}** and in the brackets the condition will goes and in the curly braces the css for multiple elements or for the whole page goes by targeting the elements with their id's.

Ex : 
```
@media (max-width:550px){
  body{
    background-color:black
  }
}
```

**Media Queries functionalities** : 

  Media queries can be apply for the functionalities like `screen, speech , print` soo with the parameters the media queries will be apply to that perticular functionality while in opration like if we want to apply the css another for printing the page then  the CSS will be like mentioned below.

```
@media print{
  body{
    color:red;
  }
}
```
When we will try to print the page it's background color will be black as per mentioned css.

**Media Queries for landscape** : 

  We can apply the media queries for the landscape device as well.

  **Landscape** : The Screen size in which width will be greate than height will be landscape device.

  We apply the media queries for the landscape devices with `@media (max-width:500px) and (orientation:landscape){}` like this.

  Ex : 
  ```
  @media (max-width:500px) and (orientation:landscape){
  body{
    color:red;
  }
  }
  ```

## BootStrap (CSS FrameWork)

Bootstrap is the css framework by twitter which is their style sheet and which they made available globally for the devlopers and we can use that by including the bootstrap in our HTML page and by simply adding their classes to our HTML elements.

**Ways to add bootstrap to our webpage** : 

1. **CDN links** - Just include their CSS and JS file in our links.


2. **Downloading bootstrap locally** - In this we download stylesheet in our computer and we use that in our HTML.

### Colors in Bootstrap
- Blue : `text-primary`
- Grey : `text-secondary`
- Green : `text-sucess`
- Red : `text-danger`
- Black : `text-dark`
- Light Grey : `text-muted`

### Color with Background
- Orange color with black background : `text-warning bg-dark`

- Teal color with black background : `text-info bg-dark`

- White color with black background : `text-light bg-dark`

- Orange color with black background : `text-warning bg-dark`

- Orange color with black background : `text-warning bg-dark`

### Alerts in Bootstrap
Alerts are the alert boxes which most of the websites use for their alerts.

alert : `alert`

And We can customize our colors of our alerts by simply adding one more class like `alert alert-primary` next class will work for the **color** of the alert.

### Buttons in Bootstrap

**Types of Buttons in Bootstrap**

- **Normal Buttons** : Normal buttons with class **`btn`** are the simple buttons with the text and styling as per the class **`btn btn-primary`** we are providing.

- **Outline Buttons** : Same as the normal buttons **`btn`** with the class for styling and outline with the class **`btn btn-outline-primary`** which will have hover effect.

- **Button-Sizes** : We can just handle the sizes of button with the extra class like:
    
    - **Small** : `btn btn-primary btn-sm`.
    - **Normal** : By default its  size is normal.
    - **Large** : `btn btn-primary btn-lg`

Colors can be applied for all the buttons by the `btn-color` class.

### Bootstrap Cards
You Dont need to create cards by your own,You can just copy paste cards and edit its content and image.

### Image slider in bootstrap (Carousel)
**Carousel's** is the image slider provided by bootstrap by just simply copy pasting the component for our image slider and there are various crousel's are available and we can use it accordingly as per our requirement.

##  Grid system in Bootstrap 

***(Most-Important class of the bootstrap)***

### Containers In Bootstrap

- **.container** - which sets a max-width at each responsive - breakpoint 

- **.container-fluid** - which is width: 100% at all breakpoints

- **.container-{breakpoint}** - which is width: 100% until the specified breakpoint


### Grid in bootstrap

**Bootstrap have 12 columns in a row.**

- **.row** - We can create row

- **.column** - We can create column inside that row

Bootstrap will automatically grasp the rows and columns automatically.

We can use the columns or cover the columns like colspan by simply adding classes like **col-3** it will cover 3 columns in a row.

### Responsive layout in bootstrap

We can make our layout responsive by just simply manipulating classes and handling their values of column widths on various types of devices.

Devices as per its size and its classes as follows : 

- Extra Small Devices : **Mobiles - xs(<576px)** - **`.col-`**

- Small Devices : **sm(≥576px)** - **`.col-sm`**

- Medium Devices : **md(≥768px)** - **`.col-md-`**

- Large Devices : **lg(≥992px)** - **`.col-lg-`**

- Extra Large Devices : **xl(≥1200px)** - **`.col-xl-	`**

- Extra Extra Large Devices : **xxl(≥1400px)** - **`.col-xxl-`**

### Bootstrap Modal
Bootstrap modal is nothing but the alert box with features and we can use that by simply copy pasting the component and modifying it.


### Bootstrap Jumotron
Jumbotron is the hero text of the website and we can refer the bootstrap docs for it.

### Bootstrap components

**We have multiple components in bootstrap.**

Maybe it will even increase in future just learn them accordingly as per your need. 

### Margins and Paddings in Bootstrap

We can give margins and paddings in bootstrap itself as follows : 

- **m** : Margin
- **p** : Padding

**Sides for margin and paddings in bootstrap :**

- **t** : Top
- **b** : Bottom
- **s** : Start (Left)
- **e** : End (Right)
- **x** : Left and Right Both
- **y** : Top and Bottom Both
- **blank** : for classes that set a `margin` or `padding` on all 4 sides of the element

**Sizes for margin and padding**

- **0** - for classes that eliminate the margin or padding by setting it -to 0
- **1** - (by default) for classes that set the margin or padding to     $spacer * .25
- **2** - (by default) for classes that set the margin or padding to     $spacer * .5
- **3** - (by default) for classes that set the margin or padding to     $spacer
- **4** - (by default) for classes that set the margin or padding to     $spacer * 1.5
- **5** - (by default) for classes that set the margin or padding to     $spacer * 3
- **auto** - for classes that set the margin to auto

### Flexbox in Bootstrap

We can make any component display flex with only bootstrap as mentioned below.

- d-flex : display flex
- justify-contnet-center : make justify content center
- align-contnet-center : make align content center

### Order of items in bootstrap

We can change the orders of div's in the same container by using : 

**order-md-1** - It will set the order as per the devices we gave or it will aply to the current device size.

### Bootstrap Flex

