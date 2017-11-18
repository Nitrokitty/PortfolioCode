andi $0, $0, 0
add $20, $0, $30	#getting reg 30 data
nop
nop
andi $21, $20, 8064		#getting row
andi $22, $20, 127		#getting column
srl $21, $20, 7		#alligning row
sll $20, $20, 1
nop
slti $3, $22, 50
nop
nop
beq $3, $0, foreground
addi $20, $0, 1
j exit

foreground: 
	addi $20, $0, 0
	j exit

exit:
nop
add $30, $20, $0