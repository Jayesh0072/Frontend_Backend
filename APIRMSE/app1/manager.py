from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, u_name, u_password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not u_name:
            raise ValueError('The given username must be set')
        u_name = self.normalize_email(u_name)
        user = self.model(u_name=u_name, **extra_fields)
        user.set_password(u_password)
        user.save(using=self._db)
        return user

    def create_user(self, u_name, u_password=None, **extra_fields):
        if not u_name:
            raise ValueError(('The Username must be set'))
        u_name = self.normalize_email(u_name)
        user = self.model(u_name=u_name, **extra_fields)
        user.set_password(u_password)
        user.save()
        return user

    # def create_superuser(self, u_name, u_password, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_active', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError(('Superuser must have is_staff=True.'))
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError(('Superuser must have is_superuser=True.'))
    #     return self.create_user(u_name, u_password, **extra_fields)
    

    