#include "ch.h"
#include "hal.h"

#ifndef DCMOTOR_H
#define DCMOTOR_H

// motor ID
typedef enum MotorNo
{
    DCMOTOR_1 = 0x201,
    DCMOTOR_2,
    DCMOTOR_3,
    DCMOTOR_4
};

static const CANConfig cancfg = {
    CAN_MCR_ABOM | CAN_MCR_AWUM | CAN_MCR_TXFP,
    CAN_BTR_SJW(0) | CAN_BTR_TS2(1) | CAN_BTR_TS1(8) | CAN_BTR_BRP(2)};

typedef struct Encoders
{
    uint16_t motor1;
    uint16_t motor2;
    uint16_t motor3;
    uint16_t motor4;
};

// Struct pass to receiver thread

typedef struct Values
{
    CANDriver *CAND;
    struct Encoders *encoders;
};

bool motor_init();
bool setPower_now(int16_t power, short motor);
bool setPower(int16_t power, short motor, bool);
uint16_t getPosition(int motor);
int16_t getPower(short motor);
#endif