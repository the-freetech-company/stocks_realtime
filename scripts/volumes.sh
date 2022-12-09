MONGO_DIR_EXISTS=$(ls /opt/mongo | grep mongo)
PYPRICE_DIR_EXISTS=$(ls /opt/pyprice | grep pyprice)
PYOHLC_DIR_EXISTS=$(ls /opt/pyohlc | grep pyohlc)

MONGO_VOL_EXISTS=$(docker volume ls | grep mongo)
PYPARSERS_VOL_EXISTS=$(docker volume ls | grep pyprice)
PYOHLC_VOL_EXISTS=$(docker volume ls | grep pyohlc)



if [ -z "$MONGO_DIR_EXISTS" ]; then
    echo "creating /opt/mongo_data/mongo_data.."
    sudo mkdir -p /opt/mongo
fi

if [ -z "$PYPRICE_DIR_EXISTS" ]; then
    echo "creating /opt/pyprice_data/pyprice_data.."
    sudo mkdir -p /opt/pyprice
fi

if [ -z "$PYOHLC_DIR_EXISTS" ]; then
    echo "creating /opt/pyohlc_data/pyohlc_data.."
    sudo mkdir -p /opt/pyohlc
fi


if [ -z "$MONGO_VOL_EXISTS" ]; then
    docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/mongo/ \
    --opt o=bind mongo
fi

if [ -z "$PYPRICE_VOL_EXISTS" ]; then
docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/pyprice/ \
    --opt o=bind pyprice
fi

if [ -z "$PYOHLC_VOL_EXISTS" ]; then
docker volume create --driver local \
    --opt type=none \
    --opt device=/opt/pyohlc/ \
    --opt o=bind pyohlc
fi

sudo cp /home/mark/stocks_realtime/price.py /opt/pyprice/
sudo cp /home/mark/stocks_realtime/ohlc.py /opt/pyohlc/
sudo cp /home/mark/stocks_realtime/requirements.txt /opt/pyprice/
sudo cp /home/mark/stocks_realtime/requirements.txt /opt/pyohlc/