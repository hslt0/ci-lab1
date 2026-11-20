# Echo sounder API and client

## Вимоги

- Python 3.10 або новіша версія
- Windows/Linux/macOS
- Tkinter для графічного профілю дна

## Встановлення

```powershell
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

На macOS/Linux активуйте оточення через `source .venv/bin/activate`.

## Запуск сервера

У першому терміналі:

```powershell
.\\.venv\\Scripts\\python.exe -m uvicorn api:app --reload
```

API буде доступне за адресою `http://127.0.0.1:8000`.

- Конфігурація: `http://127.0.0.1:8000/api/config`
- Еталонний імпульс: `http://127.0.0.1:8000/api/pulse`
- Сигнал кроку: `http://127.0.0.1:8000/api/signal/{step}`
- Документація: `http://127.0.0.1:8000/docs`

## Запуск клієнта

У другому терміналі:

```powershell
.\\.venv\\Scripts\\python.exe client.py
```

Клієнт отримує конфігурацію та імпульс, обробляє весь маршрут, усереднює `3` запити для кожного кроку та відкриває графік профілю.

Для перевірки лише частини маршруту:

```powershell
.\\.venv\\Scripts\\python.exe client.py --max-steps 10 --repeats 3 --no-plot
```

Для запуску на іншому сервері:

```powershell
.\\.venv\\Scripts\\python.exe client.py --base-url http://127.0.0.1:8000
```
