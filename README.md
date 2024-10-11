# NuriPlanner


# 데이터
- [누리놀이 교육계획안](https://www.nurinori.com/index.do)


# API 명세
## Plan API
|API명|요청방법|URL|설명|
|:---:|:---:|:---|:---|
|목록조회|get|/api/plan/list|전체 계획안을 조회한다|
|상세조회|get|/api/plan/detail/{plan_id}|계획안(plan_id)에 대한 상세 내역을 조회한다|
|계획안등록|post|/api/plan/create|새로운 계획안을 등록한다|
|계획안수정|put|/api/plan/update|계획안을 수정한다|
|계획안삭제|delete|/api/plan/delete|계획안을 삭제한다|
## RecPlan API
|API명|요청방법|URL|설명|
|:---:|:---:|:---|:---|
|추천목록조회|get|/api/recplan/{plan_id}/list|계획안(plan_id)에 대한 추전 목록을 조회한다|
|계획안등록|post|/api/recplan/create|새로운 계획안을 등록한다|
|계획안수정|put|/api/recplan/update|계획안을 수정한다|
|계획안삭제|delete|/api/recplan/delete|계획안을 삭제한다|
## User API
|API명|요청방법|URL|설명|
|:---:|:---:|:---|:---|
|회원가입|post|/api/user/create|새로운 회원을 등록한다|
|로그인|post|/api/user/login|로그인을 실행한다|

# 설치
``` bash
git clone https://github.com/angiekim05/NuriPlanner.git
cd NuriPlanner
git clone https://github.com/BM-K/KoSimCSE.git
cd KoSimCSE
git clone https://github.com/SKTBrain/KoBERT.git
cd KoBERT
pip install -r requirements.txt
pip install .
cd ..
pip install -r requirements.txt
cd ..
pip install -r requirements.txt
```

### 설치 패키지 상세 항목
```bash
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install alembic
pip install "pydantic[email]"
pip install "passlib[bcrypt]"
pip install python-multipart
pip install "python-jose[cryptography]"

(Svelte 서버 개발시 사용하는 패키지)
cd frontend
npm install
npm install svelte-spa-router
npm install bootstrap
npm install moment
npm install qs
npm install marked
```

## MySQL 설치 시
<details>
<summary>더보기</summary>

### 설치 여부 확인
``` bash
mysql --version
```
### 설치가 되어 있지 않다면 MySQL 서버 설치
``` bash
sudo apt update
sudo apt install mysql-server
```
### 설치한 MySQL 서버 시작 및 상태 확인
``` bash
sudo systemctl start mysql
sudo systemctl status mysql
```
- Ubuntu 16.04 이하 버전   
``` bash
sudo service mysql start
sudo service mysql status
```
### root 계정 설정
``` bash
mysql -u root -p
```
- 초기에는 ```Enter password:```에 비밀번호를 입력하여 설정 가능
### 데이터베이스 생성
``` mysql
CREATE DATABASE db_name;
```
### 사용자 계정 생성 및 권한 부여
``` mysql
# 계정 생성 아이디 myacct, 비밀번호 0000
CREATE USER 'myacct'@'%' IDENTIFIED WITH mysql_native_password BY '0000';

# 권한 부여
GRANT ALL PRIVILEGES ON mydb.* TO 'myacct'@'%';

# 적용
FLUSH PRIVILEGES;
EXIT;
```
### mysqld.conf 파일 설정
- ```bind-address``` 주석처리
```
cd /etc/mysql/mysql.conf.d
vim mysqld.cnf
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
# bind-address           = 127.0.0.1
```
</details>

## 데이터베이스 초기화
```
alembic init migrations
```
- alembic.ini 파일 수정
    - ```sqlalchemy.url``` 주석처리
- config.py 의 DatabaseConfig를 알맞게 수정
```python
# 예시
host = "127.0.0.1"
port = 3306
name = "mydb"
user = "myacct"
pw = "0000"
```
- migrations/env.py 파일의 target_metadata를 아래와 같이 수정
```python
import models
target_metadata = models.Base.metadata
if not config.get_main_option("sqlalchemy.url"):
    from database import DB_URL
    config.set_main_option("sqlalchemy.url", DB_URL)
```
### 데이터베이스 업데이트
```
alembic revision --autogenerate
alembic upgrade head
```


# 서버 실행
* FastAPI 서버 실행   
```bash
uvicorn main:app --reload --host=0.0.0.0
```

* elasticsearch 서버 실행   
```bash
cd C:\Users\Angie\elasticsearch-8.15.0   
.\bin\elasticsearch.bat
```

* Svelte 서버 실행  
```bash 
cd frontend   
npm run dev
```
