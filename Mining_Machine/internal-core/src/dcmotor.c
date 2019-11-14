#include "dcmotor.h"


volatile static struct Encoders encoders;
volatile static CANTxFrame txmsg;
static thread_t *Motor_Data_receiver;
static struct Values values;

// Receiver threads
static THD_WORKING_AREA(CANreceiver, 64 + sizeof(struct Values));
static THD_FUNCTION(receiver, arg){

    struct Values* values = (struct Values*)arg;
    volatile CANRxFrame rxmsg;
    volatile struct Encoders *encoders = ((struct Values *)values)->encoders;
    volatile CANDriver *CAND = values->CAND;
    while (CAND->state == CAN_UNINIT)
    {
    }
    
    while (true)
    {
        msg_t msg =
            canReceiveTimeout(CAND, CAN_ANY_MAILBOX, &rxmsg, TIME_IMMEDIATE);
        if (msg == MSG_OK)
        {
            switch (rxmsg.SID)
            {
            case DCMOTOR_1:
                encoders->motor1 = rxmsg.data8[0] << 8 | rxmsg.data8[1];
                break;
            case DCMOTOR_2:
                encoders->motor2 = rxmsg.data8[0] << 8 | rxmsg.data8[1];
                break;
            case DCMOTOR_3:
                encoders->motor3 = rxmsg.data8[0] << 8 | rxmsg.data8[1];
                break;
            case DCMOTOR_4:
                encoders->motor4 = rxmsg.data8[0] << 8 | rxmsg.data8[1];
                break;
            default:
                break;
            }
        }
        chThdSleepMicroseconds(10);
    }

}

bool motor_init()
{
    // Default frame setting
    txmsg.DLC = 8;
    txmsg.IDE = CAN_IDE_STD;
    txmsg.RTR = CAN_RTR_DATA;
    txmsg.SID = 0x200;
    AFIO->MAPR |= AFIO_MAPR_CAN_REMAP_REMAP2;
    canStart(&CAND1, &cancfg);

    for (int i = 0; i < 8; i += 2)
    {
        txmsg.data8[i] = 0;
        txmsg.data8[i + 1] = 0;
    }
    // Stop the motor when init

    if (canTransmitTimeout(&CAND1, CAN_ANY_MAILBOX, &txmsg, TIME_MS2I(1)) == MSG_OK)
    {
        void *rec_arg[] = {NULL, &CAND1, &encoders};
        volatile int temp = CAND1.state;

        values.CAND = &CAND1;
        values.encoders = &encoders;

        Motor_Data_receiver = chThdCreateStatic(CANreceiver, sizeof(CANreceiver), NORMALPRIO , receiver, &values);
        return true;
    }else
    {
        return false;
    }
    
}

bool setPower(int16_t power, short motor, bool sendNow)
{
    int pos = (motor - 0x200 - 1) * 2;
    if (pos > 6 || pos < 0)
        return false;
    txmsg.data8[pos] = power >> 8;
    txmsg.data8[pos + 1] = power & 0xFF;
    if (sendNow)
    {
        return canTransmitTimeout(
                   &CAND1, CAN_ANY_MAILBOX, &txmsg, TIME_MS2I(1)) == MSG_OK;
    }
    else
    {
        return false;
    }
}

bool setPower_now(int16_t power, short motor) { return setPower(power, motor, true); }

int16_t getPower(short motor)
{
    int pos = (motor - 0x200 - 1) * 2;
    if (pos > 6 || pos < 0)
        return -1;
    return txmsg.data8[pos] << 8 | txmsg.data8[pos + 1];
}

// return encoder value of motor
uint16_t getPosition(int motor)
{
    uint16_t value = 0;
    switch (motor)
    {
    case DCMOTOR_1:
            value = encoders.motor1;
            break;
        case DCMOTOR_2:
            value = encoders.motor2;
            break;
        case DCMOTOR_3:
            value = encoders.motor3;
            break;
        case DCMOTOR_4:
            value = encoders.motor4;
            break;
        default:
            value = 0;
    }
    return value;
}
