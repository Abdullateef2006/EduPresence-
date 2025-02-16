from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
import cv2
import datetime
import time
import threading
from .models import Attendance
from .forms import *
from .face_recognition_attendance import load_user_profile_encoding, compare_faces

# ✅ Lock to prevent multiple video streams running at the same time
camera_lock = threading.Lock()

# 📌 User Signup Viewfrom django.shortcuts import render, redirect
from .forms import SignUpForm

def sign_up(request):
    """Handles user registration"""
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form, 'error': '❌ Registration failed. Check errors below.'})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


# 📌 User Login View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User

def log_in(request):
    """Login function allowing Matric Number login"""
    if request.method == 'POST':
        matric_number = request.POST['matric_number']
        password = request.POST['password']

        try:
            user = User.objects.get(matric_number=matric_number)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user)
            return redirect('live_feed')
        else:
            return render(request, 'login.html', {'error': '❌ Invalid Matric Number or Password'})

    return render(request, 'logi.html')


# 📌 Logout View
@login_required
def log_out(request):
    logout(request)
    return redirect('login')

# 📌 Renders the Live Feed Template
@login_required
def live_feed(request):
    return render(request, 'live_feed.html')

import geopy.distance  # ✅ Import geopy for distance calculation

def is_within_allowed_location(user_lat, user_long, allowed_lat, allowed_long, radius):
    """Checks if the user's location is within the allowed area."""
    user_coords = (user_lat, user_long)
    allowed_coords = (allowed_lat, allowed_long)
    distance = geopy.distance.geodesic(user_coords, allowed_coords).meters
    return distance <= radius

from django.http import JsonResponse

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_GET
import cv2
import datetime
from .models import AttendanceControl, Attendance

@require_GET
def check_attendance_status(request):
    """Check if attendance can be marked for current location"""
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    try:
        attendance_control = AttendanceControl.objects.get(id=1)
    except AttendanceControl.DoesNotExist:
        return JsonResponse({'error': 'Attendance system not configured'}, status=500)

    if not attendance_control.is_open:
        return JsonResponse({
            'error': 'Attendance system is currently closed',
            'status': 'closed'
        }, status=403)

    if not is_within_allowed_location(lat, lon,
                                    attendance_control.allowed_latitude,
                                    attendance_control.allowed_longitude,
                                    attendance_control.radius_meters):
        return JsonResponse({
            'error': 'You must be within campus premises to mark attendance',
            'status': 'outside'
        }, status=403)

    return JsonResponse({'status': 'ok'})

def video_feed(request):
    """Streams video and performs face recognition only if attendance is open and user is in the allowed location."""
    camera = cv2.VideoCapture(0)
    user = request.user
    profile_picture_path = user.profile_picture.path if user.profile_picture else None
    user_encoding = load_user_profile_encoding(profile_picture_path)

    if user_encoding is None or len(user_encoding) == 0:
        camera.release()
        return render(request, 'error.html', {'error': 'No valid face encoding found in profile picture'})

    attendance_control, created = AttendanceControl.objects.get_or_create(id=1)

    def generate_frames():
        attendance_marked = False  # Track attendance status

        while True:
            success, frame = camera.read()
            if not success:
                break

            # ✅ Get user's location from request parameters
            user_lat = float(request.GET.get("latitude", 0))
            user_long = float(request.GET.get("longitude", 0))

            # ✅ Check if attendance is open and user is in allowed location
            if attendance_control.is_open and is_within_allowed_location(
                user_lat, user_long, attendance_control.allowed_latitude, attendance_control.allowed_longitude, attendance_control.radius_meters):

                match_found, face_locations = compare_faces(frame, user_encoding)

                for (top, right, bottom, left) in face_locations:
                    color = (0, 255, 0) if match_found else (0, 0, 255)
                    label = "Attendance Marked" if match_found else "Face Not Recognized"

                    if match_found and not attendance_marked:
                        today = datetime.date.today()
                        if not Attendance.objects.filter(user=user, date=today).exists():
                            user.attendance_count += 1
                            user.save()
                            Attendance.objects.create(user=user)
                            attendance_marked = True  # ✅ Prevent duplicate marking

                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            else:
                cv2.putText(frame, "Attendance is Closed or Outside Allowed Area", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame")  

from django.http import HttpResponseForbidden

@login_required
def dash(request):
    if not request.user.is_superuser:
        return render(request, 'admi_access.html', {})
        

    users = User.objects.all()
    return render(request, 'dashboard.html', {'users': users})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import AttendanceControl, Attendance

@login_required
def admin_dashboard(request):
    """Admin page to control attendance and set allowed location."""
    if not request.user.is_superuser:
        return render(request, 'admin_access.html', {})

    attendance_control, created = AttendanceControl.objects.get_or_create(id=1)
    users = User.objects.all()

    if request.method == "POST":
        if "open" in request.POST:
            attendance_control.is_open = True
        elif "close" in request.POST:
            attendance_control.is_open = False
        elif "update_location" in request.POST:
            attendance_control.allowed_latitude = float(request.POST["latitude"])
            attendance_control.allowed_longitude = float(request.POST["longitude"])
            attendance_control.radius_meters = float(request.POST["radius"])
        attendance_control.save()
    

    return render(request, "admin_dashboard.html", {"attendance_control": attendance_control, 'users' : users})
