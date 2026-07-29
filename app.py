from flask import Flask, render_template, request, redirect, session, flash
import pyrebase

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# === HEI HI I FIREBASE CONFIG IN THLAK RAWH ===
config = {
  "apiKey": "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "authDomain": "your-project.firebaseapp.com",
  "projectId": "your-project",
  "storageBucket": "your-project.appspot.com
