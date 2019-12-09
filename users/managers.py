from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Class that represents user manager"""

    use_in_migrations = True

    def create_user(self, phone, is_active_phone=False, username='', first_name='', last_name='', location='',
                    gender='NOT_SET', birthday_date=None, password=None, about=''):
        user = self.model(
            phone=phone,
            is_active_phone=is_active_phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
            location=location,
            gender=gender,
            birthday_date=birthday_date,
            about=about,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_staffuser(self, phone, is_active_phone=False, username='', first_name='', last_name='', password='',
                         location='', gender='NOT_SET', birthday_date=None, about=''):
        user = self.create_user(
            phone=phone,
            is_active_phone=is_active_phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            location=location,
            gender=gender,
            birthday_date=birthday_date,
            about=about,
        )
        user.staff = True
        user.save(using=self.db)
        return user

    def create_superuser(self, phone, is_active_phone=True, username='', first_name='', last_name='', password='',
                         location='', gender='NOT_SET', birthday_date=None, about=''):
        user = self.create_user(
            phone=phone,
            is_active_phone=is_active_phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            location=location,
            gender=gender,
            birthday_date=birthday_date,
            about=about,
        )
        user.staff = True
        user.admin = True
        user.save(using=self.db)
        return user
