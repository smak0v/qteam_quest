from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Class that represents user manager"""

    use_in_migrations = True

    def create_user(self, username, first_name, last_name, email, location='', gender='NOT_SET', nationality='',
                    favourite_position='NOT_SET', password=None):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            location=location,
            gender=gender,
            nationality=nationality,
            favourite_position=favourite_position,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_staffuser(self, username, first_name, last_name, email, password, location='', gender='NOT_SET',
                         nationality='', favourite_position='NOT_SET'):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            location=location,
            gender=gender,
            nationality=nationality,
            favourite_position=favourite_position,
        )
        user.staff = True
        user.save(using=self.db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password, location='', gender='NOT_SET',
                         nationality='', favourite_position='NOT_SET'):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            location=location,
            gender=gender,
            nationality=nationality,
            favourite_position=favourite_position,
        )
        user.staff = True
        user.admin = True
        user.save(using=self.db)
        return user
