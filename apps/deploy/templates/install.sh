cd /etc/nginx/conf.d/
ln -is {{settings.PROJ_ROOT}}/{{settings.PROJ_NAME}}.conf
sudo service nginx reload

cd /etc/uwsgi/vassals/
ln -is {{settings.PROJ_ROOT}}/{{settings.PROJ_NAME}}.ini
sudo service uwsgi reload
