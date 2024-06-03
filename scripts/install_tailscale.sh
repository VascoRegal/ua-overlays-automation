#!/bin/bash


usage () {
	printf "sudo sh ./install_tailscale.sh\n\n"
	printf "\tThis script installs Tailscale using Trustscale binaries.\n"
	printf "\tTrustscale is a Tailscale fork allowing the use of self-signed certificates.\n"
	printf "\tThis script must be run as sudo.\n\n"
	printf "\tThe script downloads a zip with binaries and configurations files and\n"
	printf "\t\tinstalls them in the system.\n"
       	printf "\tIt also fetches and setups Headscale certificates.\n\n"	
}

if [ "$(id -u)" -ne 0 ]; then
	usage
	printf "[ERROR] Please run the script as sudo.\n\n"
	exit 1
fi

SELFSCALE_REPO="https://github.com/VascoRegal/selfscale"
SELFSCALE_ZIP="selfscale.zip"
SELFSCALE_ZIP_PATH="/releases/download/beta/${SELFSCALE_ZIP}"
HEADSCALE_CERT="headscale.crt"
HEADSCALE_CERT_URL="https://raw.githubusercontent.com/VascoRegal/ua-overlays-automation/main/certs/${HEADSCALE_CERT}"

# Fetch zip with custom binaries
wget ${SELFSCALE_REPO}${SELFSCALE_ZIP_PATH}
unzip ${SELFSCALE_ZIP}

# Install binaries and configs
cp tailscaled /usr/sbin/tailscaled
cp tailscale /usr/bin/tailscale

# Setup and enable tailscaled as a service
cp tailscaled.service.conf /etc/default/tailscaled
cp tailscaled.service /lib/systemd/system/tailscaled.service
systemctl enable tailscaled
systemctl start tailscaled

# Add Headscale certificate
wget ${HEADSCALE_CERT_URL}
cp ${HEADSCALE_CERT} /usr/local/share/ca-certificates/headscale.crt
update-ca-certificates

exit 0
