#! /bin/sh

# Installs aps.service on raspberry-pi-zero
# then restarts service

sudo cp aps.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/aps.service
sudo systemctl daemon-reload
sudo systemctl enable aps.service
sudo systemctl restart aps.service

echo APS.service installed.