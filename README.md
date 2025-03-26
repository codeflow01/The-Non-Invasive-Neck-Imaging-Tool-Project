# A Mobile Application Prototype for Non-Invasive Cardiovascular Disease Detection Using Neck Imaging
<!-- <span>&nbsp;&#128249;<span> -->
<img alt="Python" src="https://img.shields.io/badge/Python-3.12-4630EB?style=flat-square&labelColor=000000" /><img alt="Typescript" src="https://img.shields.io/badge/TypeScript-5.3-4630EB?style=flat-square&labelColor=000000" /><img alt="ReactNative" src="https://img.shields.io/badge/React Native-0.76-4630EB?style=flat-square&labelColor=000000" /><img alt="Expo SDK" src="https://img.shields.io/badge/Expo-52.0-4630EB?style=flat-square&labelColor=000000" /> 
<!-- dynamic version badges -->
<!-- img alt="Expo SDK Version" src="https://img.shields.io/npm/v/expo.svg?style=flat-square&label=Expo&labelColor=000000&color=4630EB" -->

## Overview

This mobile application prototype serves as a proof of concept, translating ABI’s non-invasive cardiac health assessment research into a practical software solution. It enables real-time cardiac assessment through non-contact detection of carotid artery pulsations. Key functionalities—including video capture or selection from pre-recorded videos, video trimming, precise region-of-interest (ROI) selection, and advanced video processing and analysis—were fully implemented. Detailed analytical outputs were provided for further research, aligning closely with the requirements of ABI researchers and clinicians. UI responsiveness issues encountered during cross-platform development were successfully resolved through targeted optimizations, ensuring a smooth, user-friendly experience on iOS devices and laying a robust foundation for future development and expansion.

![enter image description here](https://github.com/codeflow01/The-Non-Invasive-Neck-Imaging-Tool-Project/blob/main/screencapture.png)

<br>

## Installation

### Prerequisite
Ensure you have the following installed:
- [Node.js](https://nodejs.org/en/)



### Installing Dependencies
In the project directory, install the dependencies using npm:
```bash
npm install
```

### Configuring Frontend Application
1. After installing the dependencies, start the frontend application with the following command:
```bash
npx expo start
```
2. Look for the IP address shown in your terminal. It should look like this: `exp://...(except the ":" and the following last four digits)`. <br>
3. Change the `SERVER_URL` based on this IP address in the following files:<br> 
`app/(tabs)/imaging/camera.tsx`<br>
`app/(tabs)/imaging/picker.tsx`<br>
`app/(tabs)/imaging/roi.tsx`<br>
`app/(tabs)/index.tsx`<br>
`app/(tabs)/insight.tsx` 



### Creating Server Storage Directories
In the server directory, create the necessary directories with the following command:<br><br>
**_For Mac Users:_**
```bash
mkdir server-fastapi-frames-storage server-fastapi-roiFrames-storage server-fastapi-results-storage server-fastapi-video-storage
```
**_For Windows Users:_**
```bash
mkdir "server-fastapi-frames-storage", "server-fastapi-roiFrames-storage", "server-fastapi-results-storage", "server-fastapi-video-storage"
```

### Creating Server Environment File
In the server directory, create an environment file named .env with the following command:<br><br>
**_For Mac Users:_**
```bash
touch .env
```
**_For Windows Users:_**
```bash
ni .env
```
After creating the .env file, open it and add the following environment variables:
```bash
HOST = 0.0.0.0
PORT = 8000
ALLOWED_ORIGINS == [
        "http://localhost:8081",
        # the IP address running the frontend application
        "http://172.23.117.43:8081"
        ]
```



### Activating the Python Virtual Environment
**_For Mac Users:_**
<br><br>
In the server directory, activating the Python virtual environment with the following command:
```bash
source venv/bin/activate
```
**_For Windows Users:_**
<br><br>
1. Remove the existing virtual environment
```bash
Remove-Item -Path "venv" -Recurse -Force
```
2. Create a new virtual environment
```bash
py -3.12 -m venv venv
```
3. Activating the Python virtual environment
```bash
venv/Scripts/activate
```
4. Installing the required packages in the virtual environment
```bash
pip install -r requirements.txt
```
<br>

## Quickstart

### Starting the Server Application
In the server directory, under Python virtual environment, start the server application with the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Starting the Frontend Application
- In the project directory, start the frontend application with the following command:
```bash
npx expo start
```
- Scan the QR code displayed in the terminal. If everything is set up *correctly*, the application should open on your mobile phone.
> Note: Do not start frontend application within the Python virtual environment.
