#initalizing registers
andi $0, $0, 0
addi $1, $0, 1
addi $24, $0, 40
addi $23, $0, 30
addi $6, $0, 16
addi $5, $0, 5000
sll  $6, $6, 5		#foreground
nop
add  $5, $6, $5	#foreground
#addi $20, $0, 0
#andi $21, $0, 0
#andi $22, $0, 0
nop
add $20, $0, $30	#getting reg 30 data
nop
nop
and $21, $20, 8064		#getting row
and $22, $20, 127		#getting column
srl $21, $20, 7		#alligning row

nop
nop
slt $2, $22, $23	#column < 30
slt $3, $21, $23	#row < 30
nop
beq $2, $1, set_to_background 
beq $3, $1, set_to_background
slt $2, $24, $22	#column > 40
slt $2, $24, $21	#row > 40
nop
beq $2, $1, set_to_background	
beq $3, $1, set_to_background	
addi $30, $1, 1
j exit

set_to_background:
	and $30, $0, 0
	j exit

exit:
	nop