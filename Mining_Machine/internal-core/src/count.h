#pragma once

typedef struct
{
    char c;
    unsigned short length;
} Result;

Result getLargestConsecutiveChar(char *str);