 
MONGO_EXISTS=$(docker volume ls | grep mongo_data)
PYPARSERS_EXISTS=$(docker volume ls | grep pyparsers_data)

if [ -z "$MONGO_EXISTS" ]; then
    docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/mongo_data/ \
    --opt o=bind mongo_data

fi

if [ -z "$PYPARSERS_EXISTS" ]; then
docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/pyparsers_data/ \
    --opt o=bind pyparsers_data
fi

sudo cp main.py /opt/pyparsers_data/
sudo cp requirements.txt /opt/pyparsers_data/