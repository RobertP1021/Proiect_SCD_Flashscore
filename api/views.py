from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Match, UserProfile

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