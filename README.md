# flask(sqlalcemy) + jinja2(tailwindcoss) 를 이용한 blog 웹사이트

말 그대로 그냥 blog기능이 담긴 웹사이트이다.

mysql 을 사용한다 .

.env에서 수정하길

## Install 참고서

### 1.1 필수 설치할 pip들

```bash
pip install Flask gunicorn SQLAlchemy flask-bcrypt flask-wtf flask-login python-dotenv pymysql flask_sqlalchemy flask_cors
```

### 1.2 .env 생성

```bash
cp .env.bak .env
```

### 1.3 tailwindcss 설치 참고

### 1.3.1 tailwindcss 설치

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
npm install @tailwindcss/forms
```

### 1.3.2 tailwind.config.js 파일 수정

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./**/*.{html,js}"
    ],
    theme: {
        extend: {}
    },
    plugins: [
        require(
            "@tailwindcss/forms"
        )
    ]
};
```

npm run dev 하면 실행이 됨

### 1.4 flask 실행

디비깅

```bash
flask --app run.py --debug run 
```

### 배포는 따로 아래거 참고