from .models import User
from django.forms import model_to_dict

def get_full_user(data):
    user = User.objects.get(id=data.get("user"))
    data["user"] = model_to_dict(user)
    return data