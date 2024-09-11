#!/bin/bash


usage () {
	printf "sudo sh ./install_tailscale.sh\n\n"
	printf "\tThis script installs Tailscale using the official install script.\n"
       	printf "\tIt also fetches and setups Headscale certificates.\n\n"	
}

if [ "$(id -u)" -ne 0 ]; then
	usage
	printf "[ERROR] Please run the script as sudo.\n\n"
	exit 1
fi

HEADSCALE_CERT="headscale.crt"
HEADSCALE_CERT_URL="https://raw.githubusercontent.com/VascoRegal/ua-overlays-automation/main/certs/${HEADSCALE_CERT}"

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Add Headscale certificate
wget ${HEADSCALE_CERT_URL}
cp ${HEADSCALE_CERT} /usr/local/share/ca-certificates/headscale.crt
update-ca-certificates

exit 0
