# Unique key generation as REST API

Based on Django REST Framework, SQLite DB & PyTest

Service decsription can be found here (in Russian): [link](https://gist.github.com/softzilla/e989a97d811faf26e22e019967937f96).

## Up & run:
1. Install docker & docker compose
2. Clone repo into some dir: ```git clone https://github.com/PostMetalFun1992/KeyDeliver.git```
3. Inside repo dir: ```docker-compose build```
4. And then: ```docker-compose up```

## Useful scripts:
* ```./run_shell``` - runs django shell with ipython mode
* ```./run_tests``` - starts pytest session
* Request samples in ```./requests``` file - can run with emacs restclient.el
