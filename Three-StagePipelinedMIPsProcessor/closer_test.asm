andi $0, $0, 0
nop
nop
addi $2, $0, 0		#X-Position
addi $4, $0, 0		#Y-Position
addi $6, $0, 30		#X-Center
addi $8, $0, 40		#Y-Center
#addi $21, $0, 5	#radius
addi $23, $0, 50	#radius
addi $24, $0, -50
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
	addi $19, $2, 0
	j new_x_and_y
	nop
	mult $21, $21
	mflo $13		#$11 = r ^ 2
	nop
	mult $18, $18
	mflo $19		#$12 = x ^ 2
	nop
	sub $9, $13, $19	#$9 = r^2- x^2
	addi $19, $18, 1
	j new_x_and_y

nop
	#moving result of sqrt to new y position


new_x_and_y:	
	nop				#clearing old x and y
	nop
	add $2, $18, $0			#storing new x and y
	nop
	add $4, $19, $0
	nop
	#add $4, $8, $4		
	nop
	sll $4, $4, 7
	nop
	#add $2, $7, $2
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
	

