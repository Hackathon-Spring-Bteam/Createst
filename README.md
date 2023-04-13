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

## ブランチの命名規則 
  
developブランチから切り、「feature/#(イシュー番号)_わかりやすい名前」のブランチを作る。  
  
例：feature/#1_header  
  
※絶対日本語使わない  

## よく使うコマンド  
  
git branch ：今いるブランチを見る  
  
git switch ブランチ名 ：指定したブランチに飛ぶ  
  
git switch -c ブランチ名 ：今いるブランチから新しくブランチをきる  
  
git pull　：developブランチに移動し作業前に使用し最新の情報を取り込む  
  
git rebase　ブランチ名　：作業ブランチに移動し基本developを指定して取り込む 

これｒはテストです!