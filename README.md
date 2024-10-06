# NuriPlanner


# 데이터
- [누리놀이 교육계획안](https://www.nurinori.com/index.do)


# API 명세
|API명|요청방법|URL|설명|
|:------:|:----:|:-------------------------|:-------------------------|
|목록조회|get|/api/plan/list|전체 계획안을 조회한다|
|상세조회|get|/api/plan/detail/{plan_id}|계획안(plan_id)에 대한 상세 내역을 조회한다|
|추천목록조회|get|/api/recplan/{plan_id}/list|계획안(plan_id)에 대한 추전 목록을 조회한다|
|계획안등록|post|/api/plan/create|새로운 계획안을 등록한다|
|회원가입|post|/api/user/create|새로운 회원을 등록한다|
|로그인|post|/api/user/login|로그인을 실행한다|
|계획안수정|put|/api/plan/update|계획안을 수정한다|
|계획안삭제|delete|/api/plan/delete|계획안을 삭제한다|

# 서버 실행
* FastAPI 서버 실행
uvicorn main:app --reload

* elasticsearch 서버 실행
cd C:\Users\Angie\elasticsearch-8.15.0
.\bin\elasticsearch.bat

* Svelte 서버 실행
cd frontend
npm run dev
