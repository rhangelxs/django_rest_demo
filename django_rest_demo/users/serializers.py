from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
User = get_user_model()

class UsersDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'country')

        read_only_fields = ('email', )

    birth_date = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', 'iso-8601'])

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=250,
        #min_length=8,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    email = serializers.EmailField(required=True,
            validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    gender = serializers.CharField(write_only=True)

    # def validate_username(self, username):
    #     username = get_adapter().clean_username(username)
    #     return username
    #
    # def validate_email(self, email):
    #     email = get_adapter().clean_email(email)
    #     if allauth_settings.UNIQUE_EMAIL:
    #         if email and email_address_exists(email):
    #             raise serializers.ValidationError(
    #                 _("A user is already registered with this e-mail address."))
    #     return email
    #
    # def validate_password1(self, password):
    #     return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        # Remove allauth
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user
