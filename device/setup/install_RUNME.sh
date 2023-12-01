#!/usr/bin/env bash

if [ $UID -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

create_new_rc_local() {
	echo "WARNING: rewriting /etc/rc.local; saving old one (if exists) as /etc/rc.local.bak"
	mv -fv "/etc/rc.local" "/etc/rc.local.bak"

	echo -e "#!/usr/bin/env bash\n/usr/local/lib/networkmonitor/sim_init\n/usr/local/lib/networkmonitor/init.sh" > "/etc/rc.local"
	chmod +x "/etc/rc.local"
}

install_sim_init_script() {
	echo "Installing sim init script thing"
	mkdir -p "/usr/local/lib/networkmonitor"
	cp -v "./sim_init" "/usr/local/lib/networkmonitor/sim_init"
	chmod +x "/usr/local/lib/networkmonitor/sim_init"
}

install_data_init_script() {
	echo "Installing cellular data init script thing"
	mkdir -p "/usr/local/lib/networkmonitor"
	cp -v "./init.sh" "/usr/local/lib/networkmonitor/init.sh"
	chmod +x "/usr/local/lib/networkmonitor/init.sh"
}


compile_qcm_rssi_command() {
	cc ../qmicli-get-info.c -o /usr/local/lib/networkmonitor/qmicli-get-info
	chmod u+s /usr/local/lib/networkmonitor/qmicli-get-info
}

run_setup_script() {
	./setup.sh
}

install_sim_init_script
install_data_init_script
create_new_rc_local
compile_qcm_rssi_command
#run_setup_script

echo "Done!"
