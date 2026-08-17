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

    # Première version : avantage à l'équipe à domicile
    prediction = "1"
    result = "Victoire domicile"

    print(f"📅 {date}")
    print(f"⚽ {home} vs {away}")
    print(f"🔮 Prédiction : {prediction} — {result}")
    print("-" * 50)
