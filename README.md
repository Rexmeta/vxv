# VXV.CO.KR URL 단축 서비스

간단하고 사용하기 쉬운 URL 단축 서비스입니다. 긴 URL을 짧고 기억하기 쉬운 형태로 변환해줍니다.

## 기능

- URL 단축
- 단축 URL 통계 (클릭 수, 생성일 등)
- 단축 URL 복사 기능
- 모바일 친화적인 반응형 디자인

## 로컬 개발 환경 설정

1. 저장소를 클론합니다:
```bash
git clone https://github.com/yourusername/vxv.co.kr.git
cd vxv.co.kr
```

2. 가상환경을 생성하고 활성화합니다:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

## Vercel 배포 방법

1. [Vercel CLI](https://vercel.com/download)를 설치합니다:
```bash
npm i -g vercel
```

2. Vercel에 로그인합니다:
```bash
vercel login
```

3. 프로젝트를 배포합니다:
```bash
vercel
```

4. 환경 변수 설정:
   - Vercel 대시보드에서 다음 환경 변수를 설정합니다:
     - `SECRET_KEY`: 랜덤한 문자열

5. 도메인 설정:
   - Vercel 대시보드에서 vxv.co.kr 도메인을 추가합니다
   - DNS 설정을 업데이트합니다

## 기술 스택

- Python 3.9+
- Flask
- Bootstrap 5
- HTML/CSS/JavaScript
- Vercel

## 라이선스

MIT License
