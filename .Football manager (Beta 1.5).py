import os
import random
import time
import json

# Константы для паков
ALL_PLAYERS = [
    {"name": "Cristiano Ronaldo", "rating": 102},
    {"name": "Lionel Messi", "rating": 105},
    {"name": "Neymar Jr", "rating": 107},
    {"name": "Kylian Mbappe", "rating": 101},
    {"name": "Erling Haaland", "rating": 99},
    {"name": "Kevin De Bruyne", "rating": 98},
    {"name": "Vinicius Jr", "rating": 95},
    {"name": "Mohamed Salah", "rating": 94},
    {"name": "Luka Modric", "rating": 92},
    {"name": "Harry Kane", "rating": 93},
    {"name": "Jude Bellingham", "rating": 91},
    {"name": "Pedri", "rating": 89},
    {"name": "Rodri", "rating": 96}
]

# Список всех клубов-соперников
ENEMIES = ["Real Madrid", "FC Barcelona", "Manchester City", "Bayern Munich", "PSG", "Man City", "Liverpool", "Juventus", "Arsenal", "Chelsea"]
SAVE_FILE = "save_data.json"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_game(data):
    """Сохраняет данные всех игроков в один JSON файл"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_game():
    """Загружает общую базу данных из JSON файла"""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def get_team_power(team):
    if not team: return 0
    ratings = sorted([p['rating'] for p in team], reverse=True)
    top_11 = ratings[:11]
    return sum(top_11) / len(top_11)

def main():
    clear()
    abs_path = os.path.abspath(SAVE_FILE)
    
    print("="*40)
    print(" ArTEm1K_ PYTHONS: FOOTBALL MANAGER (PYTHON) ")
    print("="*40)
    print(f"Путь к общей базе: {abs_path}")
    print("-" * 40)
    
    # Загружаем все существующие аккаунты
    all_saves = load_game()
    
    if all_saves:
        print(f"Зарегистрировано тренеров: {', '.join(all_saves.keys())}")
    
    # --- СИСТЕМА ЛОГИНА ---
    print("\n[ВХОД В СИСТЕМУ]")
    username = input("Введите никнейм: ").strip()
    password = input("Введите пароль: ").strip()

    is_admin = False
    if username == "ArTEm1K_" and password == "aA201533R":
        print(f"\n[OK] Режим администратора активирован!")
        is_admin = True
    else:
        if not username:
            username = f"Guest_{random.randint(100, 999)}"
        print(f"\n[!] Текущий пользователь: {username}")

    if username in all_saves:
        game_data = all_saves[username]
        # Проверка пароля (админ может войти в любой аккаунт)
        if game_data.get("password") != password and not is_admin:
            print("[!] ОШИБКА: Неверный пароль!")
            time.sleep(2)
            return
        print(">>> Профиль загружен успешно!")
    else:
        clear()
        print(f"--- СОЗДАНИЕ НОВОГО АККАУНТА ---")
        print(f"Никнейм '{username}' будет добавлен в общую базу.")
        print(f"Ваш пароль будет сохранен для этого ника.")
        
        custom_team_name = input("\nНазовите ваш клуб: ").strip()
        if not custom_team_name:
            custom_team_name = f"{username} FC"
            
        game_data = {
            "password": password,
            "money": 1000,
            "my_team": [],
            "energy": 5,
            "team_name": custom_team_name
        }
        # Добавляем новый аккаунт к уже существующим в словаре
        all_saves[username] = game_data
        save_game(all_saves)
        print(f"\n>>> Аккаунт создан! Теперь в базе {len(all_saves)} тренера(ов).")
    
    time.sleep(1.5)

    while True:
        clear()
        power = get_team_power(game_data["my_team"])
        print(f"ТРЕНЕР: {username} | КЛУБ: {game_data['team_name']}")
        print(f"ДЕНЬГИ: {game_data['money']}€ | ЭНЕРГИЯ: {game_data['energy']}/5")
        print(f"РЕЙТИНГ ТОП-11: {power:.1f}")
        print("-" * 40)
        print("1. [pack]  - Купить пак (200€)")
        print("2. [match] - Играть матч (-1⚡)")
        print("3. [team]  - Управление составом и название")
        print("4. [sell]  - Продать игрока")
        print("5. [rest]  - Отдохнуть (300€)")
        print("6. [save]  - Сохранить прогресс")
        print("7. [exit]  - Выйти из игры")
        print("-" * 40)
        
        choice = input("Выбор: ").lower().strip()

        if choice == "pack" or choice == "1":
            if game_data["money"] >= 200:
                game_data["money"] -= 200
                player = random.choice(ALL_PLAYERS).copy()
                game_data["my_team"].append(player)
                print(f"\n[🌟] ПАК: {player['name']} ({player['rating']})!")
                time.sleep(2)
            else:
                print("\n[!] Не хватает денег.")
                time.sleep(1)

        elif choice == "match" or choice == "2":
            if game_data["energy"] > 0:
                game_data["energy"] -= 1
                
                my_name_lower = game_data['team_name'].lower()
                available_enemies = [e for e in ENEMIES if e.lower() != my_name_lower]
                
                if not available_enemies:
                    available_enemies = ["All Stars FC"]

                enemy = random.choice(available_enemies)
                enemy_pwr = random.randint(85, 105)
                
                print(f"\nМАТЧ: {game_data['team_name']} vs {enemy}")
                print(f"Сила противника: {enemy_pwr}")
                
                win_chance = 0.5 + (power - enemy_pwr) / 100
                score_me, score_en = 0, 0
                
                for _ in range(3):
                    time.sleep(0.7)
                    roll = random.random()
                    if roll < win_chance:
                        score_me += 1
                        print("ГОЛ забиваем МЫ!")
                    elif roll > 0.8:
                        score_en += 1
                        print("ГОЛ забивают НАМ...")
                
                print(f"\nИТОГОВЫЙ СЧЕТ: {score_me} - {score_en}")
                if score_me > score_en:
                    game_data["money"] += 500
                    print("ПОБЕДА! +500€")
                elif score_me < score_en:
                    print("ПОРАЖЕНИЕ.")
                else:
                    game_data["money"] += 150
                    print("НИЧЬЯ. +150€")
                time.sleep(2.5)
            else:
                print("\n[!] Энергия на нуле.")
                time.sleep(1)

        elif choice == "team" or choice == "3":
            while True:
                clear()
                print(f"--- УПРАВЛЕНИЕ КОМАНДОЙ: {game_data['team_name']} ---")
                print(f"Средний рейтинг (Топ-11): {power:.1f}")
                print("-" * 30)
                
                if not game_data["my_team"]:
                    print("Состав пуст.")
                else:
                    sorted_team = sorted(game_data["my_team"], key=lambda x: x['rating'], reverse=True)
                    for i, p in enumerate(sorted_team):
                        tag = "⭐ ОСНОВА" if i < 11 else "  ЗАПАС "
                        print(f"{i+1:2}. {tag} | {p['name']:<18} | Рейтинг: {p['rating']}")
                
                print("-" * 30)
                print("Команды: [rename] - сменить имя, [back] - назад")
                
                sub_choice = input("\nДействие: ").lower().strip()
                if sub_choice == "rename":
                    new_name = input("Новое название: ").strip()
                    if new_name:
                        game_data['team_name'] = new_name
                        print("Готово!")
                        time.sleep(1)
                elif sub_choice == "back":
                    break

        elif choice == "sell" or choice == "4":
            if not game_data["my_team"]:
                print("\nНекого продавать.")
                time.sleep(1)
                continue
            
            clear()
            print("--- ПРОДАЖА ИГРОКОВ ---")
            for i, p in enumerate(game_data["my_team"]):
                print(f"{i}. {p['name']} ({p['rating']}) -> {p['rating'] // 2}€")
            
            try:
                ans = input("\nНомер (или 'back'): ")
                if ans.lower() != 'back':
                    idx = int(ans)
                    player = game_data["my_team"].pop(idx)
                    reward = player['rating'] // 2
                    game_data["money"] += reward
                    print(f"Продано за {reward}€!")
            except:
                print("Ошибка.")
            time.sleep(1)

        elif choice == "rest" or choice == "5":
            if game_data["money"] >= 300:
                game_data["money"] -= 300
                game_data["energy"] = 5
                print("\nЭнергия восстановлена!")
            else:
                print("\nНедостаточно монет!")
            time.sleep(1)

        elif choice == "save" or choice == "6":
            all_saves[username] = game_data
            save_game(all_saves)
            print("\nПрогресс всех аккаунтов сохранен!")
            time.sleep(1)

        elif choice == "exit" or choice == "7":
            all_saves[username] = game_data
            save_game(all_saves)
            print("\nВыход...")
            break

if __name__ == "__main__":
    main()