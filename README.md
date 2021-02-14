# Portfolio Dashboard - Back End
This repository is par of the Portfolio Dashboard application.
It represents the API of the application used as a back end.

## 1 How to use the application
### 1.1 Production
To run the back end part of the application you need to use the docker-compose file which organize the different containers.
You can find this file in another repository gathering the back end and the front end.

### 1.2 Development
#### 1.2.1 Prerequisites
##### 1.2.1.1 Python
This application uses Python 3, all the information needed to install it are there: https://wiki.python.org/moin/BeginnersGuide/Download.

##### 1.2.1.2 Virtual Environment
In order to run the application you need to set up a virtual environment, to do so run the following:
```shell
python -m venv .env
```

##### 1.2.1.3 Dependencies
To install the application dependencies run the following:
```shell
.env/bin/pip install -r requirements.txt
```

#### 1.2.2 Run the application
To run the application you need to run the following command:
```shell
.env/bin/uvicorn app.main:app --reload
```

Then the application is accessible at this address: http://127.0.0.1:80000
