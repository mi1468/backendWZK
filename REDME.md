python3 manage.py runserver 0.0.0.0:8000

pm2 start "python3 manage.py runserver 0.0.0.0:8000 " --name "serverDjango"

pm2 start "npm run dev -- --host 0.0.0.0 " --name "vue"

npm run dev -- --host 0.0.0.0
