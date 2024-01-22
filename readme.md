# Welcome to Paper Basket (Grocery Store App)
Paper Basket is a web app used for purchasing groceries, which has one 
admin, with multiple store managers and customers. Admin adds or removes categories, and checks new store manager sign-ups and requests from store manager regarding category modifications. Customers can purchase from the store. Store managers can add new products and make requests regarding categories.

### The application is divided into three sections.
* frontend-server
* backend-server
* dependencies

## Frontend server
### Prerequisites
- Node.js
### Installation
```shell
npm install
```
### Development Server
```shell
npm run serve
```
### Production Build
```shell
npm run build
```
### Production Server
```shell
serve -s dist
```
### Frontend structure
* src : Contains the source code of the application for running npm run serve
* public : Contains static assets.
* dist : Generated production ready files after running npm run build.

## Backend server
### Prerequisite
- Python
### Virtual Environment
Install virtualenv package (if not already installed)
```shell
pip install virtualenv
python -m virtualenv env
separate virtualenv for wsl
python -m virtualenv venv
```
### Activate the Envirnoment
````
env/scripts/activate
source venv/bin/activate
```
### Install Dependencies
####windows requirements.txt
####wsl requirement.txt


```
pip install -r requirements.txt
pip install -r requirement.txt
```

### Development server
```
python main.py 
```

```
### Celery Tasks
```shell
celery -A application.celery worker --loglevel=info
```
### Celery Scheduled Tasks
```shell
celery -A application.celery beat --loglevel=info
```
### Create databases
grocery.db database creates when server runs initially
### Deactivate the Environment
```shell
deactivate
```
### Backend structure
* application : Contains the configuration, blueprints registered, other modules for celery worker, database creation.
* database : Contains the database of the application
* user, category, product, review, cart, purchase : APIs for each features

## Dependencies
### Windows
flask mail

In WSL
* ```sudo apt install redis``` to install redis, for more details [visit Redis](https://redis.io/docs/install/install-redis/install-redis-on-windows/)

### Launch redis server
```bash
sudo service redis-server start
```
## Contact
For inquiries, reach out to [21f3003026@ds.study.iitm.ac.in](mailto:21f3003026@ds.study.iitm.ac.in)