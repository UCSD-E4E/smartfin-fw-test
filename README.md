# smartfin-fw-test
Smartfin FW Test Framework

# Dependencies
- pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib matplotlib jupyter RPi.GPIO numpy pandas pyserial ipython pyyaml
- apt-get install libatlas-base-dev

# Getting your Google credentials.json
1. In your web browser, navigate to https://console.cloud.google.com/
2. Select the E4E Smartfin Tester project
3. At the top-left, click Menu > APIs & Services > Credentials.
4. Click Create Credentials > OAuth client ID.
5. Click Application type > Desktop app.
6. In the "Name" field, type a name for the credential. This name is only shown in the Cloud Console.
7. Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
8. Download the created JSON file and place into this folder as `credentials.json`