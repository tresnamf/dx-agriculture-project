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

#### 3. Checking the Python environment and installing libraries on Raspberry Pi
- By default, Raspberry Pi OS comes with Python pre-installed.
- Open terminal, type:~ $ python3 --version
- The output will display the Python version in use, for example:~ $ Python 3.x.x

#### 4. Building Web-based Automatic Sensor Logger for Experimental Monitoring

![diagram-iot-dx-agri (1)](https://github.com/user-attachments/assets/72ac5ae4-e831-4d83-a845-e09eae95133a)


- Download project repository:~ $ git clone https://github.com/tresnamf/dx-agriculture-project.git
- :~ $ cd dx-agriculture-project
- :~ $ sudo python3 -m venv myenv
- :~ $ source myenv/bin/activate
- :~ $ pip install flask
- :~ $ pip install adafruit-circuitpython-sht31d
- :~ $ python3 app.py
<br/> <img width="563" height="363" alt="Screenshot 2026-02-08 at 13 11 13" src="https://github.com/user-attachments/assets/6850c4dd-3c4c-48b8-b23a-ec1bf9fa7ae3" />
- Open new tab browser, then type: http://localhost:5000
<br/> <img width="1425" height="848" alt="Screenshot 2026-02-08 at 13 12 40" src="https://github.com/user-attachments/assets/cad1995e-2936-46e4-816a-82bca2e3da53" />
- To create and manage a database using SQLite3, open a new terminal and type:
- :~ $ sqlitebrowser
- Wait for the GUI to appear > select menu **Open Database** > browse and select the project database named: **dx_agri_project.sql3**
<br/><img width="1063" height="711" alt="Screenshot 2026-02-08 at 13 30 57" src="https://github.com/user-attachments/assets/b35ed80f-7ff8-452e-8f94-ec0f9efa24cb" />
- Also make sure to adjust the database path location (*.sql3) in Python code **db_path=**, which is specified in both _app.py_ and _observation_routes.py_.
- Test the system by filling the field of **Day of Experiment, Observation Time, Treatment, and Recording Duration**, then click button **Start** and wait until the recording process is completed.

#### 5. Building Web-based Plant Growth Observation System

![diagram-iot-dx-agri2](https://github.com/user-attachments/assets/57d877cd-fe8d-4c98-a974-a54907f7bd52)

- Please navigate to http://localhost:5000/observation
- User allows to add,insert,edit, dan delete observation data
- Users can add new observation data by filling in the fields  **Height (cm), Day of Experiment, Observation Time, Treatment, dan Notes**
<br/> <img width="1425" height="857" alt="Screenshot 2026-02-08 at 14 30 30" src="https://github.com/user-attachments/assets/c547326c-6a15-44d3-b4ed-b7ebf086f8bd" />
- Users can also edit previously entered observation data
<img width="1425" height="857" alt="Screenshot 2026-02-08 at 14 32 45" src="https://github.com/user-attachments/assets/ca21b1f4-df95-4b05-8cb3-56a83b038d08" />

#### 6. Analyzing and Visualizing Sensor and Plant Growth using Grafana

- Install basic dependency, type: ~ $sudo apt install -y apt-transport-https software-properties-common wget
- Grafana GPG key for official packet verification, type:~ $ sudo mkdir -p /etc/apt/keyrings
  wget -q -O - https://apt.grafana.com/gpg.key | \
  gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
- Add Grafana repository, type:~ $ echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | \
  sudo tee /etc/apt/sources.list.d/grafana.list
- Install Grafana, type:~ $ sudo apt install grafana -y
- Start Grafana service, type:~ $ sudo systemctl start grafana-server
- Open new tab browser: navigate to http://localhost:3000
<img width="800" height="500" alt="Screenshot 2026-02-08 at 15 38 30" src="https://github.com/user-attachments/assets/fff6a52b-8c65-4c6a-8d2f-f9d26b68f3c3" />

- Install SQLite plugin, type:~ $ grafana-cli plugins install frser-sqlite-datasource
- Check the installed plugin, Home > Plugins and data > Plugins
<br/><img width="800" height="500" alt="Screenshot 2026-02-08 at 15 39 18" src="https://github.com/user-attachments/assets/307990c2-712d-430e-8ed6-f3bfbeff95cd" />
- Please navigate to http://localhost:3000/dashboards > New > Import
- Drag and drop **PlantGrowthViz-1770467082684.json** to Grafana's import dashboard
<br/><img width="862" height="628" alt="Screenshot 2026-02-08 at 15 44 26" src="https://github.com/user-attachments/assets/f2493637-b201-4e74-a3d3-a73f3d890b04" />
- Click imported dashboard, it will be redirected to dashboard project
- Please configure first the database connection, navigate to Home > Connections > Data Sources > Add new data sources > Select SQLite and filling the field below
<br/><img width="1425" height="857" alt="Screenshot 2026-02-08 at 15 50 51" src="https://github.com/user-attachments/assets/3f165c5b-2628-43f2-906a-3e5e95330012" />
- Navigate to dashboard project, Grafana will display below
- Environmental Condition & Plant Growth Summary
<br/> <img width="1425" height="857" alt="Screenshot 2026-02-08 at 15 53 59" src="https://github.com/user-attachments/assets/a9764052-44dc-44e7-8c74-6e6665151297" />
- Trend Over 10 Days
<br/> <img width="1425" height="857" alt="Screenshot 2026-02-08 at 15 54 33" src="https://github.com/user-attachments/assets/634dddae-39ae-4421-9c54-ff04c264ac48" />
- Correlation Analysis
<br/> <img width="1425" height="857" alt="Screenshot 2026-02-08 at 15 55 03" src="https://github.com/user-attachments/assets/fa0fddf9-2f14-45cd-8ee1-47cafb254456" />

<br/> 
<br/> 
<br/> 
Feel free to fork this repository, submit pull requests, or open issues.
Any contributions are welcome and appreciated.

<br/> 
<img width="220" height="67" alt="image" src="https://github.com/user-attachments/assets/b5bf517b-72b3-4273-a1e3-3d732067a780" />
<br/> 
Tresna Maulana Fahrudin
<br/> 
PhD Student
<br/> 
Graduate School of Environmental, Life, Natural Science and Technology
<br/> 
Division of Environmental, Life, Natural Science and Technology
<br/> 
Information and Communication Systems Course
<br/> 
Distributed System Design Laboratory


