import requests
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleAuthProvider:
    def __init__(self, token):
        self.token = token
    
    def validate_token(self):
        print("Validating token")
        r = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
        )
        r.raise_for_status()
        self.user = r.json()

    def get_decoded_data(self):
        try:
            self.validate_token()
        except Exception:
            error = {"message": "Google token invalid."}
            raise ValidationError(error)
        else:
            return {
                "username": self.user["name"],
                "email": self.user["email"],
                "image": self.user["picture"],
            }

def create_token(user):
    refresh = RefreshToken.for_user(user=user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }