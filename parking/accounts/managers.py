from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email), password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(
            self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        return self.create_user(
            email=email, password=password, **extra_fields)

    def create_superuser(
            self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        return self.create_staffuser(
            email=email, password=password, **extra_fields)
