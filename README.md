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
  data-www ALL=(root) /pathBlaBlaBla/ap-control.py
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

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
