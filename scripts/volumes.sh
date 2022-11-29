MONGO_DIR_EXISTS=$(ls /opt/mongo_data | grep mongo_data)
PYPRICE_DIR_EXISTS=$(ls /opt/pyprice_data | grep pyprice_data)
PYOHLC_DIR_EXISTS=$(ls /opt/pyohlc_data | grep pyohlc_data)

MONGO_VOL_EXISTS=$(docker volume ls | grep mongo_data)
PYPARSERS_VOL_EXISTS=$(docker volume ls | grep pyprice_data)
PYOHLC_VOL_EXISTS=$(docker volume ls | grep pyohlc_data)



if [ -z "$MONGO_DIR_EXISTS" ]; then
    echo "creating /opt/mongo_data/mongo_data.."
    sudo mkdir -p /opt/mongo_data
fi

if [ -z "$PYPRICE_DIR_EXISTS" ]; then
    echo "creating /opt/pyprice_data/pyprice_data.."
    sudo mkdir -p /opt/pyprice_data
fi

if [ -z "$PYOHLC_DIR_EXISTS" ]; then
    echo "creating /opt/pyohlc_data/pyohlc_data.."
    sudo mkdir -p /opt/pyohlc_data
fi


if [ -z "$MONGO_VOL_EXISTS" ]; then
    docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/mongo_data/ \
    --opt o=bind mongo_data
fi

if [ -z "$PYPRICE_VOL_EXISTS" ]; then
docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/pyprice_data/ \
    --opt o=bind pyprice_data
fi

if [ -z "$PYOHLC_VOL_EXISTS" ]; then
docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/pyohlc_data/ \
    --opt o=bind pyohlc_data
fi

sudo cp /home/mark/stocks_realtime/price.py /opt/pyprice_data/
sudo cp /home/mark/stocks_realtime/ohlc.py /opt/pyohlc_data/
sudo cp /home/mark/stocks_realtime/requirements.txt /opt/pyprice_data/
sudo cp /home/mark/stocks_realtime/requirements.txt /opt/pyohlc_data/