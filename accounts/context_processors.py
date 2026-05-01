"""
accounts/context_processors.py
Injects `is_admin` boolean into every template context so templates
never need to call user.userprofile.role directly (which crashes for
anonymous users and users without a profile).
"""


def user_role(request):
    user = request.user
    is_admin = False

    if user.is_authenticated:
        if user.is_superuser:
            is_admin = True
        else:
            try:
                is_admin = user.userprofile.role == 'admin'
            except Exception:
                is_admin = False

    return {'is_admin': is_admin}
