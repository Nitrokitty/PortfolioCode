andi $0, $0, 0
nop
addi $1, $0, 1
addi $3, $0, 100	#delay		
addi $6, $0, 15		#X-Center
addi $7, $0, 20		#Y-Center
addi $23, $0, 10	#radius
addi $5, $0, 0		#counter
addi $20, $0, 239	#counter max
addi $22, $0, 8888	#color
addi $24, $0, 1111	#bg
nop

#Awesome Loop


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
	j new_x_and_y
	nop

reset_counter:
	nop
	addi $5, $0, 0
	nop
	j new_x_and_y
	

