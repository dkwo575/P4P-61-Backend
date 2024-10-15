# P4P-61-Backend

## Introduction
This project is Part 4 Project #61 from done my Do Jun Kwon and Kim Zuo.
This repository contains code and document for Integrated Plant Monitoring System for estimate tomato harvest time.

## Prerequisites
- Window or Linux os
- Nodejs above version 18
- Anaconda or Miniconda
- Pytorch
- MMDetection (mmcv-full = 1.6.0 and mmdet = 3.1.0)
- XAMPP
- Arduino

### Frontend
Frontend application directory run the following command
```
> npm install
```
then use the following command to run the project
```
> npm run dev
```

### Backend
1. Install Anaconda
2. Create and activate a new Python environment
3. Install PyTorch
4. Use pip to install packages include Flask, SocketIO, pyrealsense2(Any Version is available), MMDetection (mmcv-full = 1.6.0 and mmdet = 3.1.0)


### IoT Sensor system
1. Install Arduino to control MCU with sensors
2. Install XAMPP that can run Apache server and MySQL server to transfer data from MCU to MySQL Database
3. Use the Arduino file names as final.ino
4. Use PhP file to communicate between Apache Web Server and MySQL server.

### Server setup
1. Install Nginx for Frontend and Gunicorn for Backend.
2. Follow the instructions on how to use Nginx and Gunicorn.
3. Then the user can access our web interface


### Key Technology
- TypeScript
- React
- Vite
- Arduino
- PhP
- XAMPP
- Nginx
- Gunicorn
- Flask
- PyTroch
- MMDetection



