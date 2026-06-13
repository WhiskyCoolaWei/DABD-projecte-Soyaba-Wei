# Com arrancar HealthLog

## Terminal 1 (Django)
```bash
cd ~/Public/healthlog-app && python3 manage.py runserver
```

## Terminal 2 (Frontend)
```bash
cd ~/Public/healthlog-app && python3 -m http.server 3000 --directory frontend/
```

## URL
http://localhost:3000/login.html

## Usuaris de prova
- Metge pur: `metge@healthlog.com` / `1234`
- Overlapping (metge+pacient): `overlapping@healthlog.com` / `1234`
- Pacient pur: `test@healthlog.com` / `1234`

Fer `localStorage.clear()` a la consola abans de canviar de compte.
