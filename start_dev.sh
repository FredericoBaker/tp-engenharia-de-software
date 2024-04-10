
cleanup() {
    echo "Encerrando..."
    kill $SERVER_PID
    exit 0
}

trap cleanup SIGINT

python manage.py runserver &
SERVER_PID=$!

while true; do
    python manage.py runcrons
    sleep 60 
done
