#include <stdio.h>
#include <string.h>
#include <errno.h>

#define LED_PATH "/sys/class/leds/ACT/brightness"

int main(int argc, char** argv) {
	if (argc < 2) {
		return 1;
	}

	FILE* led = fopen(LED_PATH, "w");

	if(!strcmp(argv[1], "on")) {
		fputs("1", led);
		fclose(led);
		return 0;
	}

	if (!strcmp(argv[1], "off")) {
		fputs("0", led);
		fclose(led);
		return 0;
	}
}
