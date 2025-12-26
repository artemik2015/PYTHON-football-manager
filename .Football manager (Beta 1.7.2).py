import os
import random
import time
import json
from datetime import datetime

# --- НАСТРОЙКИ ВИЗУАЛА (ANSI-ЦВЕТА) ---
COLORS = {
    "COMMON": "\033[90m",    # Серый
    "RARE": "\033[94m",      # Синий
    "EPIC": "\033[95m",      # Фиолетовый
    "LEGEND": "\033[93m",    # Золотой
    "RESET": "\033[0m"       # Сброс
}

RARITY_CONFIG = {
    "COMMON": {"min": 60, "max": 75},
    "RARE": {"min": 76, "max": 85},
    "EPIC": {"min": 86, "max": 94},
    "LEGEND": {"min": 95, "max": 110}
}

# Звезды футбола для паков
STAR_PLAYERS = [
    {"name": "Cristiano Ronaldo", "rating": 102, "rarity": "LEGEND"},
    {"name": "Lionel Messi", "rating": 105, "rarity": "LEGEND"},
    {"name": "Neymar Jr", "rating": 107, "rarity": "LEGEND"},
    {"name": "Kylian Mbappe", "rating": 101, "rarity": "LEGEND"},
    {"name": "Erling Haaland", "rating": 99, "rarity": "LEGEND"},
    {"name": "Kevin De Bruyne", "rating": 98, "rarity": "LEGEND"},
    {"name": "Vinicius Jr", "rating": 95, "rarity": "LEGEND"},
    {"name": "Mohamed Salah", "rating": 94, "rarity": "EPIC"},
    {"name": "Luka Modric", "rating": 92, "rarity": "EPIC"},
    {"name": "Harry Kane", "rating": 93, "rarity": "EPIC"},
    {"name": "Jude Bellingham", "rating": 91, "rarity": "EPIC"}
]

ENEMIES = ["Real Madrid", "FC Barcelona", "Manchester City", "Bayern Munich", "PSG", "Liverpool", "Arsenal", "Juventus", "Chelsea"]
SAVE_FILE = "save_data.json"

def clear():
    """Очистка консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_player():
    """Генерация обычного игрока по шансам редкости"""
    roll = random.randint(1, 100)
    if roll <= 5: r_type = "LEGEND"      # 5%
    elif roll <= 15: r_type = "EPIC"    # 10%
    elif roll <= 40: r_type = "RARE"    # 25%
    else: r_type = "COMMON"             # 60%
    
    config = RARITY_CONFIG[r_type]
    names = ["Silva", "Muller", "Kante", "Benzema", "Gavi", "Zidane", "Maradona", "Pele", "Yashin", "Arshavin", "Dzyuba", "Golovin"]
    return {
        "name": f"{random.choice(names)}",
        "rating": random.randint(config["min"], config["max"]),
        "rarity": r_type
    }

def save_game(data):
    """Сохранение всех профилей в JSON"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_game():
    """Загрузка базы данных"""
    if not os.path.exists(SAVE_FILE): return {}
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except: 
            return {}

def get_team_power(team):
    """Расчет силы топ-11 игроков"""
    if not team: return 0.0
    try:
        ratings = sorted([p['rating'] for p in team if 'rating' in p], reverse=True)
        top_11 = ratings[:11]
        if not top_11: return 0.0
        return sum(top_11) / len(top_11)
    except:
        return 0.0

def main():
    all_saves = load_game()
    clear()
    print(f"{COLORS['LEGEND']}⚽ FOOTBALL MANAGER ULTIMATE v1.7.2 (MAJOR UPDATE) ⚽{COLORS['RESET']}")
    print("-" * 45)
    
    if all_saves:
        print(f"Зарегистрировано тренеров: {', '.join(all_saves.keys())}")
    
    user = input("\nВведите логин: ").strip()
    pwd = input("Введите пароль: ").strip()

    is_admin = (user == "ArTEm1K_" and pwd == "aA201533R")

    if user in all_saves:
        data = all_saves[user]
        
        # --- ФИКС СОВМЕСТИМОСТИ (чтобы не вылетало) ---
        if "my_team" in data and "team" not in data:
            data["team"] = data.pop("my_team")
        if "team_name" in data and "club_name" not in data:
            data["club_name"] = data.pop("team_name")
        if "stadium_lvl" not in data:
            data["stadium_lvl"] = 1
        if "last_bonus" not in data:
            data["last_bonus"] = ""
        # Добавляем редкость старым игрокам, если её нет
        for p in data.get("team", []):
            if "rarity" not in p:
                p["rarity"] = "COMMON"
        # ----------------------------------------------

        if data.get("password") != pwd and not is_admin:
            print(f"\n{COLORS['EPIC']}❌ Ошибка: Неверный пароль!{COLORS['RESET']}")
            time.sleep(2)
            return
        print(f"\n[✔] С возвращением, тренер {user}!")
    else:
        print(f"\n[+] Создание нового клуба для {user}...")
        club_name = input("Назовите ваш клуб: ").strip()
        if not club_name: club_name = f"{user} FC"
        data = {
            "password": pwd,
            "money": 1000,
            "energy": 5,
            "stadium_lvl": 1,
            "last_bonus": "",
            "team": [generate_player() for _ in range(3)],
            "club_name": club_name
        }
        all_saves[user] = data
        save_game(all_saves)
    
    time.sleep(1)

    while True:
        clear()
        power = get_team_power(data.get('team', []))
        print(f"🏟️ Клуб: {data.get('club_name', 'No Name')} | Стадион: {data.get('stadium_lvl', 1)} ур.")
        print(f"💰 Деньги: {data.get('money', 0)}€ | ⚡ Энергия: {data.get('energy', 0)}/5")
        print(f"📊 Рейтинг ТОП-11: {power:.1f}")
        print("-" * 45)
        print("1. ⚔️  МАТЧ (Симуляция)")
        print("2. 🛒  ТРАНСФЕРЫ (Рынок)")
        print("3. 🎁  БОНУС (Ежедневный)")
        print("4. 🏟️  АПГРЕЙД (Стадион)")
        print("5. 📋  СОСТАВ / ИМЯ")
        print("6. 📦  ПАК (200€)")
        print("7. 💰  ПРОДАТЬ ИГРОКА")
        print("8. ⚡  ОТДЫХ (300€)")
        print("9. 💾  ВЫХОД")
        
        choice = input("\nВаш выбор: ")

        if choice == "1":
            if data["energy"] <= 0:
                print("\n❌ Мало энергии! Используйте отдых."); time.sleep(1.5); continue
            
            enemy = random.choice([e for e in ENEMIES if e.lower() != data['club_name'].lower()])
            e_rate = random.randint(int(power) - 5, int(power) + 10)
            data["energy"] -= 1
            
            print(f"\n🔥 ИГРАЕМ ПРОТИВ {enemy} ({e_rate})")
            score_me, score_en = 0, 0
            for minute in [20, 45, 70, 90]:
                time.sleep(0.6)
                chance = (power / (power + e_rate)) if (power + e_rate) > 0 else 0.5
                if random.random() < chance:
                    score_me += 1
                    print(f"⚽ {minute}' ГОООЛ! ({score_me}:{score_en})")
                elif random.random() > 0.8:
                    score_en += 1
                    print(f"🥅 {minute}' Пропустили... ({score_me}:{score_en})")

            print(f"\n🏁 ИТОГ: {score_me}:{score_en}")
            if score_me > score_en:
                win = (300 + random.randint(50, 150)) * data["stadium_lvl"]
                data["money"] += win
                print(f"🏆 ПОБЕДА! Доход: {win}€")
            elif score_me == score_en:
                data["money"] += 150
                print("🤝 НИЧЬЯ! +150€")
            else:
                print("❌ ПОРАЖЕНИЕ.")
            time.sleep(2)

        elif choice == "2":
            market = [generate_player() for _ in range(3)]
            while True:
                clear()
                print("🛒 ТРАНСФЕРНЫЙ РЫНОК")
                for i, p in enumerate(market):
                    price = p['rating'] * 15
                    color = COLORS.get(p.get('rarity', 'COMMON'), COLORS['COMMON'])
                    print(f"{i+1}. {color}{p['name']}{COLORS['RESET']} ({p['rating']}) - {price}€")
                
                buy = input("\nНомер для покупки (или '0' для выхода): ")
                if buy == '0': break
                try:
                    idx = int(buy) - 1
                    p = market[idx]
                    cost = p['rating'] * 15
                    if data["money"] >= cost:
                        data["money"] -= cost
                        data["team"].append(p)
                        market.pop(idx)
                        print("✅ Контракт подписан!")
                    else: print("❌ Нет денег!")
                except: pass
                time.sleep(1)

        elif choice == "3":
            today = datetime.now().strftime("%Y-%m-%d")
            if data.get("last_bonus") != today:
                data["money"] += 500
                data["last_bonus"] = today
                print("\n🎁 Получено 500€!")
            else:
                print("\n⏳ Приходите завтра!")
            time.sleep(1.5)

        elif choice == "4":
            cost = data["stadium_lvl"] * 1500
            print(f"\n🏟️ Улучшение стадиона до {data['stadium_lvl']+1} ур.")
            print(f"Цена: {cost}€. Это увеличит призовые за матчи.")
            if input("Улучшить? (y/n): ").lower() == 'y':
                if data["money"] >= cost:
                    data["money"] -= cost
                    data["stadium_lvl"] += 1
                    print("✅ Готово!")
                else: print("❌ Нет денег.")
            time.sleep(1)

        elif choice == "5":
            while True:
                clear()
                print(f"📋 СОСТАВ КЛУБА: {data['club_name']}")
                data["team"].sort(key=lambda x: x['rating'], reverse=True)
                for i, p in enumerate(data["team"]):
                    tag = "⭐" if i < 11 else "  "
                    color = COLORS.get(p.get('rarity', 'COMMON'), COLORS['COMMON'])
                    print(f"{tag} {color}{p['name']:<15}{COLORS['RESET']} | Рейтинг: {p['rating']} | {p.get('rarity', 'COMMON')}")
                
                print("\nКоманды: [rename] - сменить имя клуба, [back] - назад")
                cmd = input("Действие: ").lower().strip()
                if cmd == "rename":
                    new_name = input("Новое название: ").strip()
                    if new_name: data['club_name'] = new_name; print("Успешно!")
                elif cmd == "back": break
                time.sleep(1)

        elif choice == "6":
            if data["money"] >= 200:
                data["money"] -= 200
                if random.random() < 0.3:
                    player = random.choice(STAR_PLAYERS).copy()
                else:
                    player = generate_player()
                data["team"].append(player)
                color = COLORS.get(player.get('rarity', 'COMMON'), COLORS['COMMON'])
                print(f"\n📦 В ПАКЕ ВЫПАЛ: {color}{player['name']}{COLORS['RESET']} ({player['rating']})!")
                time.sleep(2)
            else:
                print("\n❌ Нужно 200€ для пака!"); time.sleep(1)

        elif choice == "7":
            if not data.get("team"): print("Некого продавать."); time.sleep(1); continue
            clear()
            print("💰 ПРОДАЖА ИГРОКОВ (Цена = Рейтинг * 5)")
            for i, p in enumerate(data["team"]):
                price = (p['rating'] * 5)
                print(f"{i+1}. {p['name']} ({p['rating']}) -> {price}€")
            
            idx_in = input("\nНомер игрока для продажи (0 - отмена): ")
            if idx_in != '0':
                try:
                    idx = int(idx_in) - 1
                    sold_p = data["team"].pop(idx)
                    gain = (sold_p['rating'] * 5)
                    data["money"] += gain
                    print(f"✅ {sold_p['name']} продан за {gain}€")
                except: print("Ошибка выбора.")
            time.sleep(1)

        elif choice == "8":
            if data["money"] >= 300:
                data["money"] -= 300
                data["energy"] = 5
                print("\n⚡ Энергия полностью восстановлена (5/5)!")
            else:
                print("\n❌ Недостаточно денег (нужно 300€)!")
            time.sleep(1.5)

        elif choice == "9":
            all_saves[user] = data
            save_game(all_saves)
            print("💾 Сохранено. До новых побед!"); break

if __name__ == "__main__":
    main()