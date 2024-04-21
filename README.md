# L-System v1.0

A small project, visualizer of [fractals](https://en.wikipedia.org/wiki/Fractal) described in [Lindenmayer System](https://en.wikipedia.org/wiki/L-system), hence the name.

- [L-System 0.1](#l-system-01)
  - [L-System scripting language](#l-system-scripting-language)
    - [Comments](#comments)
    - [Special Characters](#commands)
    - [Axiom](#axiom)
    - [Rules](#rules)
    - [Variables](#variables)
    - [Settings](#settings)
    - [Example script](#example-script)
  - [Running the script](#running-the-script)

## L-System scripting language

L-System is a system that describes fractals using a short notation. It composes of (axiom)[#axiom], (rules)[#rules] and (settings)[#settings].

```
extension.lsys
```

### Comments

```
; I think this is self explainatory.
```

### Commands

```
Character        Meaning
======================================================================
   F             Move forward by line length drawing a line
   f             Move forward by line length without drawing a line
   +             Turn left by angle
   -             Turn right by angle
   |             Reverse direction (ie: turn by 180 degrees)
   [             Push current drawing state onto stack
   ]             Pop current drawing state from the stack
   #             Increment line width
   !             Decrement line width
   @             Draw a dot
   {             Open a polygon
   }             Close a polygon
   >             Multiply line length by a factor
   <             Divide line length by a factor
   &             Swap the meaning of + and -
   (             Decrement turning
   )             Increment turning
```

Any lowercase or uppercase letters that are not __F__ or __f__ are used as place holders ([more](#rules)).

### Axiom

__Axiom__ describes the starting set of commands. It is the starting condition which gets recursively replaced. How are commands replaced defines a set of [rules](#rules)

```
axiom <expr>  ; <expr> is any set of commands
```

### Rules

__Rules__ describe how fractals grow, how are commands replaced.

```
rules
    X -> +FY,   ; 'X' gets replaced by '+FY'
    Y -> -FX    ; 'Y' gets replaced by '-FX'
```

you can even write it on a single line,

```
rules X -> +FX, Y -> -FX
```

### Variables

Yes, variables. Even if this language doesn't seem like it needs variables, I've added them anyways.
Variables start with a dot ``.name`` followed by space and a set of commands.

```
.name <expr>     ; <expr> is any set of commands

axiom F.name+    ; usage
```

### Settings

__Settings__ are used to specify how the fractal should be drawn.

```
angle   float   ; angle in degrees (+, -)
width   float   ; width of of the line
winc    float   ; width increment (#, !)
lfac    float   ; line factor (>, <)
ainc    float   ; angle increment ('(', ')')
{col    #hex    ; color of polygon
Fcol    #hex    ; color of line
@col    #hex    ; color of dot
```

Here is how you use them

```
<setting> <value>
```

### Example script

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
python3 lsys.py <script.lsys>
```

Requirements are listed in 'requirements.txt'

