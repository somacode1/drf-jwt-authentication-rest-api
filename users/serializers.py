from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of user objects"""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, read_only=True)
    is_verified = serializers.CharField(max_length=255, read_only=True)
    display_name = serializers.CharField(max_length=255, read_only=True)
    # avatar = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=20, read_only=True)
    bio = serializers.CharField(read_only=True)
    phone = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
             
                'id': user.id,
                'username': user.email,
                'is_verified': user.is_verified,
                'display_name': user.display_name,
                # 'avatar': user.avatar, 
                'role': user.role,
                'bio': user.bio,
                'phone': user.phone,
                'email': user.email,
                'token': user.token
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    id = serializers.CharField(max_length=255, read_only=True)
    is_verified = serializers.CharField(max_length=255, read_only=True)
    display_name = serializers.CharField(max_length=255, read_only=True)
    # avatar = serializers.CharField(max_length=255, read_only=True)
    bio = serializers.CharField(read_only=True)
    phone = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=20, write_only=True)
    email = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id','is_verified','display_name','role','bio','phone','username','email', 'password','token']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True}
            # 'token': {'read_only': True},
        }
        

    def create(self, validated_data):
        try:
            # Use the `create_user` method to create a new user.
            user = User.objects.create_user(**validated_data)
            return user
        except Exception as e:
            # Handle the exception
            print(e)
            raise serializers.ValidationError("An error occurred during user creation")

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")