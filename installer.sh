#!/bin/bash
# Installation script for the lights control panel

aptDependencies=("build-essential" "python3" "python3-dev" "git" "scons" "swig" "uwsgi" "uwsgi-plugin-python" "nginx" "uwsgi-plugin-python3");
pipDependencies=("uwsgi neopixel")

lights_service_config_location="/etc/systemd/system/"
nginx_config_file_root="/etc/nginx/"
uwsgi_config_file_root="/etc/lights/"
site_contents_root="/var/lights/"

is_root() {
	!((${EUID:-0} || $(id -u) ));
}

install_dependencies() {
	apt-get install -y "$aptDependencies[@]";
	pip install --yes "$pipDependencies[@]";
}

write_config_files() {
	# - Move site configuration file for nginx to /etc/nginx/sites-available/lights and link the equivalent sites-enabled/lights file
	# - Move lights.ini to /etc/lights/lights.ini
	# - Move nginx.conf to /etc/nginx/nginx.conf
}

install_site() {
	# - Move flask application, templates, and static content to /var/lights/
}

generate_secrets() {
	# - Autogenerate a default password and a secret key for flask application
}

create_service() {
	# - Create and enable lights service to start uwsgi server on boot
}

enable_spi() {
	# - Enable the SPI pin by appending to /boot/config.txt and /boot/cmdline.txt
	# - Add user www-data to SPI group
}

main() {
	echo -e "Installer for the lights control panel application\n";
	
	if ! is_root; then
		echo -e "[Error]\tInstallation requires root privileges!";
		exit;
	fi

	echo -e "[Info]\tInstalling dependencies...";

	if ! install_dependencies; then
		echo -e "[Error]\tFailed to install dependencies!";
		exit;
	fi

	echo -e "[Info]\tWriting configuration files...";

	if ! write_config_files; then
		echo -e "[Error]\tFailed to write configuration files!";
		exit;
	fi

	echo -e "[Info]\tInstalling site...";

	if ! install_site; then
		echo -e "[Error]\tFailed to install site!";
		exit;
	fi

	echo -e "[Info]\tGenerating secrets...";

	if ! generate_secrets; then
		echo -e "[Error]\tFailed to generate secrets!";
		exit;
	fi

	echo -e "[Info]\tCreating lights service...";

	if ! create_service; then
		echo -e "[Error]\tFailed to create service!\nAre you running systemd?";
		exit;
	fi
}

main "@"