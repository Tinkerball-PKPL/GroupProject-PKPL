# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .oauth_client import SimpleOAuth2Client  # Pastikan file oauth_client.py ada sejajar dengan views.py
import urllib.parse
import secrets
from django.conf import settings
# Whitelist email anggota kelompok
TEAM_EMAILS = [
    "nay.kenara@gmail.com",
    "febifey242@gmail.com",
    "gstniera@gmail.com",
    "kh.adzkiyah@gmail.com",
    "delilaisrn@gmail.com"
]

def is_team_member(email):
    if not email:
        return False
    return email.lower() in [e.lower() for e in TEAM_EMAILS]

def index(request):
    # Nanti diisi Anggota 2 
    # user_email = request.session.get("user_email")
    user_email = request.session.get("user_email") # placeholder dulu
    
    is_member = is_team_member(user_email)
    
    return render(request, "index.html", {
        "is_member": is_member,
        "user_email": user_email,
    })

def get_oauth_client():
    # Ganti dengan Client ID dan Secret milikmu
    return SimpleOAuth2Client(
        client_id=settings.GOOGLE_CLIENT_ID, 
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        auth_url="https://accounts.google.com/o/oauth2/auth",
        token_url="https://oauth2.googleapis.com/token",
        redirect_uri="http://localhost:8000/callback",
        scope="openid profile email"
    )

def login_google(request):
    """Fungsi ini dipanggil saat tombol 'Login with Google' di HTML diklik"""
    client = get_oauth_client()
    state = secrets.token_urlsafe(16)
    request.session['oauth_state'] = state
    
    # Buat link untuk diarahkan ke halaman login Google
    params = {
        'client_id': client.client_id,
        'redirect_uri': client.redirect_uri,
        'scope': client.scope,
        'response_type': 'code',
        'state': state
    }
    auth_url = f"{client.auth_url}?{urllib.parse.urlencode(params)}"
    
    # Arahkan user ke Google
    return redirect(auth_url)

def callback(request):
    """Google akan mengirim data kembali ke fungsi ini setelah user pilih akun"""
    code = request.GET.get('code')
    
    if not code:
        return HttpResponse("Gagal login: Authorization code tidak ditemukan.")
        
    client = get_oauth_client()
    
    try:
        # Tukarkan code dengan access token (Ini otomatis by-pass terminal browser)
        client.get_token(code=code)
        
        # Minta informasi profil (Email & Nama)
        response = client.make_api_request("https://www.googleapis.com/oauth2/v2/userinfo")
        user_info = response.json()
        
        # SIMPAN EMAIL KE SESSION (Ini yang ditunggu-tunggu Anggota 3!)
        request.session["user_email"] = user_info.get("email")
        request.session["user_name"] = user_info.get("name")
        
        # Kembalikan ke halaman utama
        return redirect('index')
    except Exception as e:
        return HttpResponse(f"Terjadi kesalahan saat otentikasi: {str(e)}")

def logout(request):
    """Fitur tambahan: Tombol untuk keluar"""
    request.session.flush() # Hapus semua data login
    return redirect('index')