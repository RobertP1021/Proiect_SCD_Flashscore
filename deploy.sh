#!/bin/bash

echo "=========================================="
echo "🚀 Flashscore - Docker Swarm Deployment"
echo "=========================================="
echo ""

# Verifică dacă Docker Swarm e inițializat
if ! docker info | grep -q "Swarm: active"; then
    echo "⚠️  Docker Swarm nu e activ. Inițializez..."
    docker swarm init
    echo "✅ Docker Swarm inițializat!"
else
    echo "✅ Docker Swarm deja activ"
fi

echo ""
echo "🔨 Building imaginea user-service..."
docker build . -t flashscore-user-service

echo ""
echo "📦 Deploying stack-ul flashscore..."
docker stack deploy -c docker-compose.yml flashscore

echo ""
echo "⏳ Aștept serviciile să pornească..."
sleep 10

echo ""
echo "📊 Status servicii:"
docker service ls

echo ""
echo "⏳ Aștept ca user-service să fie gata (30 sec)..."
sleep 30

echo ""
echo "🗄️  Rulează migrations..."
CONTAINER_ID=$(docker ps --filter "name=flashscore_user-service" --format "{{.ID}}" | head -n 1)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ Nu am găsit containerul user-service! Așteaptă puțin și încearcă manual:"
    echo "   docker ps | grep user-service"
    echo "   docker exec -it <CONTAINER_ID> python manage.py migrate"
else
    echo "✅ Container găsit: $CONTAINER_ID"
    docker exec -it $CONTAINER_ID python manage.py migrate
fi

echo ""
echo "=========================================="
echo "✅ Deployment complet!"
echo "=========================================="
echo ""
echo "🌐 Servicii disponibile:"
echo "   - REST API:      http://localhost:8001/api/matches/"
echo "   - Django Admin:  http://localhost:8001/admin/"
echo "   - Keycloak:      http://localhost:8080/"
echo ""
echo "📋 Comenzi utile:"
echo "   docker service ls              # Vezi serviciile"
echo "   docker service logs flashscore_user-service  # Vezi log-uri"
echo "   docker stack rm flashscore     # Oprește totul"
echo ""
