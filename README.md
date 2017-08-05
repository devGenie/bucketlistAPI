[![Build Status](https://travis-ci.org/devGenie/bucketlistAPI.svg?branch=master)](https://travis-ci.org/devGenie/bucketlistAPI)

[![Code Health](https://landscape.io/github/devGenie/bucketlistAPI/master/landscape.svg?style=flat)](https://landscape.io/github/devGenie/bucketlistAPI/master)



## BUCKET LIST ## 
A bucketlist is a list of things you wish to do before you go ghost. This application a REATFUL webservice to help you keep track of ypur life goals. Have a blast and dont forget to make this world a better place, save the trees.

**Installation**
```
$ git clone https://github.com/devGenie/bucketlistAPI.git
$ cd bucketlistAPI
$ git pull master
```
**Install the virtual environment**
```
$ pip install virtualenv
$ pip install virtualenvwrapper
$ export WORKHOME=~/Envs
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv bucketlistAPI
$ workon bucketlist
```
**Install the requirements**

```	
$ pip install requirements.txt
```

OR

```
$ pip install --upgrade -r requirements.txt
```

Set the flask application environment variables

```
$ source .env
```

run the flask server

```
$ flask run
```