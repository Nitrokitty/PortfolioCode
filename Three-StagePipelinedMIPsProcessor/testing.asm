loop:
	addi $3, $0, 10
	addi $4, $0, 50
	nop
	lw  $2, 0($0) 			# load cos 
	lw  $10, 1($0) 			# load sin
	nop
	mult $2, $4
	mflo $5
	nop
	mult $5, $11
	mfhi $8
	nop
	nop
	mult $10, $4
	mflo $5
	nop
	mult $5, $11
	mfhi $9