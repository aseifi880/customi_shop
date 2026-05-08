from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, phone=None):
        if (not email) and (not phone):
            raise ValueError('کاربر باید ایمیل یا تلفن همراه داشته باشد.')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, email, phone, password,**extra_fields):
        if not email and not phone:
            raise ValueError('کاربر باید ایمیل یا تلفن همراه داشته باشد.')
        user = self.model(email=email, phone=phone)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)