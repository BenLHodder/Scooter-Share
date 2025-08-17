cd console
pip install pipreqs
pipreqs --force
make

cd ..
python3 -m venv venv
source venv/bin/activate

cd frontend
pip install pipreqs
pipreqs --force
echo "pillow" >> requirements.txt
make