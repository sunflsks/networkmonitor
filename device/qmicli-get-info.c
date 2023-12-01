#include <unistd.h>

int main(void) {
	execle("/usr/bin/qmicli", "qmicli", "--device=/dev/cdc-wdm0", "--device-open-proxy", "--nas-get-signal-info", NULL);
}
