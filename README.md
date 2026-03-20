**Free to Use C SDK for the Cody Computer written in Python**

--------------------------------------------------

**Requirements**

- Python 3  
- 64tass assembler  

--------------------------------------------------

**Usage**

It is possible to translate a program consisting of **N C files** to assembly by using:

`python3 Main.py [-data] <output file name> <input file 1>.c <input file 2>.c ... <input file N>.c`

The output ASM file can be translated to binary using the **64tass** assembler by using:

`64tass --mw65c02 --nostart -o <out filename>.bin <input filename>.asm`

**Optional Flag**

-data is optional.  
If used, the SDK includes the bytes from data.lib into the assembly file.  
This allows as much data as possible to be included with less code.

The included data can be used by the system libraries found in the /libs folder.


--------------------------------------------------

**System Libraries**

In the /libs folder there are header files for the corresponding libraries.

Inside each header file is a brief explanation of the method that is implemented in **Three-Address Code** inside the <file>.dac, which is also located in the /libs folder.

All implemented functions are usable in your C program.

**Including a system library**

`#include <syslib.h>`

**Including custom libraries**

`#include "file.h"`

These custom libraries must also be included in the SDK call above in order to be compiled.

--------------------------------------------------

**Example Code**

Example programs can be found in the Examplecodes folder.  
These examples demonstrate how to use the SDK, system libraries, and language features.

--------------------------------------------------

**Boolean Representation**

The C language implementation uses the following boolean representation:

- true is represented by **0**
- false is represented by **255**

--------------------------------------------------

**Comments**

Comments are supported in every representation.

Single-line comments can be written using:

`// comment`

Multi-line comments can be written using:

`/*
   comment
*/`

--------------------------------------------------

**C Grammar Specification**

Program:  
    EOF |  
    Globalinit Program |  
    Globaldec Program |  
    Functiondec Program |  
    Func Program  

Globaldec: Type Ident ';'  

Globalinit: Type Ident '=' Globalinitvalue ';'  

Functiondec: FuncType Ident '(' (Type Ident (',' Type Ident)* )? ')' ';'  

Func: FuncType Ident '(' (Type Ident (',' Type Ident)* )? ')' '{' Funcbody '}'  

Funcbody: (Instructions)*  

Instructions: (Instruction)*  

Instruction:  
    '{' Instructions '}' |  
    'if' '(' Expression ')' Instruction ('else' Instruction)? |  
    'for' '(' Type Ident '=' Expression ';' Expression ';' Assignment ')' Instruction |  
    'while' '(' Expression ')' Instruction |  
    'return' Expression ';' |  
    Type Ident (';' | '=' Expression (',' Ident '=' Expression)* ';') |  
    Voidfunccall |  
    Assignment  

Voidfunccall: Ident '(' (Expression (',' Expression)* )? ')' ';'  

Functioncall: Ident '(' (Expression (',' Expression)* )? ')'  

Assignment: LeftUnary ('+=' | '=' | '-=' | '*=' | '/=' | '%=' | '&=' | '^=' | '|=') Ternary  

LeftAdd: LeftMult (('+' | '-') LeftMult)*  

LeftMult: LeftUnary (('*' | '/' | '%') LeftUnary)*  

LeftUnary: ('*' | '&' | '++' | '--') LeftUnary | LeftSuffix  

LeftSuffix: LeftHighest (('++' | '--' | '[' LeftAdd ']'))*  

LeftHighest: '(' LeftAdd ')' | Ident | Number  

Expression: Ternary  

Ternary: Or ('?' Expression ':' Ternary)?  

Or: And ('||' And)*  

And: BwOr ('&&' BwOr)*  

BwOr: BwXor ('|' BwXor)*  

BwXor: BwAnd ('^' BwAnd)*  

BwAnd: Eq ('&' Eq)*  

Eq: Cond (('==' | '!=') Cond)*  

Cond: Shift (('<' | '>' | '<=' | '>=') Shift)*  

Shift: Add (('<<' | '>>') Add)*  

Add: Mult (('+' | '-') Mult)*  

Mult: Unary (('*' | '/' | '%') Unary)*  

Unary: ('+' | '-' | '!' | '*' | '&' | '++' | '--') Unary | Suffix  

Suffix: Highest (('++' | '--' | '[' Expression ']'))*  

Highest: '(' Expression ')' | Functioncall | Ident | Number | Character  

Type: 'int' Pointerstar | 'short' Pointerstar  

FuncType: 'void' Pointerstar | 'int' Pointerstar | 'short' Pointerstar  

Pointerstar: ('*')*

--------------------------------------------------

**Compiler Capabilities**

The compiler supports:

- variable pointers  
- while loops  
- for loops  
- if-else statements  
- operator precedence  
- scoping  
- short-circuit evaluation  

There are only two data types:

- **int** is represented as **16-bit**
- **short** is represented as **8-bit**

Variable pointers are also **16-bit**.

--------------------------------------------------

**Notes**

This documentation was translated by ChatGPT.

