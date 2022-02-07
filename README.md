# Accesspoint

## Description
I have an accesspoint setup on my RaspberryPI (with hostapd). And I wanted to have the possibility to turn the accesspoint on and off at every point in time without having to open the bash and type in a command. So I created this little website.

## Setup

### Prerequisites 
* **[Python3](https://www.python.org/downloads/)** needs to be setup
  * **[pandas](https://pandas.pydata.org/)** needs to be setup
  * **[websockets](https://websockets.readthedocs.io/en/stable/)** needs to be setup
* **hostapd** needs to be setup ([how I did it](https://gist.github.com/bananensplit/08e7ca5b66565dfad3f8b19a4f1ff728))


### Configure the API (as Service)
Of course you can run the API directly, but in most cases it is more convinient to configure it as a service and be able use different tools (like `systemctl`).

1.  Edit `/etc/systemd/system/ap-api.service`
    ```
    [Unit]
    Description=API for (hostapd) Accesspoint

    [Service]
    Type=simple
    ExecStart=/usr/local/bin/ap-apiap-api.py \
        --port=8001 \
        --log-file=/var/log/ap-api.log \
        --mac-file=/var/ap-api-resources/mac_addresses_28-01-2022.csv \
        -v

    [Install]
    WantedBy=multi-user.target
    ```


2.  Copy the `ap-api.py` to `/usr/local/bin/`
    ```
    sudo cp ~/ap-api.py /usr/local/bin
    sudo chown root:root /usr/local/bin/ap-api.py
    sudo chmod +x /usr/local/bin/ap-api.py
    ```


3.  Copy the `mac_addresses_*.csv` to `/var/ap-api-resources/`
    ```
    sudo mkdir /var/ap-api-resources
    sudo cp ~/mac_addresses_*.csv /var/ap-api-resources/mac_addresses_*.csv
    ```


4.  Reload sysmtectl and start the api
    ```
    sudo systemctl daemon-reload
    sudo systemctl enable ap-api
    sudo systemctl start ap-api
    sudo systemctl status ap-api
    ```


### Setup website
> Note that this assumes that you already setup a webserver like [nginx](http://nginx.org/en/download.html) or [apache2](https://httpd.apache.org/) and know how to add a new site to it.

Copy the content of the `build` folder to your webroot. This should do the trick.


## Usage
Now when everything is setup correctly you should be able to access the webserver and see this little website:  
![site.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/site.png)  
You can turn the Accesspoint off and back on again whenever you want by pressing the buttons.  
![off.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/off.png)
![on.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/on.png)

Also when you connect to your Accesspoint the number of connected clients should go up by one.  
![clients.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/clients.png)  
## Enjoy :)