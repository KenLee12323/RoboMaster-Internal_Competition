/**
 * @file shell_manager.h
 * @author Alex Au (alex_acw@outlook.com)
 * @brief The purpose of ShellManager is to handle the start and restart of shell thread, also assist the setup of shell commands
 * @version 0.1
 * @date 2019-01-04
 *
 * @copyright Copyright (c) 2019
 *
 */

#pragma once

#include "ch.h"
#include "hal.h"
#include "shell.h"
#include "chprintf.h"
#include "../peripherals/usbcfg.h"
#ifdef __cplusplus
extern "C"
{
#endif

#define SHELL_WA_SIZE 1024

    /**
     * @brief start and manage the shell thread on SHELL_CHN,
     * @param commands pointer to array of ShellCommand, defined the functions available in the shell
     */
    void shellManagerStart(const ShellCommand *commands);

#ifdef __cplusplus
}
#endif