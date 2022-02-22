# audium-aps
 Audium Projector System

This repo runs a simple OSC server on the raspberry pi, allowing it to receive and send OSC commands

Requires: python-osc

Install APS-Service: 
```
sudo cp aps.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/aps.service
sudo systemctl daemon-reload
sudo systemctl enable aps.service
```