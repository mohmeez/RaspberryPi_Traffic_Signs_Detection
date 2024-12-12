# RaspberryPi_Traffic_Signs_Detection
Overview

This project utilizes a Raspberry Pi 4 and a standard webcam to build a real-time object detection system using YOLO (You Only Look Once). The setup involves configuring the Raspberry Pi OS, setting up a Python virtual environment, and installing necessary libraries to facilitate model building and detection.
Features

    Real-time object detection using YOLO
    Lightweight setup suitable for Raspberry Pi 4
    Remote development using SSH and Visual Studio Code
    Modular and easily extendable codebase

Prerequisites
Hardware

    Raspberry Pi 4
    MicroSD card (16GB or higher recommended)
    Power supply for Raspberry Pi
    Standard USB webcam
    Keyboard and portable display for initial setup
    PC or laptop if you plan to remote SSH into the pi

Software

    Raspberry Pi OS Full Desktop
    Visual Studio Code (if you plan to ssh into the pi from your PC or Laptop)
    Python 3.7 or higher (raspberry pi OS comes with the latest Python 3.12)

## Hardware Setup / Installation

Follow these steps to set up your Raspberry Pi for the YOLO Detection Project.
1. Install Raspberry Pi OS

    Download Raspberry Pi OS Full Desktop:
        Visit the Raspberry Pi Downloads page and download the full desktop version of Raspberry Pi OS.
   
   ![image](https://github.com/user-attachments/assets/e7fdf186-5cd4-4a05-957e-85ffc49688a3)

    USE CTRL + SHIFT + X to open up Advanced options and enable SSH and enter your wifi details for the pi to connect to wifi
   
    ![Screenshot from 2024-12-11 11-26-54](https://github.com/user-attachments/assets/904d6a14-2625-40b1-9498-ea531fecffd8)



    Flash the OS Image:
        Use Raspberry Pi Imager or a tool like Etcher to flash the downloaded image onto your microSD card.
  
    Insert and Boot:
        Insert the microSD card into your Raspberry Pi 4, connect the keyboard and display, and power it on.

2. Connect Peripherals

    Keyboard and Display: Connect a USB keyboard and a portable display to your Raspberry Pi.
    Webcam: Connect your standard USB webcam to one of the Raspberry Pi’s USB ports.


3. Update the System

    Open Terminal:
        Click on the terminal icon or press Ctrl + Alt + T to open the terminal.

   Chech usb devices attached:

       lsusb
   
   You Should see a list of usb devices connected (USB camera, keyboard, hdmi display)

    Update and Upgrade Packages:

        sudo apt update
        sudo apt upgrade -y


4. Set Up SSH for Remote Development

    Enable SSH:
        Open Raspberry Pi Configuration from the Preferences menu.
        Navigate to the Interfaces tab and enable SSH.

    Find Raspberry Pi IP Address:

        hostname -I

   Note the IP address for SSH access.

   Connect via Visual Studio Code:
   Install the Remote - SSH extension in Visual Studio Code.
   CTRL SHIFT P to open up the commad pallate 
   
   Use the IP address to establish an SSH connection.

       ssh <raspberrypiUsername>@ <apaddress>

   Add your username and ip and you will be prompted for your pi password for authentication and Voila you are in.

5. Create a Virtual Environment
    
        Navigate to Your Project Directory:
    
      cd ~
      mkdir detection
      cd detection
      
      Create a Virtual Environment:
      
      python3 -m venv yolo
      
      Activate the Virtual Environment:
      
          source yolo/bin/activate
    
6. Install Required Libraries
    
   To simplify the installation of Python dependencies, a requirements.txt file is provided. This allows users to install all necessary libraries with a single command.
    
        Create requirements.txt:
    
   Create a requirements.txt file inside the detection folder with the following content:
    
      ultralytics
      torch
      opencv-python
      
      Install Libraries Using requirements.txt:
      
      With the virtual environment activated, run:
      
          pip install -r requirements.txt
      
     This command will install all the required Python libraries listed in the requirements.txt file.

## Build and train model locally 
  1. Dataset Preparation
  
      
     Download the traffic sign dataset from Roboflow: 
    
                https://universe.roboflow.com/project-sign-detection/traffic-sign-cdfml
            
     The dataset will be downloaded as a zipped file.
  
  2. Unzip Dataset:
     
      Unzip the downloaded file. After unzipping, you should have three folders: train, val, and test containing the images along with their corresponding labels for bounding boxes.


      Folder Structure Should look something like this:
    
          Project Root
          │
          ├── data
          │   ├── test
          │   │   ├── images
          │   │   └── labels
          │   ├── train
          │   │   ├── images
          │   │   └── labels
          │   ├── valid
          │   │     ├── images
          │   │     ├── labels
          │   ├── data.yaml
          │   ├── README.dataset.txt
          │   └── README.roboflow.txt
          │
          ├── runs
          │   └── train
          │       └── weights
          │           └── best.pt
          │
          ├── scripts
          │   |── train.ipynb
          │
          └── yolo_env
              ├── yolov8n.pt
              └── yolov11n.pt

      
  
  4. Configure Dataset Path:
     
        Locate the data.yaml file within the dataset directory.

        The data.yaml file show the number of classes and shows them as a list. The model will only use this for training and detection.
         
        Update the paths for train, test, and val in the data.yaml file to point to the respective folders. This file is used by the model to retrieve the dataset paths.
  
  6. Model Training
  
      Training Notebook:
            Open the train.ipynb Jupyter notebook included in the dataset. This notebook is configured to use a pre-trained YOLOv8n model.
      
      Run Training:
            Execute the cells in the notebook to start training the model on your local machine using the provided dataset.
            The model will automatically save the best weights based on the training performance to runs/train/weights/best.pt.

      Run Inference on test images locally:

     ![predicted_image](https://github.com/user-attachments/assets/938ee75b-d269-45bb-b7f9-99c9c37da864)

      After successfully running inference locally, we are reasy to deploy this model onto the raspberry pi for testing on live camera feed.

         

## Model Deployment (can hook up the raspberry pi to your power source in the car and take it out for a test trive and detect traffic signs) & Voila its really just that simple.

  1. Transfer Weights:
      After training, transfer the best.pt file to your Raspberry Pi. This can be done via secure copy (SCP) with the following command:

          scp best.pt rasppi@ipaddress:~/

      Alternatively, you can transfer the weights using a USB drive.

  2. Run Inference on live feed from your webam connected to the raspberry pi:
    
        Load the transferred best.pt weights in your YOLO environment on the Raspberry Pi. (refer to the yolo_inference.py file foe details)
        Set up a webcam and run inference on the live video feed to detect traffic signs in real-time.

  3. Create a shell script named start_yolo.sh (attached in the repo) This script is in the user foler.
  
     The function if this script is to activate the virtual environment and run the yolo_inference.py Python script on the RaspberryPi

     After transfering the saved yolo model weights, the yolo_inference.py and the start_yolo shell script to the Raspberry pi, run the shell script using the follwoing command in the terminal:

            bash start_yolo.sh

Congratulations! You have now succesfully delployed a YOLO model for object detection on an IOT edge device. Safe Driving!
