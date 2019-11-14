/**
 * @file shell_manager.c
 * @author Alex Au (alex_acw@outlook.com)
 * @brief
 * @version 0.1
 * @date 2019-01-04
 *
 * @copyright Copyright (c) 2019
 *
 */

#include "shell_manager.h"
#include <stdio.h>
#include <stdlib.h>
static ShellConfig shellCfg = {(BaseSequentialStream *)&SDU1, NULL};

static thread_t *shellWatchdogThd = NULL;

THD_WORKING_AREA(shellWA, SHELL_WA_SIZE);
const size_t temp = sizeof(shellWA);
/**
 * @brief shellWatchdog: thread to monitor the running of a thread, which it
 * will restart the thread when exited, or USB disconnected, later it will have
 * to switch between modes on the channel to achieve other functionalties
 */
THD_WORKING_AREA(shellWatchdogWA, 64);
THD_FUNCTION(shellWatchdog, arg)
{
    (void)arg;
    chRegSetThreadName("shellWatchdog");
    while (!chThdShouldTerminateX())
    {
        chThdWait(chThdCreateStatic(&shellWA,
                                    SHELL_WA_SIZE,
                                    NORMALPRIO + 1,
                                    shellThread,
                                    (void *)&shellCfg));
    }
}

/**
 * @brief start and manage the shell thread on specified channel,
 * events like usb disconnection, exiting, restarting are handled after calling
 * this
 *
 * @param commands pointer to array of ShellCommand, defined the functions
 * available in the shell
 */
void shellManagerStart(const ShellCommand *commands)
{
    shellCfg.sc_commands = commands;
    shellInit();
    if (!shellWatchdogThd)
        shellWatchdogThd = chThdCreateStatic(&shellWatchdogWA,
                                             sizeof(shellWatchdogWA),
                                             NORMALPRIO,
                                             shellWatchdog,
                                             NULL);
}