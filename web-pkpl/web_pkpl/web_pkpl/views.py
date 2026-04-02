# views.py

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
    user_email = None  # placeholder dulu
    
    is_member = is_team_member(user_email)
    
    return render(request, "index.html", {
        "is_member": is_member,
        "user_email": user_email,
    })