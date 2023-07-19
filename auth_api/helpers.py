from .models import User
from django.forms import model_to_dict

def get_full_user(data):
    excluded_values = ["password", "last_login",
                       "is_superuser", "first_name",
                       "last_name", "is_staff",
                       "is_active", "date_joined",
                       "permissions", "groups",
                       "user_permissions"]
    user = User.objects.get(id=data.get("user"))
    data["user"] = model_to_dict(user, exclude=excluded_values)
    return data