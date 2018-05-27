from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        is_superuser = extra_fields.pop('is_superuser', None)
        is_staff = extra_fields.pop('is_staff', None)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        if is_superuser is not None:
            user.is_superuser = is_superuser
            user.account_type = 'superuser'
        if is_staff is not None:
            user.is_staff = is_staff
            user.account_type = 'admin'
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone_number, date of
        birth and password.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Creates and saves a superuser with the given phone_number, date of
        birth and password.
        """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault('account_type', 'superuser')
        return self._create_user(phone_number, password, **extra_fields)
