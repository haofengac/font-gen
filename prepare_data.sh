mkdir data
cd data
wget https://github.com/google/fonts/archive/master.zip
unzip master.zip && rm master.zip
cd ..
python tools/prepare_data.py
rm -rf data/fonts-master
