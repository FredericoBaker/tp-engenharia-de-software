echo "Installing virtualenv"

cd ..

echo "Installing requirements"
pip install -r django
pip install -r django-livereload-server

echo "Creating database"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Finished! Installation complete."