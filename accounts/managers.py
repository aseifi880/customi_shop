from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, password: str, email: str=None, phone: str=None):
        """
        Checks if either email or phone is provided if true tries to
        create a new user if given values are valid
        """
        try:
            email = self.normalize_email(email)
            user = self.model(email=email, phone=phone)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            raise ValueError('اطلاعات وارد شده قابل قبول نیست.')

    def create_superuser(self, email, phone, password,**extra_fields):
        if not email and not phone:
            raise ValueError('کاربر باید ایمیل یا تلفن همراه داشته باشد.')
        user = self.model(email=email, phone=phone)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)