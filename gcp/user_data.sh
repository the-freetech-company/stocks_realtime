project_exists=$(ls | grep stocks_realtime)
if [ -z "$project_exists" ]; then
  git clone https://github.com/adamsiwiec1/stocks_realtime.git
  cd stocks_realtime
  chmod +x startup.sh
  chmod +x scripts/*
  bash startup.sh
else
  cd stocks_realtime
  git pull
  chmod +x startup.sh
  chmod +x scripts/*
  echo "y" | bash startup.sh
fi