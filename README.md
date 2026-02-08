# ICT Agriculture Practice
Development of an IoT-Based Web Application for Monitoring Temperature and Humidity of Mung Bean Sprout Growth in Indoor and Outdoor Environments 

<b> Motivation </b> <br/>
<img width="350" height="200" alt="image" src="https://github.com/user-attachments/assets/d00c256b-dfe2-45d2-b89d-59310af2f3c3" />


<b> Objective </b> <br/>
<img width="722" height="226" alt="image" src="https://github.com/user-attachments/assets/fd98f70c-a5d4-4dd9-8adf-bdefe96b0f77" />

<b> Required Equipment and Environment </b> <br/>
<img width="450" height="300" alt="image" src="https://github.com/user-attachments/assets/caa34eac-b181-437c-b08b-4f154e4dd270" />


<b> System Overview </b> <br/>
<img width="650" height="350" alt="image" src="https://github.com/user-attachments/assets/51081b9e-a1be-4490-8e5f-0f6a78ec0329" />

<b> Experimental Scenario </b> <br/>
<img width="650" height="350" alt="image" src="https://github.com/user-attachments/assets/eaf72188-9077-4f6c-8a9d-3e425dd184c5" />

### Experimental Setup </b> <br/>

#### 1. Sensor Connections
<img width="524" height="361" alt="image" src="https://github.com/user-attachments/assets/a3d38a81-353f-4be1-9cd5-005598ef16e8" /> <br/>
- Open terminal, type :~ $ sudo apt update
- :~ $ sudo apt install -y i2c-tools
- :~ $ sudo raspi-config
- Interface Options → I2C → Enable
<br/><img width="561" height="361" alt="Screenshot 2026-02-08 at 11 35 27" src="https://github.com/user-attachments/assets/7dcbc2e5-c830-4fac-8a20-5982e6000c63" />
- :~ $ sudo reboot
- :~ $ sudo i2cdetect -y 1
<br/> <img width="403" height="142" alt="Screenshot 2026-02-08 at 11 36 59" src="https://github.com/user-attachments/assets/180a47e0-759b-4c40-b927-1d3eb0ee705a" />
<br/> Note: The output terminal show that I2C interface is active and the sensor is detected, while 0x44 is the I2C address of the SHT3X / SHT31D sensor.

#### 2. Flash Raspberry Pi
- Prepare a microSD card (at least 16GB is recommended) and a card reader
- Download Raspberry Pi Imager (according to your PC operating system): https://www.raspberrypi.com/software/
- Run Raspberry Pi Imager
- Open the Imager: launch the application and select "Choose OS" to choose the operating system
- Select Storage: click "Choose Storage" and select your microSD card
- Click "Write" to start the flashing process and wait until verification is completed
- After completion, remove the microSD card and insert it into the Raspberry Pi 4 for the first boot

#### 3. Memeriksa Python environment dan install library in Raspberry Pi
- By default, Raspberry Pi OS comes with Python pre-installed.
- Open terminal, type:~ $ python3 --version
- The output will display the Python version in use, for example:~ $ Python 3.x.x

#### 4. Building Web-based Automatic Sensor Logger for Experimental Monitoring
- Download project repository:~ $ git clone https://github.com/tresnamf/dx-agriculture-project.git
- :~ $ cd dx-agriculture-project
- :~ $ sudo python3 -m venv myenv
- :~ $ source myenv/bin/activate
- :~ $ pip install flask
- :~ $ pip install adafruit-circuitpython-sht31d
- :~ $ python3 app.py
<br/> <img width="563" height="363" alt="Screenshot 2026-02-08 at 13 11 13" src="https://github.com/user-attachments/assets/6850c4dd-3c4c-48b8-b23a-ec1bf9fa7ae3" />
- Open new tab browser, then type: http://localhost:5000
<img width="1425" height="848" alt="Screenshot 2026-02-08 at 13 12 40" src="https://github.com/user-attachments/assets/cad1995e-2936-46e4-816a-82bca2e3da53" />
- 





