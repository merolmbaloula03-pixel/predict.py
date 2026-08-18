import json
from pathlib import Path

# Charger les matchs
matches_file = Path("matches.json")

if not matches_file.exists():
    print("❌ matches.json introuvable")
    raise SystemExit(1)

with open(matches_file, "r", encoding="utf-8") as f:
    data = json.load(f)

matches = data.get("data", {}).get("matches", [])

if not matches:
    print("❌ Aucun match trouvé")
    raise SystemExit(1)

print(f"✅ {len(matches)} matchs trouvés")
print()
print("===== PRÉDICTIONS =====")
print()

predictions = []

for match in matches:
    home = match.get("home_team", {}).get(
        "team_name", "Équipe domicile"
    )
    away = match.get("away_team", {}).get(
        "team_name", "Équipe extérieure"
    )
    date = match.get("match_date", "")

    probabilities = match.get("probabilities", {})

    home_prob = probabilities.get("home_win", 0)
    draw_prob = probabilities.get("draw", 0)
    away_prob = probabilities.get("away_win", 0)

    if home_prob >= draw_prob and home_prob >= away_prob:
        prediction = "1"
        result = "Victoire domicile"
    elif away_prob >= home_prob and away_prob >= draw_prob:
        prediction = "2"
        result = "Victoire extérieure"
    else:
        prediction = "X"
        result = "Match nul"

    confidence = max(home_prob, draw_prob, away_prob)

    prediction_data = {
        "date": date,
        "home_team": home,
        "away_team": away,
        "prediction": prediction,
        "result": result,
        "probabilities": {
            "1": home_prob,
            "X": draw_prob,
            "2": away_prob
        },
        "confidence": confidence
    }

    predictions.append(prediction_data)

    print(f"⚽ {home} vs {away}")
    print(f"🔮 {prediction} — {result}")
    print(
        f"📊 1={home_prob}% | X={draw_prob}% | 2={away_prob}%"
    )
    print(f"🎯 Confiance : {confidence}%")
    print("-" * 50)

# Créer le fichier pour l'application
output_file = Path("predictions.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        {
            "success": True,
            "count": len(predictions),
            "predictions": predictions
        },
        f,
        ensure_ascii=False,
        indent=2
    )

print()
print(f"✅ {len(predictions)} prédictions enregistrées dans predictions.json")
