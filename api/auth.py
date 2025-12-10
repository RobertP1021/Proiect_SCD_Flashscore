from functools import wraps
from rest_framework.response import Response
from keycloak import KeycloakOpenID
from django.conf import settings

# Inițializare Keycloak client (global)
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
)

def verify_token(token):
    """Verifică token cu Keycloak introspection"""
    try:
        # Introspection endpoint
        token_info = keycloak_openid.introspect(token)

        if not token_info.get('active'):
            raise Exception('Token is not active')

        return token_info
    except Exception as e:
        raise Exception(f'Token verification failed: {str(e)}')

def require_auth(view_func):
    """Decorator pentru autentificare obligatorie"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Extrage token din Authorization header
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return Response({'error': 'Missing or invalid Authorization header'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            # Verifică token
            user_info = verify_token(token)
            # Atașează la request pentru uz în view
            request.user_info = user_info
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': f'Unauthorized: {str(e)}'}, status=401)

    return wrapper

def require_role(role):
    """Decorator pentru verificare rol"""
    def decorator(view_func):
        @wraps(view_func)
        @require_auth  # Mai întâi verifică autentificarea
        def wrapper(request, *args, **kwargs):
            user_info = request.user_info

            # Extrage roluri din token
            realm_access = user_info.get('realm_access', {})
            roles = realm_access.get('roles', [])

            if role not in roles:
                return Response({
                    'error': f'Forbidden: User does not have required role "{role}"'
                }, status=403)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
