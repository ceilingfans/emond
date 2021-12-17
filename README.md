# emond
A language inspired by brainfuck

## How the language works
- Input
  - A SINGLE line of operators
- Cells
  - There will be 1000 cells with the value of 0 when the program starts
- Operators
  - These are special characters used to interact with cells and their values


### Operators
| Operator | Literal |
----------|-----------
| Add | + |
| Minus | - |
| Print | % |
| Newline | ^ |
| Hard Reset | ! |
| Alphabet Reset | $ |
| Left Cell Shift | < |
| Right Cell Shift | \> |

### Add (+):
```
; adds 1 to the current cell's value
+++
; the operator has been used 3 times in the current cell (0)
; the value of the cell will now be 3
```

### Minus (-)
```
; subtracts 1 from current cell' value
---
; the operator has been used 3 times in the current cell (0)
; the value of the cell will now be -3

; NOTE: cell's values cannot be negative! this will throw an error
;       this will be explained later
```

### Print (%)
```
; prints the unicode character correspondent to the cell's value
$%
; the current cell's value is 96 after the alphabet reset operator
; was used (will be covered later)
; the print operator will now print unicode character 96 which is
; the lowercase A `a`
```

### Newline
```
; prints a newline
^
; self explanatory
```

### Hard Reset (!)
```
; resets the current cell's value to 0
$!
; the current cell's value is 96 after the alphabet reset operator
; was used (will be covered later)
; the hard reset operator will reset the cell's value to 0
```

### Alphabet Reset (!) - Utility Operator
```
; sets the current cell's value to 96 (unicode character `a`)
$%
; prints `a`
```

### Left Cell Shift (<)
```
; shifts the cell pointer 1 cell to the left
<<<
; the operator was used 3 times which means the current cell
; is cell -3 (this will throw an error as cell pointers cannot be negative)
```

### Right Cell Shift (>)
```
; shifts the cell pointer 1 cell to the right
>>>
; the operator was used 3 times which means the current cell
; is cell 3
```

# Getting Started
- Running Code
```shell
$ python3 emond.py examples/helloworld.em
```
This will interpret the hello world example
```shell
$ python3 emond.py --help
```
This will print the help message where you can find more options

# Contribution
I am currently not accepting any contributions to this project
but feel free to fork it

# Credits
- The Creator of Brainfuck