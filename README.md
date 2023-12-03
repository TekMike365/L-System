# L-System

A small project, visualizer of [fractals](https://en.wikipedia.org/wiki/Fractal) described in [Lindenmayer System](https://en.wikipedia.org/wiki/L-system), hence the name.

* [L-System scripting language](#l-system-scripting-language)
    * [Comments](#comments)
    * [Special Characters](#special-characters)
    * [Axiom](#axiom)
    * [Rules](#rules)
    * [Variables](#variables)
    * [Settings](#settings)
    * [Example Script](#example-code)
* [Running the script](#running-the-script)

\* This project is work in progress. What you see now, will change at some point.

## L-System scripting language

* extension: .lsys

L-System is a system that describes fractals using a short notation. This scripting language is almost a one to one representation.

### Comments

```
; I think this is self explainatory.
```

### Special Characters

L-System uses characters to represent many acions. Here are all the symbols explained.

```
Character        Meaning
==========================================================================
   F             Move forward by line length drawing a line
   f             Move forward by line length without drawing a line
   +             Turn left by turning angle <angle>
   -             Turn right by turning angle <angle>
   |             Reverse direction (ie: turn by 180 degrees)
   [             Push current drawing state onto stack
   ]             Pop current drawing state from the stack
   #             Increment the line width by line width increment <winc>
   !             Decrement the line width by line width increment <winc>
   @             Draw a dot with line width radius
   {             Open a polygon
   }             Close a polygon and fill it with fill colour
   >             Multiply the line length by the line length factor <lfac>
   <             Divide the line length by the line length factor <lfac>
   &             Swap the meaning of + and -
   (             Decrement turning angle by turning angle increment <ainc>
   )             Increment turning angle by turning angle increment <ainc>
```

Any lowercase or uppercase letters that are not __F__ or __f__ are also a special characters and they can be used as place holders or fractal expandors ([more](#rules)).

### Axiom

__Axiom__ describes the starting characters.

```
axiom <expr>  ; <expr> is any set of characters
```

### Rules

__Rules__ describe how the fractal grows, or how are the characters replaced.

```
rules
    X -> +FY,   ; 'X' gets replaced by '+FY'
    Y -> -FX    ; 'Y' gets replaced by '-FX'
```

### Variables

Yes, variables. Even if this language doesn't seem like it needs variables, I've added them anyways. Variables are always usefull.

```
; variables start with a dot
.name <expr>     ; <expr> any set of special characters

axiom F.name+    ; usage
```

### Settings

__Settings__ are used to specify how the fractal should be drawn. So far I've implemented these settings.

```
angle   ; angle in degrees (+, -)
winc    ; width increment (#, !)
lfac    ; line factor (>, <)
ainc    ; angle increment ('(', ')')
```

You use them simply.

```
<setting> <value>
```

### Example script

An example code of a fractal tree.

```
;       Fractal Tree

; variables
.left +FX
.right -FX

axiom FX    ; setup

rules
    X -> >[.left].right

; settings
angle 40
lfac 0.72
```

## Running the script

```shell
python lsys.py <script.lsys>
```
