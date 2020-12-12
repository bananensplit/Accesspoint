# Accesspoint

## Description
I have an accesspoint setup on my RaspberryPI (with hostapd).
And I wanted to have the possibility to turn the accesspoint on and off at every point in time without having to open
the bash and type in a command. So I created this little website.

## How to setup
To setup this little Website on your own, do the following steps
* Make sure **apache2** or any other webserver is setup
* Make sure **php** is setup
* Make sure you have **python3** installed
* Make sure **hostapd** is setup. I used [this](https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md)
  guide to set it up on my raspberry pi.
* Make sure the user of the webserver has the ability to execute the python files with sudo priviledges.
  I did this by adding data-www (user that apache uses) to /etc/sudoers  
  ```shell
  data-www ALL:(root) /pathBlaBlaBla/ap-control.py
  # would allow user 'data-www' to execute ap-control.py with root priviledges without asking for a password. 
  ```
  I know this **is not** the safest solution but couldn't find another that worked for me (Suggestions are very welcome)

## Usage
Now when you access the webserver you should see this little website.
Now when everything is setup correctly you should be able to access the webserver and see this little website:  
![site.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/site.png)  
You can turn the Accesspoint off and back on again whenever you want by pressing the buttons.  
![off.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/off.png)
![on.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/on.png)

Also when you connect to your Accesspoint the number of connected clients should go up by one.  
![clients.png](https://raw.githubusercontent.com/bananensplit/AccessPoint/media/clients.png)  
If this dosn't happen check if the name of your wlan interface is correct in getData.py:
```python
...
command = 'iw dev <INTERFACE NAME> station dump | grep Station | wc -l'.split(' | ')
...
```
if not replace it with the proper one.

## Enjoy :)