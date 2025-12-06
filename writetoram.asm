;   64tass --mw65c02 --nostart -o writetoram.bin writetoram.asm
ADDR= $0300
.WORD ADDR
.WORD (ADDR + LAST - FIRST - 1)
.LOGICAL    ADDR
FIRST:
LDA #$FF
STA 0
LDA #0
STA 2
LDA #208
STA 3
LDA 2
STA 10
LDA 3
STA 11
LDA #1
STA 2
LDA #208
STA 3
LDA 2
STA 12
LDA 3
STA 13
LDA #2
STA 2
LDA #208
STA 3
LDA 2
STA 14
LDA 3
STA 15
LDA #3
STA 2
LDA #208
STA 3
LDA 2
STA 16
LDA 3
STA 17
LDA #4
STA 2
LDA #208
STA 3
LDA 2
STA 18
LDA 3
STA 19
LDA #5
STA 2
LDA #208
STA 3
LDA 2
STA 20
LDA 3
STA 21
LDA #6
STA 2
LDA #208
STA 3
LDA 2
STA 22
LDA 3
STA 23
LDA #6
STA 2
LDA #208
STA 3
LDA 2
STA 24
LDA 3
STA 25
LDA #0
STA 2
LDA #224
STA 3
LDA 2
STA 26
LDA 3
STA 27
LDA #0
STA 2
LDA #196
STA 3
LDA 2
STA 28
LDA 3
STA 29
LDA #0
STA 2
LDA #216
STA 3
LDA 2
STA 30
LDA 3
STA 31
JSR main
JMP BRK
;	 Function: funcA
funcA:
TSX
LDA 0
PHA
TXA
STA 0
LDA #0
;	 Call
LDA #3
STA 2
LDA #0
STA 3
LDA 3
PHA
LDA 2
PHA
JSR vid_set_border_color
;	Return
;	Ram[6] = Ram[$100 + Ram[0]](Old FBP)
LDA 0
TAX
LDA $100, X
STA 6
LDA #1
STA 2
LDA #0
STA 3
;	SP=Ram[0](FBP)
LDA 0
TAX
TXS
;	FBP = Ram[6]
LDA 6
STA 0
rts
;	 Function: funcB
funcB:
TSX
LDA 0
PHA
TXA
STA 0
LDA #0
;	 Call
LDA #4
STA 2
LDA #0
STA 3
LDA 3
PHA
LDA 2
PHA
JSR vid_set_border_color
;	Return
;	Ram[6] = Ram[$100 + Ram[0]](Old FBP)
LDA 0
TAX
LDA $100, X
STA 6
LDA #1
STA 2
LDA #0
STA 3
;	SP=Ram[0](FBP)
LDA 0
TAX
TXS
;	FBP = Ram[6]
LDA 6
STA 0
rts
;	 Function: main
main:
TSX
LDA 0
PHA
TXA
STA 0
LDA #0
;	 Call
JSR funcA
;	_0 = Ram[2]
LDA 2
STA $200
LDA 3
STA $201
;	Ram[2] = _0
LDA $200
STA 2
LDA $201
STA 3
;	_1 = Ram[2]
LDA 2
STA $202
LDA 3
STA $203
;	Ram[2] = c2
LDA $202
STA 2
LDA $203
STA 3
LDA 2
BNE mainc2
JMP mainc3
mainc2:
;	 Call
JSR funcB
;	_3 = Ram[2]
LDA 2
STA $206
LDA 3
STA $207
;	Ram[2] = _3
LDA $206
STA 2
LDA $207
STA 3
;	_1 = Ram[2]
LDA 2
STA $202
LDA 3
STA $203
;	Ram[2] = c1
LDA $202
STA 2
LDA $203
STA 3
LDA 2
BNE mainc1
JMP mainc3
mainc1:
;	Ram[2] = 1
LDA #1
STA 2
LDA #0
STA 3
;	_2 = Ram[2]
LDA 2
STA $204
LDA 3
STA $205
JMP mainc4
mainc3:
;	Ram[2] = 0
LDA #0
STA 2
LDA #0
STA 3
;	_2 = Ram[2]
LDA 2
STA $204
LDA 3
STA $205
mainc4:
;	Ram[2] = c5
LDA $204
STA 2
LDA $205
STA 3
LDA 2
BNE mainc5
JMP mainc6
mainc5:
;	 Call
LDA #5
STA 2
LDA #0
STA 3
LDA 3
PHA
LDA 2
PHA
JSR vid_set_border_color
;	Return
;	Ram[6] = Ram[$100 + Ram[0]](Old FBP)
LDA 0
TAX
LDA $100, X
STA 6
LDA #1
STA 2
LDA #0
STA 3
;	SP=Ram[0](FBP)
LDA 0
TAX
TXS
;	FBP = Ram[6]
LDA 6
STA 0
rts
mainc6:
;	Return
;	Ram[6] = Ram[$100 + Ram[0]](Old FBP)
LDA 0
TAX
LDA $100, X
STA 6
LDA #0
STA 2
LDA #0
STA 3
;	SP=Ram[0](FBP)
LDA 0
TAX
TXS
;	FBP = Ram[6]
LDA 6
STA 0
rts
;	 Function: vid_set_border_color
vid_set_border_color:
TSX
LDA 0
PHA
TXA
STA 0
LDA #0
;	Ram[2] = *vid_color_register
LDA 14
STA 2
LDA 15
STA 3
LDA #0
TAY
LDA (2),Y
STA 2
LDA #0
STA 3
;	Ram[4] = 240
LDA #240
STA 4
LDA #0
STA 5
LDA 2
AND 4
STA 2
LDA 3
AND 5
STA 3
;	*vid_color_register = Ram[2]
;	Ram[4] = vid_color_register
LDA 14
STA 4
LDA 15
STA 5
LDA #0
TAY
LDA 2
STA (4),Y
;	Ram[2] = *vid_color_register
LDA 14
STA 2
LDA 15
STA 3
LDA #0
TAY
LDA (2),Y
STA 2
LDA #0
STA 3
;	Ram[4] = color
LDA 0
CLC
ADC #3
TAX
LDA $100,X
STA 4
LDA #0
STA 5
LDA 2
ORA 4
STA 2
LDA 3
ORA 5
STA 3
;	*vid_color_register = Ram[2]
;	Ram[4] = vid_color_register
LDA 14
STA 4
LDA 15
STA 5
LDA #0
TAY
LDA 2
STA (4),Y
;	Return
;	Ram[6] = Ram[$100 + Ram[0]](Old FBP)
LDA 0
TAX
LDA $100, X
STA 6
;	SP=Ram[0](FBP)
LDA 0
TAX
TXS
;	FBP = Ram[6]
LDA 6
STA 0
rts
BRK: BRA BRK
LAST
.ENDLOGICAL
