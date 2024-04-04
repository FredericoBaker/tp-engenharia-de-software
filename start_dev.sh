# Inicia runserver_plus em background
python manage.py runserver_plus &

# Loop para executar runcrons a cada minuto
while true; do
    python manage.py runcrons
    sleep 60
done
