#include "hal.h"
#include "targetValues.h"



TargetValues getTargetValues(Movement movement){

    TargetValues tvs;

    tvs.is_valid_target_values = movement.is_valid_movement;

    if(movement.left_stick_horizontal_pos > 0 ){

        tvs.motor1_target_power =  - TURN_POWER;
        tvs.motor2_target_power =  - TURN_POWER;
        tvs.motor3_target_power =  TURN_POWER;
        tvs.motor4_target_power =  TURN_POWER;
    }
    else if(movement.left_stick_horizontal_pos < 0)
    {
        tvs.motor1_target_power =  TURN_POWER;
        tvs.motor2_target_power =  TURN_POWER;
        tvs.motor3_target_power =  -TURN_POWER;
        tvs.motor4_target_power =  -TURN_POWER;
    }
    
    //only moves when the cart is not rotating
    else{

        short vx = movement.right_stick_horizontal_pos / 660.0 * MAX_MOTOR_POWER;
        short vy = movement.right_stick_vertical_pos / 660.0 * MAX_MOTOR_POWER;

        tvs.motor1_target_power = vy - vx;
        tvs.motor2_target_power = vy + vx;
        tvs.motor3_target_power = vy + vx;
        tvs.motor4_target_power = vy - vx;
    }

    return tvs;
}