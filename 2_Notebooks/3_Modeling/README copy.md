# Modern-Data-Analytics 📈
<img src ="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Police_of_Belgium_insignia.svg/1200px-Police_of_Belgium_insignia.svg.png" width="200" height="200" />

## To run the app

To be able to run the app you need have:
1. Dash installed on your machine
2. Amazon Web Services (AWS) account 
3. AWS access keys

Using `boto-3` you will connect to AWS S3 storage where the bucket you have created in the backend repository is stored. You can check that repository [here](https://github.com/AnastasiaDv491/Modern-Data-Analytics-Backend)

Your AWS access keys go into  a `.env` file. The correct format of this file can be found in the `example.env` file. To run the app, use `python app.py` in your terminal. 

## To run the server 🚀

This app was deployed on a server in the Oracle Cloud and this branch features the necessary files to do so. Before initiating this process: remove the certbot lines from the files `app.conf` file (indicating by #managed by Certbot at the first line of the lines to be removed). You can secure your webapp later in the same way. 

To get started:

1. To run the app on an Oracle Linux server you can use the [Oracle Cloud](https://www.oracle.com/cloud/) or the cloud of your choice. This app was deployed using the free tier on the Oracle Cloud, with 24GB RAM and 4 CPU cores on an ARM processor.
2. Save the SSH key pair on your local machine. We strongly recommed to link your servers IP adress to a domain name you own. 
3. We used WinSCP and Putty on our local machine for administrative access, but you can install other software of your choice. This manual will assume you install WinSCP and Putty in this step. Provide the IP adress/domain name and the SSH key pair to both programs to gain administrative access. 

The first part of the configuration is done via Putty:


4. Install on the server: Python3 and NginX. The command is `sudo yum install` on Oracle Linux, followed by what you want to install. Check that you land on the NginX landing page when you get to the IP adress of your server in your browser.
5. Install `python3-venv` via pip install. 
6. Create a folder for your project in the root directory labeled `/srv/mda` and start a virtual environment with `python3 -m venv myprojectenv`. Make sure that the users nginx, root and opc have access to this folder.
7. Activate the virtual environment with `source myprojectenv/bin/activate` and install all packages necessary for the app (see `requirements.txt`) via pip install. 

Then the next part is done via WinSCP:


8. Upload all the files with the extension `.py`, `.ini` and the folders assets and pages to the `srv/mda folder`.
9. Upload your file `.env` with your personal AWS keys to the `srv/mda` folder.
10. Upload the `app.service` file in the following location: `/etc/systemd/system/app.service`

Then we go back to Putty:

11. Start the app via Putty `systemctl start app` and enable the app to start at boot with `systemctl enable app`. You can check the status of the app via `systemctl status app`. If this works, your app is now running on your server, but not yet visible on the web. 

And again via WinSCP:

12. We still need to link the app with NginX. Open the `app.conf` file and change the server name to your domain name. 
13. Copy the `app.conf` file to `/etc/nginx/conf.d/app.conf`

Go back to Putty:

14. test for syntax errors with `nginx -t`
15. Restart NginX with `systemctl restart nginx`

16. Success! You can go to the webapp with your browser.

17. In order to be able to secure your webapp via Let`s encrypt, you need to link the IP-adress of your server to domain name you own as mentioned in the beginning. If you have done this, call on Certbot from Putty to secure your webpage.

Troubleshooting: most issues during deployment were related to users not having the right permissions. If anything appears to not be working, check that the users that need access to your app have this access. 

This setup guide is loosely based on [this site](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-22-04).
However, be aware that this online guide is written for Ubuntu and some of the steps do not apply for Oracle Linux servers. Look here instead for concrete instructions on how to work with Oracle Linux. 