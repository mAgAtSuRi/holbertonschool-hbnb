#!/bin/bash

# --- Variables utilisateurs (remplace si besoin) ---
JOHN_ID="79fdd0f8-e548-46e9-9d28-9cc60adeab45"
JOHN_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MTY1OTIyOCwianRpIjoiMzJhNjYzMDgtYzhiZC00OTcyLWIwMjQtMWRjMzdhY2ExZjJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijc5ZmRkMGY4LWU1NDgtNDZlOS05ZDI4LTljYzYwYWRlYWI0NSIsIm5iZiI6MTc2MTY1OTIyOCwiY3NyZiI6Ijk5YjhhZDQ0LTc1MTgtNDM2YS05NmRiLWFhOWRjYjIwNDU3MiIsImV4cCI6MTc2MTY2MDEyOCwiaXNfYWRtaW4iOmZhbHNlfQ.ZowIWCz7ek7SDJwpP0UgvUwSd7J7a8DFSGg_byfUW6w"

ALICE_ID="1b90a582-b226-44dc-9af0-6bec65be1787"
ALICE_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MTY1OTIzMywianRpIjoiMzc1ODZjNzQtZTAzOS00MGUyLWI1YTUtZDhkZWVlNzU5YmQ2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjFiOTBhNTgyLWIyMjYtNDRkYy05YWYwLTZiZWM2NWJlMTc4NyIsIm5iZiI6MTc2MTY1OTIzMywiY3NyZiI6ImIyODA0Nzk1LTg4M2UtNGEwOS04ODBmLTVhN2I2NzQ0YjIwNiIsImV4cCI6MTc2MTY2MDEzMywiaXNfYWRtaW4iOmZhbHNlfQ.jEgRu_1d2sDSN2AIen1RYYJSXSZlKyYqefIUFacrLtg"

API="http://127.0.0.1:5000/api/v1"

# --- Création d'une place avec John ---
echo "=== Création d'une place par John ==="
CREATE_PLACE_RESPONSE=$(curl -s -X POST "$API/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -d "{
    \"title\": \"Maison à Paris\",
    \"description\": \"Belle maison avec jardin\",
    \"price\": 120,
    \"latitude\": 48.8566,
    \"longitude\": 2.3522,
    \"owner_id\": \"$JOHN_ID\",
    \"amenities\": []
  }")
echo "$CREATE_PLACE_RESPONSE"

PLACE_ID=$(echo "$CREATE_PLACE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id'))")
echo "Place ID: $PLACE_ID"

# --- Tentative de création par Alice (doit échouer) ---
echo "=== Tentative de création par Alice (non-owner) ==="
curl -s -X POST "$API/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -d "{
    \"title\": \"Appartement à Lyon\",
    \"description\": \"Petit appartement cosy\",
    \"price\": 80,
    \"latitude\": 45.75,
    \"longitude\": 4.85,
    \"owner_id\": \"$JOHN_ID\",
    \"amenities\": []
  }" | jq || true
echo ""

# --- Mise à jour de la place par John ---
echo "=== Mise à jour de la place par John ==="
curl -s -X PUT "$API/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -d "{
    \"title\": \"Maison rénovée à Paris\",
    \"description\": \"Maison avec jardin et piscine\",
    \"price\": 150,
    \"latitude\": 48.8566,
    \"longitude\": 2.3522,
    \"owner_id\": \"$JOHN_ID\",
    \"amenities\": []
  }" | jq || true
echo ""

# --- Tentative de mise à jour par Alice ---
echo "=== Tentative de mise à jour par Alice (doit échouer) ==="
curl -s -X PUT "$API/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -d "{
    \"title\": \"Maison piratée\",
    \"description\": \"Alice essaie de hacker\",
    \"price\": 10,
    \"latitude\": 48.8566,
    \"longitude\": 2.3522,
    \"owner_id\": \"$JOHN_ID\",
    \"amenities\": []
  }" | jq || true
echo ""

# --- Lister toutes les places ---
echo "=== Liste de toutes les places ==="
curl -s -X GET "$API/places/" | jq || true
echo ""

# --- Récupérer la place par ID ---
echo "=== Récupérer la place par ID ==="
curl -s -X GET "$API/places/$PLACE_ID" | jq || true
echo ""

# --- Récupérer les reviews de la place ---
echo "=== Récupérer les reviews de la place ==="
curl -s -X GET "$API/places/$PLACE_ID/reviews" | jq || true
echo ""
