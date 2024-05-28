#include <unistd.h>
#include <string.h>

int main(int argc, char** argv) {
	char* modem_path = argv[1];
	char* query = argv[2];

	char* gps_args[] = {
		"mmcli",
		"-m",
		modem_path,
		"--location-get",
		NULL
	};

	char* cellular_args[] = {
		"mmcli",
		"-m",
		modem_path,
		"--signal-get",
		NULL
	};

	char** args = NULL;

	if (!strcmp(argv[2], "gps")) {
		args = gps_args;
	} 

	else if (!strcmp(argv[2], "cell")) {
		args = cellular_args;
	}

	else return 1;

	execve("/usr/bin/mmcli", args, NULL);
}
