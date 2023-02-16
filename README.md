# <p align="center">🔥 Fire Fighter Z 🔥</p>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/flavtor/Fire_Fighter_Z">
    <img src="src/assets/Logo/Logo.png" alt="Logo" width="315" height="131">
  </a>
   <p align="center">
     An awesome Zombie Cards Game!
   </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About the Project</a></li>
    <li><a href="#-features">Features</a></li>
    <li><a href="#%EF%B8%8F-tech-stack">Tech Stack</a></li>
    <li><a href="#-getting-started">Getting Started</a></li>
    <li><a href="#%EF%B8%8F-install-dependencies">Install Dependencies</a></li>
    <li><a href="#%EF%B8%8F-key-configuration">Key Configuration</a></li>
    <li><a href="#-running-the-application">Running the Application</a></li>
    <li><a href="#authors">Authors</a></li>
  </ol>
</details>

## About The Project

Fire Fighter Z is a web game application that was created as a school project within one week. Players take turns using cards with various abilities to combat enemies.

![fire fighter z demo](https://user-images.githubusercontent.com/74910872/216054259-23a2b3e1-1873-4b09-8a87-6768ca80541e.png)

## 🧐 Features    
- User authentication system: Users can log in using their username and password.
- Database: Store all the information about the cards and players in the game.
- Draw Cards: Users can draw cards from the deck and store them in their personal collection.
- Combat System: You can use your cards to defeat zombies.
- Rest API

## 🛠️ Tech Stack

This project is built with the Flask framework for Python, and uses Firebase for database management. The project uses Cross-Origin Resource Sharing (CORS) to handle cross-domain requests.

The front-end of the project is built using Parcel, a fast, zero-configuration web application bundler. We developed in native javascript for the interface and logic of the game.
        
- [Flask](https://github.com/pallets/flask)
- [Firebase](https://firebase.google.com/)
- [Parcel](https://github.com/parcel-bundler/parcel)

# 🚀 Getting Started

## 🛠️ Install Dependencies

To run the database, you need the following:
- Node.js and npm (included with [Node.js](http://nodejs.org/))
- Python 3.7.9
- - Firebase is currently only up to date with this version of Python, so you need to install it to run the database. You can download it from the [Python](https://www.python.org/downloads/windows/) website.
- Flask
- - You can install Flask using the following command:
```bash
pip install flask
```
- Firebase
- - You can install Firebase using the following command:
```bash
pip install firebase_admin
```
- Flask-CORS
- - You can install Flask-CORS using the following command:
```bash
pip install flask_cors
```

## 🗝️ Key Configuration
In addition to the above requirements, you also need to set up the key.json file. This file contains the credentials for accessing your Firebase project, and is required for the database to connect to Firebase.

You can generate the key.json file by following these steps:

1. Go to the Firebase Console.
2. Select the project that you want to use for the database.
3. Click on the "Settings" icon (gear icon) and select "Project settings".
4. Navigate to the "Service Accounts" tab.
5. Click on the "Generate new private key" button.
6. A key.json file will be downloaded. Save this file in the same directory as the database code.

## 🏃 Running the Application

To run the application, follow these steps:

1. Navigate to the root directory of the project in your terminal.
2. Run the following command to install the dependencies:
```bash
npm install
```
3. Start the Flask server by running:
```bash
python server/app.py
```
4. Start the frontend by running:
```bash
npm start
```

Now you should be able to access the application in your browser at http://localhost:1234. Note that it might be running on a different port.

## Authors

- [@agahakan](https://www.github.com/agahakan)
- [@MaximePETIT-code](https://www.github.com/MaximePETIT-code)
- [@flavtor](https://github.com/flavtor)
