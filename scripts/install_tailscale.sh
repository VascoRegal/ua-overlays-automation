#!/bin/bash

TRUSTSCALE_REPO="https://github.com/VascoRegal/trustscale"
TRUSTSCALE_ZIP="trustscale.zip"
TRUSTSCALE_ZIP_PATH="/raw/main/trustscale/${TRUSTSCALE_ZIP}"
HEADSCALE_CERT="headscale.crt"
HEADSCALE_CERT_URL="https://raw.githubusercontent.com/VascoRegal/ua-overlays-automation/main/certs/${HEADSCALE_CERT}"

# Fetch zip with custom binaries
wget ${TRUSTSCALE_REPO}${TRUSTSCALE_ZIP_PATH}
unzip ${TRUSTSCALE_ZIP}

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
