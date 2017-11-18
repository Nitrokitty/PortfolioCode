andi $0, $0, 0
nop
addi $1, $0, 1
#2 = cos
addi $3, $0, 100	#delay		
#4 = reg30 in (keys)
addi $5, $0, 0		#counter
addi $6, $0, 40		#X-Center
addi $7, $0, 30		#Y-Center
#8 = cos*r
#9 = sin*r
#10 = sin
#11 = temp
#15 = y + x + hc00
addi $20, $0, 358	#counter max
#21 = hc001
addi $22, $0, 8888	#color
addi $23, $0, 15	#radius
addi $24, $0, 0000	#bg
nop

#Awesome Loop
loop:
	nop
	addi $3, $0, 30000		# reset delay
	nop
	j delay
	nop
delay:
	nop
	beqz $3, new_x_and_y
	nop
	subi $3, $3, 1
	nop
	j delay
	nop

new_x_and_y:	
	nop
	sw $24, 0($15)			# clearing old
	nop
	lw  $2, 0($5) 			# load cos * 2^31
	nop
	lw  $10, 1($5) 			# load sin * 2^31
	nop
	addi $5, $5, 2			#increment counter
	nop
	mult $2, $23			# 2^31 * cos * r
	mfhi $8				#x
	nop
	nop
	mult $10, $23			#sin * 2^31 * r
	mfhi $9				#y
	nop 
	nop
	add $8, $8, $6			#x + x center
	add $9, $9, $7			#y + y center
	nop
	nop
	sll $9, $9, 7			# y_pos << 7
	nop
	add $15, $9, $8			# y_pos + x_pos			
	nop
	add $15, $15, $21		# y_pos + x_pos + hC000
	nop
	sw $22, 0($15)			# sending new positions
	nop
	beq $20, $5, reset_counter
	nop
	j check_counter
	nop

reset_counter:
	nop
	addi $5, $0, 0
	nop
	j check_counter
	nop

check_counter:
	nop
	addi $11, $0, 90
	nop
	beq $11, $5, check_keys
	nop
	addi $11, $0, 180
	nop
	beq $11, $5, check_keys
	nop
	addi $11, $0, 270
	nop
	beq $11, $5, check_keys
	nop
	addi $11, $0, 0
	nop
	beq $11, $5, check_keys
	nop
	j loop

check_keys:
	nop
	addi $4, $30, 0
	nop
	addi $11, $0, 8
	nop
	beq $4, $11, inc_r
	nop
	addi $11, $0, 4
	nop
	beq $4, $11, dec_r
	nop
	j loop
	nop

dec_r:
	nop
	addi $11, $0, 1
	nop
	beq $11, $23, loop
	nop
	subi $23, $23, 1
	nop
	j loop
	nop

inc_r:
	nop
	addi $11, $0, 60 
	nop
	beq $11, $23, loop
	nop
	addi $23, $23, 1
	nop
	j loop
	nop