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
    print("❌ Aucun match trouvé dans matches.json")
    raise SystemExit(1)


print(f"✅ {len(matches)} matchs trouvés")
print()
print("===== PRÉDICTIONS =====")
print()


for match in matches:
    home = match.get("home_team", {}).get("team_name", "Équipe domicile")
    away = match.get("away_team", {}).get("team_name", "Équipe extérieur")
    date = match.get("match_date", "")

    # # Prédiction basée sur les probabilités
probabilities = match.get("probabilities", {})

home_prob = probabilities.get("home_win", 0)
draw_prob = probabilities.get("draw", 0)
away_prob = probabilities.get("away_win", 0)

if home_prob >= draw_prob and home_prob >= away_prob:
    prediction = "1"
    result = "Victoire domicile"
elif away_prob >= home_prob and away_prob >= draw_prob:
    prediction = "2"
    result = "Victoire extérieur"
else:
    prediction = "X"
    result = "Match nul"

    print(f"📅 {date}")
    print(f"⚽ {home} vs {away}")
    print(f"🔮 Prédiction : {prediction} — {result}")
    print("-" * 50)
