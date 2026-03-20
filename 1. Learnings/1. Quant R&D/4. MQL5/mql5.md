# MQL 5

MQL 5 is programming language used by meta trader for automated trading, tools building & automating small tasks such as position sizing, risk management till building algorithms which will analyse markets by themselves and trade based on it.

### Opening MQL Editor
We can open the mql5 editor via `metatrader 5 > tools > metaquotes language editor`

### How to make it integrable
When we generate the file its just template text file but once we compile it will be availalbe in experts folder in mt5.

Then we can drag the ea to the chart via activating algo trading.

### Properties

We have properties initialised at the start of the programme.

With those properties we can modify the algo version, copy right text, copy right link etc.

We write properties with `#property propertyName` and we have different properties for different purposes.

**Properties :-**
- `copyright :-` This is the copy right text appears on EA popup when we attach it to the chart.
- `link :-` This is the clickable link which is integrated for copyright, it redirects us to that speicified link when we click on copyright.
- `version :-` We get the version appended in EA popup like `learning 1.0` where `1.0` is controlled by version property.

We need to close the MT5 & reopen it so these modified properties will be reflected.

### Comments
Comments are only for refernece only or for the documentation purpose as like other programming languages.

We can write comments as mentioned below

**Comments :-**
- `Single line :-` Single line comments are written with `//comment`
- `Multiline comment :-` we can write multi line comment with `/* multiline comment */`

### Variables

We can create variable with `datatype varName` like `int a` where data type is `int` & `a` is variable name.

**Data types :-**
- `int :-` It stores the negative & positve integer numbers, we cant store values with decimals in this datatype.
- `double :-` We can store the decimal values in it either positive or negative, it takes more space in ram as compared to int.
- `bool :-` We can store `true | false` values in it.
- `long :-` Its similar to integer but we can store bigger numbers in it either negative or positive. It takes more space in ram.
- `ulong :-` Its similar to long but we cant store 0 in it but we can store even bigger numbers in this datatype.
- `string :-` Its used to store the texts, wrapped inside `"string"`

```
// Data Types with variables
int num = 10;
double decimalNum = 1.21;
bool isDay = true;
long bigNum = 123456789;
ulong biggerNum = 12346578901234567890;
string name = "Kosashi Capital";
```

**Arrays**
Arrays are the data types to store multiple variables or values in single variable. we can define array variable with `int num[3] = [0,1,2]` where 3 refers to length or size of array based on which space gets allocated and we can access the elements similar to other programming languages as `int firstVal = num[0]` where index starts from 0 & last index is `-1`.

### Functions & Built-in Events
MQL5 events are functions gets triggered at perticular stage of programme as same as lifecycle methods in angular.

We can write events with `int OnInit(){ return(INIT_SUCCEEDED) }` where `int` is return type of function, we write code inside the `{}` in it.

We can write nested functions as well as mentioned below.

```
int OnInit()
  {
    // Nested Function
    Print("this is the OnInit function...");
   return(INIT_SUCCEEDED);
  }
```
`Note :- We can see the print statements in the experts tab in mql5.`

```
void OnDeinit(const int reason){

    // const defines the arguements is not modifieable, int represents the data type of arguement & reason is parameter name.
    
    Print("Deinit called due to ", reason)
}
```

**Event Types :-**
- `OnInit() :-` This function gets executed when the EA is attached to a chart, recompiled or timeframe changes of the chart.
- `OnDeinit(const int reason) :-` Deinit gets called when program is removed form the chart, chart changed, timeframe changed etc. we have different reason types & its codes we get to know in mql5 documentation.
- `OnTick () :-` This function is called on each & every tick, tick defines the change in price on chart and this function will get called. We need to use this carefully as this will be called on each & every tick. 

**Event Return Types :-**
- `void :-` Returns nothing 
  
  And we can return the data types we have saw in variables section.

### Reference
Reference is the popup window opens with documentation of mql5 and we can use that for understanding of any functionality.

We can open reference popup with via `mql 5 editor > help > mql 5 reference` or with keyboard shortcut `F1` by keeping cursor of any function.

### Indicator Methods
We have different methods for indicators, we can use it with `iATR(params)`, when we type `iATR(` it suggests its parameters & we need to pass it, we need to keep in mind that return type of indicator method with variable data type.

```
int atr;

int OnInit(){
    // It will return atr value to atr variable.
    atr = iATR("EURUSD", PERIOD_M1, 14)
}
```
### Indicator Handle
Indicators descriptions are stored in ram of our memory, whenever we are using any indicator & storing its reference to variable it references to the indicator handle.

```
int handleAtr;

int OnInit(){
    // It will return atr value to atr variable.
    handleAtr = iATR("EURUSD", PERIOD_M1, 14)
}
```

**Indicator Params :-**
- `int start_pos` - Every candle holds its index last bar in chart have index 0 & its increments wiht 1 to previous bars.
- `int count` - It refers how much number of candles we need to consider in past if we need to consider 3 candles then we pass 3 likewise.

### Buffer (CopyBuffer)
Buffer is the value of indicator per candle, if we want to see it visually we need to insert indicator like ATR to chart & view data window. Now if we hover over any candle with cursor or crossair we can see the buffer value for that indicator in data window.

We can copy that buffer value for indicator with `CopyBuffer(params)`.

### Dynamic Trading Symbol

As we have used `EURUSD` in earlier code `handleAtr = iATR("EURUSD", PERIOD_M1, 14)` and whenver we want to apply this EA to new chart we need to edit again.

Instead if we want symbol to be taken based on applied chart we need to pass `NULL` like `handleAtr = iATR(NULL, PERIOD_M1, 14)`.

### Candle Size or Params (Open, Close, High, Low)

We need to get candle params for current, previous or last some candle then we need the candle params for executing our quantative logic so we will need the following built-in functions most of the time.

**Candle Functions :-**
- `iOpen(params) :-` This gives open price of candle according to params.
- `iClose(params) :-` This gives us close price of candle according to params.
- 

### User Inputs
We need dynamic user input or input should be decided by the user to make EA more dynamic.

We can do that by adding `input varName` so this field will be visible in the inputs of the EA.

We use Capitalised case for user inputs like `Timeframe` rather than `timeframe`

### Enums

There are some predefined enums or values we need to enter and we that should match the mql 5 enum its called as enums.

Ex : 
We want to take timeframe used for the EA from user but it cant be enter in plain text field so we can take user input along with enum as mentioned below.

`input ENUM_TIMEFRAME timeframe = PERIOD_M1`

In the above example PERIOD_M1 is default value which will be overridden by user input.

### Conditional Statements
We have conditional statements in mql5 as well as like other programming languages where we want to check conditions which returns `true | false`. 

The syntax for conditional statements as mentioned below.

**Logical Operator :-**
- `> | <` - Less than or greater than to compare the numeric or floating values.
- `==` - Equals to to compare if x value is equal to y.
- `<= | >=` - Less than or greater than to compare numeric or floating values.
- `&&` - And symbol to combine multiple conditions.
- `!=` - Not equal to.

```
if(open < close){
     Print("Green Candle");
   }else if(close < open){
      Print("Red Candle");
   }else{
      Print("Else Case");
   }
```

### Loops
Loops are the same as for loops in other programming languages to make repetable operations for multiple elements.

**Syntax : :-**

```
for(int i = 0; i < PositionsTotal(); i = i+1){
    // Logic for updating the orders or closing the orders which we will see in next sections.
}
```

`PositionsTotal()` returns total number of active positions in the toolbox if we want to loop over all the positions.

Positions are indexbased starts from zero.


### Place trades
In MQL5 we can send open buy or sell order as well programatically as well which we will study in this section.

If we want to open the order traditionally in mql 5 there is very big payload, to simplify it we have one package which we need to include like `#include <trade/trade.mqh>`.

We will only deal majorly with the package class as `CTrade` and we need to create variable for it with `CTrade trade;` which we will use for opening orders.

**Orders :-**
- `trade.Buy(lotSize)` - This opens the buy trade at market price.
- `trade.Sell(lotSize)` - This opens the sell trade at market price.

**Note - rest of the params taken by default form the package, if we want limit orders or pass the custom params then we can pass it manually.**

**Advanced Params :-**
In this section we will provide more params to buy or sell orders.

Order Params : `trade.Buy(volume,symbol,price,sl,tp,comment)`

1. `volume` - Lotsize can be calculated dynamically or can be taken from user.
2. `symbol` - we can use `NULL | _Symbol` to refer to current chart symbol.
3. `price` - for getting the price we can use some logic as mentioned below.
   1. We can create variable as `entryPrice` with `SymbolInfoDouble(symbol, enum_param)` through which we can get bid, ask and other params from the symbol ie `double entryPrice = SymbolInfoDouble(NULL,SYMBOL_ASK)`
   2. Sometime very precise or accurate values create unwanted problems for opening order so we can round it with `entryPrice = NormalizeDouble(entry,_Digits)` where `_Digits` holds value of digits available after decimal for current chart pair.
4. `sl` - we need to provide sl price of it, we can calculate with pips or points with entry price like `double sl = entryPrice - 100 * _Points` where we can take the tp points form user itself as input.
5. `tp` - we need to provide tp price of it, we can calculate with pips or points with entryprice like `doulbe tp = entryPrice + 100 * _Points` where we can take the sl points from user itself as input. 
6. `comment` - if we want to provide any comment for the order.


### Prevent Order placement on every tick
We have function `iBars(params)` returns the total bars available on chart, Now to run the logic only on new candle completed then we have small logic as mentioned below.

****
- Create global variable as `int totalBars = iBars(NULL, timeframe)` in `OnInit()` which returns total bars avaialble on chart.
- Create local variable as `int bars = iBars(NULL, Timeframe)` in `onTick()` function which will return latest value of totalBars.
- Bars value will not match if new bar created so we compare if `totalBars!=bars` which means new bar created we update the `totalBars` and run the logic under that if statement.
- So our logic written inside the block will be only executed on new candle creation.


### Modify the trades

**Get Position Details :-**

For modifying the position we need to get the position ticket with `ulong posTicket = PositionGetTicket(index)` when we execute this statement position of that index gets selected due to which we can access other details such as `PositionGetDouble, PositionGetInteger, PositionGetString` ie if we want to get openPrice of position we can get by `double posOpenPrice = PositionGetDouble(POSITION_PRICE_OPEN)`.

If we want to check if position is type of buy or sell we can get by `PositionGetInteger(POSITION_TYPE)` which returns inteter, we can compare that with enum `POSITION_TYPE_BUY | POSITION_TYPE_SELL`.

**Position Modification :-**
`trade.PositionModify(posTicket, sl, posTp)` where we need to pass the position ticket stored in variable, new sl & new tp to which we want to modify the position.


### Magic Number
Magic number is the concept which is unique number used for unique ea orders, not to operate on all the orders. ie if we have 2 ea's running, a & b, and we want to modify the order only for ea a but dont touch positions opend by b then we can identify the positions for EA a by magic number.

**How to implement magic number :-**
- Create `int input MagicNumber;` where user will enter magic number for this ea.
- In `OnInit()` method set the magicNumber to CTrade class like `trade.SetExpertMagicNumber(MagicNumber)`
- Check the condition before modifying the order like `if(PositionGetInteger(POSITION_MAGIC)!=Magic) continue;` which means loop will not execute below statements or code block if magic number doesnt match.

















  
