open-logger
===========

open source online data logging 

### Installing into Local Virtualenv Development Environment
Install base system packages (Debian based OSes)
```sudo apt-get install python-dev python-virtualenv libpng-dev libfreetype6-dev

Create a virtual environment and activate it
```virtualenv venv --distribute
```source venv/bin/activate

Note that your command-line prompt may now be prepended with "(venv)".  Now packages installed using `pip` will only be in this environment.  Use the command `deactivate` to exit this mode.
Finish installing dependencies
```pip install flask flask-sijax numpy matplotlib pillow

(also install anything else you'll need.)

Check out [the code](https://github.com/dwblair/open-logger.git) from GitHub
```sudo apt-get install git
```git clone https://github.com/dwblair/open-logger.git

Run locally
```cd infrapix
```python runLocally.py

Open browser to url http://127.0.0.1:5000/ to test the web app!

