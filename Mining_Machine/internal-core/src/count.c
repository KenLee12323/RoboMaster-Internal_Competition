#include "count.h"

Result getLargestConsecutiveChar(char *str)
{
    Result r;
    r.length = 0;

    int theFirstChar = 0, theIntervalLength = 0;
    char thePresentChar;

    while (str[theFirstChar] != '\0')
    {
        thePresentChar = str[theFirstChar];
        theIntervalLength = 0;
        while (str[theFirstChar + theIntervalLength] == thePresentChar)
            theIntervalLength++;
        if (theIntervalLength > r.length)
            r.length = theIntervalLength, r.c = thePresentChar;
        theFirstChar += theIntervalLength;
    }

    if (r.length == 0)
        r.c = '\0', r.length = 1;

    return r;
}