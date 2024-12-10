# -*- coding: utf-8 -*-

import os

def create_nginx_conf():
    # Demander les informations nécessaires
    site_name = input("Entrez le nom de votre site (ex : monsite1.com) : ")
    upstream_ip = input("Entrez l'IP de votre serveur (ex : 192.168.56.102) : ")
    
    # Générer le contenu de la configuration Nginx
    nginx_conf_content = f'''
upstream monsite1 {{
    server {upstream_ip};
}}

server {{
    server_name {site_name};

    location / {{
        proxy_pass http://monsite1;
        proxy_set_header    Host $host;
        
        proxy_connect_timeout 30;
        proxy_send_timeout 30;
    }}
}}
    '''
    
    # Créer le fichier de configuration
    conf_filename = f"/etc/nginx/sites-available/{site_name}.conf"
    with open(conf_filename, "w") as conf_file:
        conf_file.write(nginx_conf_content)
    
    # Créer le lien symbolique
    os.system(f"ln -s {conf_filename} /etc/nginx/sites-enabled/{site_name}.conf")
    
    # Ajouter le SSL via Certbot
    os.system(f"certbot --nginx -d {site_name}")

    print(f"Configuration créée pour {site_name}. Le certificat SSL est en cours d'ajout.")
    print(f"Fichier de configuration : {conf_filename}")
    
if __name__ == "__main__":
    create_nginx_conf()
