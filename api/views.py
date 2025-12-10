from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Match, UserProfile
from .auth import keycloak_openid, require_role

@api_view(['GET'])
def get_matches(request):
    matches = Match.objects.all().values()
    return Response(list(matches))

@api_view(['GET'])
def get_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
        return Response({
            'id': match.id,
            'home_team': match.home_team,
            'away_team': match.away_team,
            'home_score': match.home_score,
            'away_score': match.away_score,
        })
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=404)

@api_view(['POST'])
def subscribe_match(request, match_id):
    email = request.data.get('email')
    username = request.data.get('username', email)

    try:
        match = Match.objects.get(id=match_id)
        user, created = UserProfile.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'keycloak_id': 'temp_' + email
            }
        )
        return Response({'message': 'Subscribed successfully'})
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=404)

@api_view(['POST'])
@require_role('administrator')
def create_match(request):
    home_team = request.data.get('home_team')
    away_team = request.data.get('away_team')
    match_date = request.data.get('match_date')
    home_score = request.data.get('home_score', 0)
    away_score = request.data.get('away_score', 0)

    # Validare câmpuri obligatorii
    if not home_team or not away_team or not match_date:
        return Response({
            'error': 'Missing required fields',
            'required_fields': ['home_team', 'away_team', 'match_date']
        }, status=400)

    try:
        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            match_date=match_date
        )
        return Response({
            'id': match.id,
            'home_team': match.home_team,
            'away_team': match.away_team,
            'home_score': match.home_score,
            'away_score': match.away_score,
            'match_date': match.match_date
        }, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['PUT'])
@require_role('administrator')
def update_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)

        # Actualizează scorurile dacă sunt furnizate
        if 'home_score' in request.data:
            match.home_score = request.data.get('home_score')
        if 'away_score' in request.data:
            match.away_score = request.data.get('away_score')

        # Permite actualizare și pentru alte câmpuri (opțional)
        if 'home_team' in request.data:
            match.home_team = request.data.get('home_team')
        if 'away_team' in request.data:
            match.away_team = request.data.get('away_team')
        if 'match_date' in request.data:
            match.match_date = request.data.get('match_date')

        match.save()

        return Response({
            'id': match.id,
            'home_team': match.home_team,
            'away_team': match.away_team,
            'home_score': match.home_score,
            'away_score': match.away_score,
            'match_date': match.match_date
        })
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=404)

@api_view(['DELETE'])
@require_role('administrator')
def delete_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
        match.delete()
        return Response({'message': 'Match deleted successfully'}, status=200)
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=404)

@api_view(['POST'])
def login(request):
    """
    POST /api/login/
    Body: {"username": "...", "password": "..."}
    Returns: {"access_token": "...", "refresh_token": "...", "expires_in": ...}
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'error': 'Missing required fields',
            'required_fields': ['username', 'password']
        }, status=400)

    try:
        # Obține token de la Keycloak
        token = keycloak_openid.token(username, password)

        return Response({
            'access_token': token.get('access_token'),
            'refresh_token': token.get('refresh_token'),
            'expires_in': token.get('expires_in')
        }, status=200)
    except Exception as e:
        return Response({'error': f'Login failed: {str(e)}'}, status=401)