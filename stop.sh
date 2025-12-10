#!/bin/bash

echo "🛑 Opresc stack-ul flashscore..."
docker stack rm flashscore

echo ""
echo "⏳ Aștept să se oprească serviciile..."
sleep 5

echo ""
echo "📊 Volumele rămân intacte:"
docker volume ls | grep flashscore

echo ""
echo "✅ Stack oprit! Datele sunt salvate în volume."
echo ""
echo "Pentru a reporni:"
echo "   ./deploy.sh"
