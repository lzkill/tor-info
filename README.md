tor-info
========

The files needed to extend RPi-Monitor and show a Tor relay's bandwidth information.

## Introduction ##

[RPi-Monitor](http://rpi-experiences.blogspot.com.br/p/rpi-monitor.html) is a nice monitoring tool for your Raspberry Pi. It provides a web view where you can watch things such as memory, CPU and temperature. If your RPi is running a Tor relay then you can easily extend RPi-Monitor to show how much bandwidth the relay is consumig, the observed bandwidth, the relay's address and so on.

![Stats](https://raw.githubusercontent.com/lzkill/tor-bw/master/stats.jpg)

## License ##

These files may be used under the terms of the MIT License, wich a [copy](LICENSE) is included in the download.

## Dependencies ##

- [Python](https://www.python.org) 2.6 or greater
- [Stem](https://stem.torproject.org) 1.2.2 or greater
- [Supervisor](http://supervisord.org)

## Configuration ##

- Copy [tor.conf](tor.conf) to `/etc/rpimonitor/template/`
- Add the following line to `/etc/rpimonitor/data.conf`
```
include=/etc/rpimonitor/template/tor.conf
```
- Copy [tor.png](tor.png) to `/usr/share/rpimonitor/web/img`
- Copy [tor-bw.conf](tor-bw.conf) and [tor-desc.conf](tor-desc.conf) to `/etc/supervisor/conf.d/`
- Run `sudo groupadd supervisor;sudo usermod -a -G supervisor pi`
- Modify `/etc/supervisor/supervisord.conf` with the following:
```
[unix_http_server]
file=/var/run/supervisor.sock
chmod=0770
chown=root:supervisor
```
- Run `sudo mkdir /usr/local/sbin/rpimonitor/`
- Copy [tor-bw.py](tor-bw.py) and [tor-desc.py](tor-desc.py)to `/usr/local/sbin/rpimonitor`  
- Set your connection parameters on [tor-bw.py](tor-bw.py) (`TOR_CONTROL_PORT`, `TOR_ADDRESS` and `TOR_CONTROLLER_PASSWD`)
- Set your relay's fingerprint on [tor-desc.py](tor-desc.py) (`FINGERPRINT`)
- Logout/login and run `sudo service supervisor restart;sudo service rpimonitor restart`

The traffic graph shows the values of `RelayBandwidthRate` and `RelayBandwidthBurst` if these parameters are set in `torrc`.

## Your Improvements ##

If you add improvements to these files please send them to me as pull requests on GitHub. I will add them to the next release so that everyone can enjoy your work. You might also benefit from it as others may fix bugs in your files or may continue to enhance them.

## Thanks ##

With regards from

[Luiz Kill](mailto:me@lzkill.com)

