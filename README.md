# snortubs
Chat id & Bot token pada code alertbot.sh diganti sesuai chat_id &bot_token yang dipakai atau didapat ketika membuat bot dan groupchat telegram


**Script Instalasi InfluxDB**
  -wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
  -echo "deb https://repos.influxdata.com/ubuntu $(lsb_release -cs) stable" |       sudo tee /etc/apt/sources.list.d/influxdb.list
  -sudo apt update
  -sudo apt install influxdb
  -sudo systemctl start influxdb
  -sudo systemctl enable influxdb

**Konfigurasi database InfluxDB**
  -Buat Database snort
  -Buat Measurement snort_alerts
  
**Command Untuk Membuat Database InfluxDB**
  -influx
  -create database snort (nama database bebas, bisa diganti)
  -use database snort
  -insert snort_alerts (nama measurements bebas, bisa diganti)

**Script Instalasi Grafana**
  -sudo apt update && sudo apt upgrade -y
  -sudo apt-get install -y software-properties-common
  -wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -         (Menambahkan kunci GPG untuk Grafana)
  -echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee         /etc/apt/sources.list.d/grafana.list (Menambahkan repository Grafana ke        sistem)
  -sudo apt update
  -sudo apt install -y grafana (Install Grafana)
  -sudo systemctl start grafana-server (Start Grafana server)
  -sudo systemctl stop grafana-server (Stop Grafana server)
  -sudo systemctl status grafana-server (Cek status Grafana server)
  -http://(IP VM):3000 (Akses Grafana di browser)

  **Import Dashboard Grafana**
    -Pilih menu dashboards di panel kiri
    -Klik button new, dan pilih option import dashboard (Add file JSON yang         ada di GitHub) / pilih add visualization jika ingin membuat dashboard           sendiri (Menentukan metrics-metrics dan datasource sendiri)
