from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class CustomAuthToken(ObtainAuthToken):
    """
    Custom view for obtaining an authentication token with additional user information.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'role': user.role if hasattr(user, 'role') else 'user',
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """
    Logout view to delete the token and log out the user
    """
    try:
        # Get the token from the Authorization header
        token = request.auth
        if token:
            token.delete()
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'No token provided'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_profile(request):
    """
    Get user profile information
    """
    user = request.user
    return Response({
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
        'role': user.role if hasattr(user, 'role') else 'user',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'date_joined': user.date_joined,
    })
