# Createst

django/.env を作成し以下の内容を張り付け

MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=db
MYSQL_USER=db-user
MYSQL_PASSWORD=password



mysqlフォルダを作成しその中に.envファイルを作成し以下を記述

MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=db
MYSQL_USER=db-user
MYSQL_PASSWORD=password
TZ='Asia/Tokyo'

その後Dockerデスクトップを立ち上げた後以下のコマンド

docker compose up -d