import cv2
import os
import numpy as np
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def capture_face():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_region = frame[y:y+h, x:x+w]
            _, buffer = cv2.imencode('.jpg', face_region)  # Convert face to image format
            cap.release()
            cv2.destroyAllWindows()
            return ContentFile(buffer.tobytes(), "face.jpg")

    cap.release()
    cv2.destroyAllWindows()
    return None

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            face_image = capture_face()

            if face_image:
                user.face_image.save(f"{user.username}.jpg", face_image)  # Save face image
                user.save()
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "register.html", {"form": form, "error": "No face detected! Try again."})

    form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import cv2
import numpy as np
from .models import CustomUser

@login_required
def mark_attendance(request):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            scanned_face = frame[y:y+h, x:x+w]
            scanned_face_gray = cv2.cvtColor(scanned_face, cv2.COLOR_BGR2GRAY)
            scanned_face_resized = cv2.resize(scanned_face_gray, (100, 100))

            user = request.user
            stored_face = cv2.imread(user.face_image.path, cv2.IMREAD_GRAYSCALE)
            stored_face_resized = cv2.resize(stored_face, (100, 100))

            diff = np.abs(stored_face_resized.astype("int") - scanned_face_resized.astype("int")).mean()

            if diff < 40:  # Lower value means closer match
                user.attendance_count += 1
                user.save()
                cap.release()
                return JsonResponse({"message": f"Attendance marked! Count: {user.attendance_count}"})
            else:
                cap.release()
                return JsonResponse({"message": "Face does not match!"}, status=400)

    cap.release()
    return JsonResponse({"message": "No face detected!"}, status=400)


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")  # Redirect to the attendance dashboard

    form = AuthenticationForm()
    return render(request, "logi.html", {"form": form})



def logout_view(request):
    logout(request)
    return redirect("login")
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "dashoard.html")
