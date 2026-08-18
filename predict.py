import json
from pathlib import Path
from datetime import datetime, timezone

# ==========================================
# CONFIGURATION
# ==========================================

MATCHES_FILE = Path("matches.json")
OUTPUT_FILE = Path("predictions.json")


# ==========================================
# CHARGEMENT DES MATCHS
# ==========================================

if not MATCHES_FILE.exists():
    print("❌ matches.json introuvable")
    raise SystemExit(1)

with open(MATCHES_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


# Supporte :
# { "data": { "matches": [...] } }
# ou directement { "matches": [...] }

if isinstance(data.get("data"), dict):
    matches = data["data"].get("matches", [])
else:
    matches = data.get("matches", [])


if not matches:
    print("❌ Aucun match trouvé")
    raise SystemExit(1)


print(f"✅ {len(matches)} matchs trouvés")
print("")


# ==========================================
# ANALYSE DES MATCHS
# ==========================================

predictions = []

for match in matches:

    # --------------------------------------
    # ÉQUIPES
    # --------------------------------------

    home_team = (
        match.get("home_team", {})
        .get("team_name", "Équipe domicile")
    )

    away_team = (
        match.get("away_team", {})
        .get("team_name", "Équipe extérieure")
    )

    # --------------------------------------
    # INFORMATIONS DU MATCH
    # --------------------------------------

    match_date = match.get("match_date", "")

    league = (
        match.get("league_name")
        or match.get("competition")
        or match.get("league", "")
    )

    match_id = (
        match.get("fixture_id")
        or match.get("id")
        or match.get("fixture", {}).get("id")
    )

    # --------------------------------------
    # PROBABILITÉS
    # --------------------------------------

    probabilities = match.get("probabilities", {})

    home_prob = float(probabilities.get("home_win", 0))
    draw_prob = float(probabilities.get("draw", 0))
    away_prob = float(probabilities.get("away_win", 0))

    # --------------------------------------
    # PRONOSTIC PRINCIPAL
    # --------------------------------------

    if home_prob >= draw_prob and home_prob >= away_prob:
        prediction = "1"
        result = "Victoire domicile"
        predicted_team = home_team
        confidence = home_prob

    elif away_prob >= home_prob and away_prob >= draw_prob:
        prediction = "2"
        result = "Victoire extérieur"
        predicted_team = away_team
        confidence = away_prob

    else:
        prediction = "X"
        result = "Match nul"
        predicted_team = "Match nul"
        confidence = draw_prob

    # --------------------------------------
    # NIVEAU DE CONFIANCE
    # --------------------------------------

    if confidence >= 70:
        confidence_level = "Très élevée"
    elif confidence >= 60:
        confidence_level = "Élevée"
    elif confidence >= 50:
        confidence_level = "Moyenne"
    else:
        confidence_level = "Faible"

    # --------------------------------------
    # ANALYSE TEXTE
    # --------------------------------------

    analysis = (
        f"Le modèle donne {confidence:.1f}% de probabilité "
        f"pour {result.lower()}. "
        f"Le pronostic principal est donc {prediction}."
    )

    # --------------------------------------
    # OBJET FINAL POUR L'APPLICATION
    # --------------------------------------

    prediction_data = {
        "id": match_id,
        "home_team": home_team,
        "away_team": away_team,
        "date": match_date,
        "league": league,

        "prediction": {
            "code": prediction,
            "result": result,
            "team": predicted_team
        },

        "probabilities": {
            "home": round(home_prob, 2),
            "draw": round(draw_prob, 2),
            "away": round(away_prob, 2)
        },

        "confidence": {
            "value": round(confidence, 2),
            "level": confidence_level
        },

        "analysis": analysis
    }

    predictions.append(prediction_data)


# ==========================================
# CRÉATION DE predictions.json
# ==========================================

output = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "count": len(predictions),
    "matches": predictions
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)


# ==========================================
# AFFICHAGE CONSOLE
# ==========================================

print("===== PRÉDICTIONS =====")
print("")

for item in predictions:

    print(
        f"⚽ {item['home_team']} vs {item['away_team']}"
    )

    print(
        f"🔮 {item['prediction']['code']} - "
        f"{item['prediction']['result']}"
    )

    print(
        f"📊 1={item['probabilities']['home']}% | "
        f"X={item['probabilities']['draw']}% | "
        f"2={item['probabilities']['away']}%"
    )

    print(
        f"🎯 Confiance : "
        f"{item['confidence']['value']}% "
        f"({item['confidence']['level']})"
    )

    print("-" * 50)


print("")
print(f"✅ predictions.json créé avec {len(predictions)} matchs")
