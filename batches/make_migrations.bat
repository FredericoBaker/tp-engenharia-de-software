echo "Making magrations"
cd ..

python3 manage.py makemigrations
python3 manage.py migrate

echo "Finished! Making migrations complete."