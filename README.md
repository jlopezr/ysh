# Yoli Shell

When you cannot use SSH neither Zero Tier neither any other VPN without 2FA, Yoli cames to the rescue! Yoli Shell enables you to access your server directly from your browser, without any additional software.

![Yoli Shell](./ysh.jpg)

At last, one Yoli that really helps you!

## Usage

### Server

1.Install Yoli Shell on your server:

```bash
curl -s https://raw.githubusercontent.com/jlopezr/ysh/master/server.py > server.py
```

2.Execute it, you only need Python 3:

```bash
python3 server.py
```

3.Optionally, you can add a password to the server:

```bash
python3 server.py --key mypassword
```

or

```bash
set YSH_KEY=mypassword
python3 server.py
```

### Client

1.Install Yoli Shell on your client:

```bash
curl -s https://raw.githubusercontent.com/jlopezr/ysh/master/yoli.py > yoli.py
```

2.Set the server URL and optionally the password:

```bash
set YSH_SERVER=http://myserver.com:8000
set YSH_KEY=mypassword
```

3.Execute it:

```bash
yoli.py ls -lF
```

or

```bash
yoli.py "cd / && ls -lF"
```

## Best practices

### Supervisor

You can use a process manager like supervisor or systemd to ensure that your server restarts if it crashes or if the console is closed. Here is an example using supervisor.

```bash
pip3 install supervisor
```

Then create a configuration file for supervisor:

```bash
[program:ysh_server]
command=python3 /Users/juan/ysh/server.py
autostart=true
autorestart=true
stderr_logfile=/var/log/ysh_server.err.log
stdout_logfile=/var/log/ysh_server.out.log
```

Then run supervisor with the configuration file:

```bash
supervisord -c /Users/juan/ysh/supervisord.conf
```

