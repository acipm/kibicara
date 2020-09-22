## Setup on a server

This will guide you through the whole kibicara server setup on a OpenBSD with OpenSMTPd as MTA (+ Relay at `relay.example.com`) and `https://kibicara.example.com` as domain. The kibicara server will also run on other Unix-like systems, just modify the guide to your needs.

Prerequisites:
- python>=3.8 + pip

### Set up server environment
- Create a new user: `adduser kibicara`
- Install packages: `pkg_add git python%3.8 opensmtpd-extras`
  - (Optional) Create a symlink to python3: `ln -s /usr/local/bin/python3.8 /usr/local/bin/python3`
- Ensure pip is installed: `python3 -m ensurepip --default-pip`
- Switch to kibicara user: `su -l kibicara`
- Add pip packages to PATH by appending it to the `.profile` of user `kibicara` (remember that a new login is needed for it to work). This ensures that you can call kibicara without full path:
```
PIP_PACKAGES="${HOME}/.local"
export PATH="$PATH:$PIP_PACKAGES/bin"
```

### Build backend on the server
- Clone the repository: `git clone https://github.com/acipm/kibicara`
- Install backend: `cd kibicara && pip install -U --user pip setuptools wheel && pip install --user .`

### Build frontend on your local machine
Since Angular CLI is quite bloaty and your server may don't have enough resouces, we recommend to build the frontend locally and copying it onto the server. The same steps can be used on the server if it has enough resources.

- Install npm: `pkg_add node`
- Configure npm to use global install (`-g`) without root
```
mkdir "${HOME}/.npm-packages"
npm config set prefix "${HOME}/.npm-packages"
```
- Add npm package path to PATH in `.profile` by appending:
```
NPM_PACKAGES="${HOME}/.npm-packages"
export PATH="$PATH:$NPM_PACKAGES/bin"
```
- Install Angular CLI: `npm install -g @angular/cli`
- Clone repository locally: `git clone https://github.com/acipm/kibicara`
- Change production settings in `kibicara/kibicara-frontend/src/environments/environment.prod.ts` to use your domain:
```
export const environment = {
  production: true,
  API_BASE_PATH: 'https://kibicara.example.com',
  EMAIL_DOMAIN: 'kibicara.example.com',
};
```
- Build frontend with `cd kibicara/kibicara-frontend && ng build --prod`
- Copy the generated frontend to your server to `/home/kibicara/kibicara-frontend`: `scp -r kibicara/kibicara-frontend/dist/kibicara-frontend <your_server>:/home/kibicara`

### Configure Kibicara Core
- Write config file to `/etc/kibicara.conf` and replace the domain with yours:
```
database_connection = 'sqlite:////home/kibicara/kibicara.sqlite'
frontend_path = '/home/kibicara/kibicara-frontend'
frontend_url = 'https://kibicara.example.com'
```

#### SSL
You can use the SSL stuff provided by hypercorn by generating an SSL Certificate and passing its paths to the config options `certfile` and `keyfile` in `/etc/kibicara.conf`.

### Configure Kibicara platforms

#### Configure E-Mail (OpenSMTPd + Relay)
To send and receive e-mails (necessary for registration confirmation and e-mail bot) you will need an MTA. We use OpenSMTPd:

- Configure OpenSMTPd by writing the `/etc/mail/smtpd.conf`. Basically all lines with `kibicara` in it are relavant, if you already have a different setup just copy those.
```
table aliases file:/etc/mail/aliases
table kibicara_mailaddr sqlite:/etc/mail/kibicara_mailaddr.conf

listen on all

action "local_mail" mbox alias <aliases>
action "outbound" relay host "relay.example.com"
action "kibicara" mda "/home/kibicara/.local/bin/kibicara_mda %{dest.user}" virtual { "@" => kibicara } user kibicara

match from any for domain "kibicara.example.com" rcpt-to <kibicara_mailaddr> action "kibicara"
match from any for domain "kibicara.example.com" action "local_mail"
match from local for local action "local_mail"
match from local for any action "outbound"
```
- Read accepted inbox addresses from the database by configuring `/etc/mail/kibicara_mailaddr.conf`:
```
dbpath /home/kibicara/kibicara.sqlite
query_mailaddr SELECT 1 FROM email WHERE ? IN (name || '@kibicara.example.com');
```
- Don't forget to restart OpenSMTPd when you change your database: `rcctl stop && rcctl start`

#### Configure Twitter

Twitter needs you to create a Twitter App, which hood admins can permit to read and write messages.

- Create Twitter account and app: https://developer.twitter.com
- Get your customer key and customer secret and append this to `/etc/kibicara.conf`:
```
[twitter]
consumer_key = '<your_consumer_key>'
consumer_secret = '<your_consumer_secret>'
```
- You need to configure a Callback Url in your Twitter App:
  - Go to: `https://developer.twitter.com/en/apps`
  - Add `https://kibicara.example.com/dashboard/twitter-callback` as Callback Url of your Twitter App. This is needed to successfully create a twitter oauth handshake.

#### Configure Telegram
Nothing to do, because telegram has a nice API.

### Start Kibicara
Run `kibicara` with your kibicara user. To have more verbose output add `-vvv`.
