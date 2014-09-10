cd /etc/nginx/sites-enabled/
ln -is /var/www/oceanhunter/oceanhunter/deploy/oceanhunter.conf
sudo service nginx reload

cd /etc/uwsgi/vassals/
ln -is /var/www/oceanhunter/oceanhunter/deploy/oceanhunter.ini
sudo service uwsgi reload
