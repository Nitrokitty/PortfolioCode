andi $0, $0, 0
nop
nop
addi $3, $0, 1
addi $2, $0, 0		#X-Position
addi $4, $0, 0		#Y-Position
addi $6, $0, 20		#X-Center
addi $8, $0, 20		#Y-Center
#addi $21, $0, 5	#radius
addi $23, $0, 10	#radius
addi $24, $0, -10
addi $10, $0, 1		#X-Direction
addi $22, $0, 8888
nop

loop:
	nop

#Awesome Loop
check_direction:
	nop
	beq $2, $24, change_direction_pos		#if X == radius then change direction
	nop
	beq $2, $23, change_direction_neg
	nop
	j change_x
	nop

change_direction_neg:
	nop
	addi $10, $0, -1
	nop
	j change_x
	nop

change_direction_pos:
	nop
	addi $10, $0, 1
	nop
	j change_x
	nop

change_x:
	nop
	add $18, $2, $10		# the new x is equal to x + direction
	j calculate_y
	nop

calculate_y:
	nop
	mult $23, $23
	mflo $13		#$11 = r ^ 2
	nop
	mult $18, $18
	mflo $19		#$12 = x ^ 2
	nop
	sub $9, $13, $19	#$9 = r^2- x^2
	nop
	#moving result of sqrt to new y position

sqrt:
	add $11, $0, $0 # guess
	nop
	add $12, $0, $23 # step
	nop
sqrtloop:
	nop
	nop
   	mult $11, $11
   	mflo $13
	nop
	nop
	beq $13, $9, sqrtdone
	nop
	nop
    	slt $13, $13, $0
	nop
	nop
    	bgez $13, sqrtlt0
	nop
	nop

sqrtgt0:
	nop
	nop
	sub $11, $11, $12
	nop
	j sqrtchk
	nop
sqrtlt0:
	nop
	add $11, $11, $12
	nop
sqrtchk:
	nop
	srl $12, $12, 1
	nop
	nop
	beq $12, $0, sqrtdone
	nop
	nop
	j sqrtloop
	nop
sqrtdone:
	addi $1, $0, 1
	nop
	slt $14, $18, $0
	nop
	beq $14, $1, check_less_than_zero
	nop

check_greater_than_zero:
	nop
	beqz $10, subtract
	nop
	nop
	j new_x_and_y
	nop

subtract:
	nop
	sub $11, $0, $11
	j new_x_and_y
	nop

check_less_than_zero:
	nop
	beqz $10, new_x_and_y
	nop
	nop
	sub $11, $0, $11
	nop
	nop
	j new_x_and_y

nop
new_x_and_y:	
	nop				#clearing old x and y
	nop
	add $2, $18, $0			#storing new x and y
	nop
	add $4, $11, $0
	nop
	add $4, $8, $4		
	nop
	sll $4, $4, 7
	nop
	add $2, $6, $2
	nop
	add $15, $4, $2
	nop
	add $15, $15, $21
	nop
	sw $22, 0($15)
	nop
	add $2, $18, $0			#storing new x and y
	nop
	add $4, $19, $0

j loop
	

