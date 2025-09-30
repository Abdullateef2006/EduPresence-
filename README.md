# 🎯 Face Recognition Attendance System

A comprehensive Django-based attendance system that uses facial recognition technology with geolocation verification to ensure secure and accurate attendance marking.

---

## 🌟 Core Features

### 🔐 Authentication & User Management
- Matric Number Login - Unique identifier for students  
- User Registration with profile pictures  
- Admin Dashboard for system management  
- Role-based Access (Students vs Administrators)  

### 📸 Face Recognition Technology
- Real-time Face Detection using **OpenCV**  
- Face Encoding & Matching with **face_recognition** library  
- Profile Picture Processing for user enrollment  
- Similarity Threshold (0.4 tolerance) for accurate matching  

### 📍 Geolocation Verification
- Location-based Attendance - must be within campus premises  
- Configurable Allowed Area (latitude, longitude, radius)  
- Real-time GPS Validation before marking attendance  
- Distance Calculation using **geopy**  

### ⏰ Attendance Management
- Daily Attendance Tracking - prevents duplicate entries  
- Attendance Count per user  
- Admin Control to open/close attendance system  
- Automatic Date Stamping  

### 🎥 Live Video Streaming
- Real-time Video Feed from webcam  
- Face Recognition Overlay with bounding boxes  
- Attendance Status Display (Marked/Not Recognized)  
- Streaming HTTP Response for live feed  

---

## 🛠️ Technology Stack

**Backend Framework**
- Django 4.2+  
- Python 3.8+  

**Computer Vision & AI**
- OpenCV  
- face_recognition  
- NumPy  

**Geolocation & Mapping**
- geopy  
- Browser-based GPS integration  

**Frontend & UI**
- HTML / CSS / JavaScript  
- Streaming Responses for live feed  
- Responsive Design (mobile-friendly)  

---

## 📋 Prerequisites
- Python 3.8+  
- Django 4.2+  
- Webcam access  
- GPS/location services (for mobile devices)  
- face_recognition dependencies (dlib, cmake)  

---

## 🏗️ Project Structure

**Models**
- `User` – extended AbstractUser with matric number & profile picture  
- `Attendance` – tracks user attendance with dates  
- `AttendanceControl` – system settings for attendance control  

**Views**
- Authentication – `sign_up`, `log_in`, `log_out`  
- Attendance – `live_feed`, `video_feed`, `check_attendance_status`  
- Admin – `admin_dashboard`, `dash`  

**Utilities**
- `face_recognition_attendance` – encoding & comparison logic  
- `geolocation` – distance calculation & location verification  

---

## 🛣️ URL Endpoints

### Authentication
- `/signup/` – User registration with matric number  
- `/login/` – Matric number-based login  
- `/logout/` – User logout  

### Attendance System
- `/live_feed/` – Main attendance interface  
- `/video_feed/` – Live video stream with face recognition  
- `/check_attendance_status/` – Geolocation validation API  

### Admin Management
- `/admin_dashboard/` – System control panel  
- `/dashboard/` – User management interface  

---

## ⚙️ Installation & Setup

### 1. Clone and Setup Environment
```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install django
pip install opencv-python
pip install face-recognition
pip install numpy
pip install geopy
pip install pillow
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
