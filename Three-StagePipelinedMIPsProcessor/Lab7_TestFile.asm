addi $1, $0, 0 #x position
addi $2, $0, 1 #direction_x
addi $3, $0, 30 #radius
addi $4, $0, 40 #center x
addi $5, $0, 30 #center y
j start

start:
	slt $6, $3, $1 #xpos > radius
	slt $7, $1, $3 #xpos < radius
	beq $6, 1, negate_x_direction
	beq $7, 1, negate_x_direction
	j change_x_direction	

negate_x_direction:
	xori $2, $2, 1
	j change_x_direction

change_x_direction:
	beqz $2, decrement_x
	addi $2, $2, 1
	j calculate_y

decrement_x:
	subi $2, $2, 1
	j calculate_y

calculate_y:
	addi $10, $1, 0 #step = x position
	addi $11, $1, 0 #number = x position
	addi $12, $0, 0 # guess = 0
	j sqrt

sqrt:
	beqz $10, change_y_direction
	mult $10, $10 #guess ^ 2
	mflo $13 #storing guess ^ 2
	sub $14, $13, $11 # value = guess ^ 2 - number
	slti $15, $14, 0 # value < 0
	beqz $15, sqrt_value_not_lessthan_zero
	add $12, $12, $10 #guess = guess + step
	sll $10, $10, 2 #step = step / 2
	j sqrt
	
sqrt_value_not_lessthan_zero:
	sub $12, $12, $10 #guess = guess - step
	sll $10, $10, 2 #step = step / 2
	j sqrt

change_y_direction:
	beqz $2, negate_y_position #if x direction is zero negate y position
	j new_locations

negate_y_position:
	xori $12, $12, 1
	j new_locations

new_locations:
	add $27, $1, $4 #new x position = x pos + center x
	add $28, $12, $5 #new y position = y pos + center y
	j start


