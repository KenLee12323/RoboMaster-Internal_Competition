#include "hal.h"
#include "RC.h"

#ifndef _TARGETVALUES_H
#define _TARGETVALUES_H

typedef struct TargetValues TargetValues;

struct TargetValues
{
    short motor1_target_power;
    short motor2_target_power;
    short motor3_target_power;
    short motor4_target_power;
    bool is_valid_target_values;
};

#define MAX_MOTOR_POWER ((short)4000)
#define TURN_POWER ((short)1000)

TargetValues getTargetValues(Movement movement);

#endif
