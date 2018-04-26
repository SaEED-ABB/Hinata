from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password):
        """
        Creates and saves a User with the given phone_number, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password):
        """
        Creates and saves a superuser with the given phone_number, date of
        birth and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user