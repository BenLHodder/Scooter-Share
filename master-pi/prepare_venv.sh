python3 -m venv venv
source venv/bin/activate

cd database_handler
pip install pipreqs
pipreqs --force
sed -i 's/psycopg2==.*/psycopg2-binary==2.9.9/' requirements.txt
make

cd ../backend
pip install pipreqs
pipreqs --force
make

cd ../frontend
pip install pipreqs
pipreqs --force
make