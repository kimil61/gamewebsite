# EC2 서버 설정

sudo apt-get update
sudo apt-get install python3-pip nginx
pip3 install -r requirements.txt

# Nginx 설정

sudo nano /etc/nginx/sites-available/myapp

server {
listen 80;
server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

}

# 심볼릭 링크 생성

sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
