#include "hal.h"

#ifndef _RC_H
#define _RC_H

typedef struct Rc_data Rc_data;
typedef struct Movement Movement;
typedef struct CylinderMovement CylinderMovement;

struct Rc_data
{
    uint16_t ch0;
    uint16_t ch1;
    uint16_t ch2;
    uint16_t ch3;
    uint8_t s1;
    uint8_t s2;
};

struct Movement
{
    short right_stick_vertical_pos;
    short right_stick_horizontal_pos;
    short left_stick_horizontal_pos;
    bool is_valid_movement;
};

struct CylinderMovement
{
    uint8_t front_up;
    uint8_t back_up;
    bool is_valid_cylinder_movement;
};

/*RC Channel Definition*/
#define RC_CH_VALUE_MIN ((uint16_t)364)
#define RC_CH_VALUE_OFFSET ((uint16_t)1024)
#define RC_CH_VALUE_MAX ((uint16_t)1684)
#define MAX_POSITION_VALUE ((short)660)
#define MIN_POSITION_VALUE ((short)-660)
#define CYLINDER_GO_UP 1
#define CYLINDER_NOT_MOVE 3
#define CYLINDER_GO_DOWN 2

void rcInit(void);
void rcStart(void);
msg_t rcRead(void);
void remoteDataProcess(uint8_t *pData);
Movement getMovement(void);
CylinderMovement getCylinderMovement(void);

#endif
