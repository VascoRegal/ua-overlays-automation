HEADSCALE_VERSION="0.22.3"
SYSTEM_ARCH="amd64"
CONFIGURE=0


usage () {
	printf "\nsh install_headscale.sh -v <HEADSCALE_VERSION> -a <SYSTEM_ARCHITECTURE> -c\n"
	printf "\t-v | Headscale version. Defaults to latest stable, v0.22.3 Releases available at https://github.com/juanfont/headscale/releases\n"
	printf "\t-a | System architecture. Defaults to amd64.\n"
	printf "\t-c | If enabled, configure Headscale using available config files\n\n"
}

exit_with_message () {
	printf "ERROR: $1\n\n"
	usage
	exit 1
}



install_headscale () {
	printf "[Headscale Installation]\n"
	printf "HEADSCALE_VERSION=$HEADSCALE_VERSION\n"
	printf "SYSTEM_ARCH=$SYSTEM_ARCH\n"
	printf "CONFIGURE=$CONFIGURE\n\n"


	printf "\n[+] Fetching package..."
	wget --output-document=headscale.deb https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_${SYSTEM_ARCH}.deb
	
	printf "\n[+] Installing package..."
	sudo apt install headscale.deb

	printf "\n[+] Enable service..."
	sudo systemctl enable headscale
	sudo systemctl start headscale

}

configure_headscale () {
	printf "[Headscale Configuration]"

	printf "\n[+] Downloading configuration files..."
	wget --output-document=/etc/headscale/config.yaml https://raw.githubusercontent.com/VascoRegal/ua-overlays-automation/main/config/headscale/config.yaml
	wget --output-document=/etc/headscale/derp-config.yaml https://raw.githubusercontent.com/VascoRegal/ua-overlays-automation/main/config/headscale/derp-config.yaml

	sudo service restart headscale
}



while getopts v:a:c flag
do
	case ${flag} in
		v)
			HEADSCALE_VERSION=$OPTARG
		;;

		a)
			SYSTEM_ARCH=$OPTARG
		;;

		c)
			CONFIGURE=1
		;;
		*)
			exit_with_message "Invalid Options"
		;;
	esac
done


install_headscale

if [ "$CONFIGURE" -eq "1" ]; then
	configure_headscale
fi

exit 0
