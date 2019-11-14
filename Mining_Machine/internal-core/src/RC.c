#include "hal.h"
#include "RC.h"

static Rc_data rc_data;
static Movement movement;
static CylinderMovement cylinderMovement;

static uint8_t buffer[18];
static size_t bufferSize = (size_t)18;

static const UARTConfig rc_config =
    {
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        100000,
        USART_CR1_M | USART_CR1_PCE,
        USART_CR2_LBDL,
        0
    };

static THD_WORKING_AREA(rcWorkingArea,128);
static THD_FUNCTION(rcThread,arg){
    while (true){
        rcRead();
    }
}

void rcInit(){
    AFIO->MAPR |= AFIO_MAPR_USART1_REMAP; 
    uartInit();
    rcStart();

    (void)chThdCreateStatic(rcWorkingArea, sizeof(rcWorkingArea),NORMALPRIO, rcThread, NULL);
}

void rcStart(){
    uartStart(&UARTD1,&rc_config);
}

void remoteDataProcess(uint8_t *pData)
{
    rc_data.ch0 = ((int16_t)pData[0] | ((int16_t)pData[1] << 8)) & 0x07FF;
    rc_data.ch1 = (((int16_t)pData[1] >> 3) | ((int16_t)pData[2] << 5)) & 0x07FF;
    rc_data.ch2 = (((int16_t)pData[2] >> 6) | ((int16_t)pData[3] << 2) | ((int16_t)pData[4] << 10)) & 0x07FF;
    rc_data.ch3 = (((int16_t)pData[4] >> 1) | ((int16_t)pData[5] << 7)) & 0x07FF;
    rc_data.s1 = ((pData[5] >> 4) & 0x000C) >> 2;
    rc_data.s2 = ((pData[5] >> 4) & 0x0003);

    movement.right_stick_horizontal_pos = rc_data.ch0 - RC_CH_VALUE_OFFSET;
    movement.right_stick_vertical_pos = rc_data.ch1 - RC_CH_VALUE_OFFSET;
    movement.left_stick_horizontal_pos = rc_data.ch2 - RC_CH_VALUE_OFFSET;

    if(rc_data.s1 != 0 && rc_data.s2 != 0){
        cylinderMovement.front_up = rc_data.s1;
        cylinderMovement.back_up = rc_data.s2;
    }

    //check whether the data is normal
    if((movement.right_stick_horizontal_pos <= MAX_POSITION_VALUE && movement.right_stick_horizontal_pos >= MIN_POSITION_VALUE)&&
        (movement.right_stick_vertical_pos <= MAX_POSITION_VALUE && movement.right_stick_vertical_pos >= MIN_POSITION_VALUE)&&
        (movement.left_stick_horizontal_pos <= MAX_POSITION_VALUE && movement.left_stick_horizontal_pos >= MIN_POSITION_VALUE)){
        movement.is_valid_movement = 1;
    }
    else{
        movement.is_valid_movement = 0;
    }

    if((cylinderMovement.back_up >= 1 && cylinderMovement.back_up <= 3)&&
        (cylinderMovement.front_up >= 1 && cylinderMovement.front_up <= 3)){
        cylinderMovement.is_valid_cylinder_movement = 1;
    }
    else{
        cylinderMovement.is_valid_cylinder_movement = 0;
    }


    chThdSleepMilliseconds(1);
}


msg_t rcRead(){
    bufferSize = 18;
    msg_t msg = uartReceiveTimeout(&UARTD1,&bufferSize,buffer,TIME_MS2I(10));
    remoteDataProcess(buffer);
    return msg;
}



Movement getMovement(){
    return movement;
}

CylinderMovement getCylinderMovement(){
    return cylinderMovement;
}


