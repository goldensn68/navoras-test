# Navoras v0.1 (funktionel test)
Dette er en funktionel version med admin-login, brugeroprettelse og formularer.

## Standard login
- Admin: admin@navoras.dk / admin
(Men du skal oprette dem selv første gang)

## Kørsel
1. Udpak og push til GitHub
2. Deployer på Render
3. Initier database med:
```
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, role TEXT);
CREATE TABLE boats (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, length TEXT, motor TEXT);
CREATE TABLE logbooks (id INTEGER PRIMARY KEY, user_id INTEGER, entry TEXT);
CREATE TABLE maintenance (id INTEGER PRIMARY KEY, user_id INTEGER, task TEXT, status TEXT);
```
