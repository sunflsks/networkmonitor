#include <stdio.h>
#include <string.h>
#include <errno.h>

#define PWR_LED_PATH "/sys/class/leds/PWR/brightness"
#define ACT_LED_PATH "/sys/class/leds/ACT/brightness"

int main(int argc, char **argv)
{
	if (argc < 3)
	{
		return 1;
	}

	FILE *led = NULL;

	if (!strcmp(argv[1], "PWR"))
	{
		led = fopen(PWR_LED_PATH, "w");
	}
	else if (!strcmp(argv[1], "ACT"))
	{
		led = fopen(ACT_LED_PATH, "w");
	}
	else
	{
		return 1;
	}

	if (!strcmp(argv[2], "on"))
	{
		fputs("1", led);
		fclose(led);
		return 0;
	}

	else if (!strcmp(argv[2], "off"))
	{
		fputs("0", led);
		fclose(led);
		return 0;
	}

	else
	{
		return 1;
	}
}
