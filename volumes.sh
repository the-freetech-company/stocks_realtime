MONGO_DIR_EXISTS=$(ls /opt/mongo_data | grep mongo_data)
PYPARSERS_DIR_EXISTS=$(ls /opt/mongo_data | grep pyparsers_data)

MONGO_VOL_EXISTS=$(docker volume ls | grep mongo_data)
PYPARSERS_VOL_EXISTS=$(docker volume ls | grep pyparsers_data)




if [ -z "$MONGO_DIR_EXISTS" ]; then
    echo "creating /opt/mongo_data/mongo_data.."
    sudo mkdir -p /opt/mongo_data
fi

if [ -z "$PYPARSERS_DIR_EXISTS" ]; then
    echo "creating /opt/mongo_data/pyparsers_data.."
    sudo mkdir -p /opt/pyparsers_data
fi


if [ -z "$MONGO_VOL_EXISTS" ]; then
    docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/mongo_data/ \
    --opt o=bind mongo_data

fi

if [ -z "$PYPARSERS_VOL_EXISTS" ]; then
docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/pyparsers_data/ \
    --opt o=bind pyparsers_data
fi

sudo cp main.py /opt/pyparsers_data/
sudo cp requirements.txt /opt/pyparsers_data/