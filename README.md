# Yoli Shell

When you cannot use SSH neither Zero Tier neither any other VPN without 2FA, Yoli cames to the rescue! Yoli Shell enables you to access your server directly from your browser, without any additional software.

![Yoli Shell](./ysh.jpg)

At last, one Yoli that really helps you!

## Usage

### Server

1.Install Yoli Shell on your server:

```bash
curl -s https://raw.githubusercontent.com/jlopezr/ysh/master/server.py | bash
```

2.Execute it

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
