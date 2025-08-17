python -m venv venv
source venv/bin/activate

# Install Dependencies

cd master-pi/backend
pip install pipreqs
pipreqs --force
make

cd ../database_handler
pip install pipreqs
pipreqs --force
sed -i 's/psycopg2==.*/psycopg2-binary==2.9.9/' requirements.txt
make

cd ../frontend
pip install pipreqs
pipreqs --force
make

cd ../../agent-pi/frontend
pip install pipreqs
pipreqs --force
make

cd ../console
pip install pipreqs
pipreqs --force
make
cd ../../

# Run Unit Tests
cd master-pi/backend
python -m unittest discover

cd ../database_handler
python -m unittest discover

cd ../frontend
python -m unittest discover

cd ../../agent-pi/frontend
python -m unittest discover

cd ../console
python -m unittest discover

cd ../../
rm -r venv/