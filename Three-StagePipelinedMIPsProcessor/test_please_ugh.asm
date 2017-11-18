andi $0, $0, 0
andi $1, $0, 0
nop
andi $5, $0, 0
andi $2, $0, 0

addi $3, $0, 50
addi $4, $0, 50
addi $22, $0, 8888
addi $23, $0, 1111
addi $24, $0, 10

loop:
	andi $10, $0, 0
	nop
	addi $11, $10, 1000000
	nop


wait:
	addi $10, $10, 1
	nop
	beq $10, $11 calculating
	nop
	j wait
	nop

calculating:	
	addi $2, $2, 1
	nop
	beq $2, $3, add_to_y
	j store_stuff
	nop
add_to_y:
	nop
	addi $5, $5, 1
	andi $2, $0, 0
	beq $5, $3, reset_x
	j store_stuff
	nop

reset_x:
	andi $5, $5, 0
	j store_stuff

store_stuff:
	nop
	sll $12, $5, 7		#move by number of columns bits
	nop
	add $13, $12, $2
	nop
	add $13, $21, $13
	nop
	sw $22, 0($13)

j loop
