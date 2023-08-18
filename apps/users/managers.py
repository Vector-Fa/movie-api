from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, username: str, email: str, password: str, **extra_fields
    ):
        if not username:
            raise ValueError("You have not provided an username")
        if not email:
            raise ValueError("You have not provided an email")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save()
        return user
