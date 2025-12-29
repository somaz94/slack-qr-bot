# Slack QR Bot - 프로젝트 분석 문서

## 프로젝트 개요

Slack QR Bot은 APK 다운로드 URL을 QR 코드 이미지로 변환하여 Slack 채널에 자동으로 전송하는 Flask 기반 RESTful API 서비스입니다. CI/CD 파이프라인과 통합하여 빌드된 APK 파일을 쉽게 배포하고 테스트할 수 있도록 설계되었습니다.

### 주요 사용 사례
- 모바일 앱 빌드 자동화 (Jenkins, GitLab CI, GitHub Actions)
- QA 팀에게 APK 배포
- 내부 테스터 그룹에 빌드 공유
- 다중 채널 동시 배포

---

## 아키텍처 및 기술 스택

### 기술 스택
- **언어**: Python 3.14
- **프레임워크**: Flask 3.0.0
- **API 문서화**: Flasgger (Swagger UI)
- **QR 코드 생성**: qrcode 7.4.2, Pillow 10.4.0
- **Slack 연동**: slack-sdk 3.26.1
- **Rate Limiting**: flask-limiter 3.5.0
- **재시도 로직**: tenacity 8.2.3
- **로깅**: python-json-logger 2.0.7
- **웹 서버**: Gunicorn 21.2.0

### 디렉토리 구조
```bash
slack-qr-bot/
├── src/
│   ├── app.py              # Flask 앱 팩토리 및 초기화
│   ├── config.py           # 환경 설정 및 Swagger 설정
│   ├── decorators.py       # API 키 인증 데코레이터
│   ├── services.py         # QR 생성 및 Slack 전송 서비스
│   ├── utils.py            # 유틸리티 함수 (응답 포맷 등)
│   └── routes/             # API 라우트 모듈
│       ├── health.py       # 헬스 체크 엔드포인트
│       ├── qr.py           # QR 코드 생성/전송 API
│       ├── channels.py     # Slack 채널 조회 API
│       └── slack_events.py # Slack 이벤트 핸들러
├── k8s/                    # Kubernetes 배포 매니페스트
│   ├── deployment.yaml     # 앱 배포
│   ├── api-key-secret.yaml # API 키 시크릿
│   ├── slack-token-secret.yaml # Slack 토큰 시크릿
│   └── harbor-robot-secret.yaml # Harbor 레지스트리 시크릿
├── Dockerfile              # 컨테이너 이미지 빌드
├── requirements.txt        # Python 의존성
└── README.md              # 사용자 가이드
```

---

## 핵심 기능

### 1. QR 코드 생성 및 전송
- URL을 QR 코드 이미지로 변환
- 커스터마이징 가능 (크기, 색상, 테두리)
- Slack 채널에 자동 업로드
- 빌드 번호 및 다운로드 URL 정보 포함

### 2. API 키 인증
- `X-API-Key` 헤더 기반 인증
- 외부 호출 보호 (CI/CD 파이프라인 전용)
- 개발 환경에서는 비활성화 가능

### 3. Rate Limiting
- 기본: 10회/분 (글로벌)
- QR 생성: 20회/분
- 브로드캐스트: 10회/분
- DoS 공격 방지

### 4. 자동 재시도 로직
- Slack API 실패 시 최대 3회 재시도
- 지수 백오프: 2초 → 4초 → 8초
- Tenacity 라이브러리 사용

### 5. 구조화된 JSON 로깅
- JSON 포맷 로그 출력
- ELK Stack/Loki 통합 용이
- 타임스탬프, 로그 레벨, 메시지, 컨텍스트 포함

### 6. 다중 채널 브로드캐스트
- 여러 Slack 채널에 동시 전송
- Public/Private 채널 지원
- 채널별 전송 결과 반환

### 7. Swagger UI 기반 API 문서화
- 인터랙티브 API 문서
- 모든 엔드포인트 테스트 가능
- 접속 경로: `/api-docs`

---

## API 엔드포인트

### 1. Health Check
```
GET /health
```
- Slack 연결 상태 확인
- 응답: 연결 상태, 팀/유저 정보, Bot ID

### 2. QR 코드 생성 및 전송
```
POST /generate-qr
Headers: X-API-Key: <your-api-key>
Body: {
  "apk_url": "https://example.com/app.apk",
  "channel": "#apk-qr-generator",
  "build_number": "123"  // optional
}
```

### 3. Slack 채널 목록 조회
```
GET /channels
Headers: X-API-Key: <your-api-key>
```
- Bot이 접근 가능한 모든 채널 반환
- Public/Private 채널 구분

### 4. 다중 채널 브로드캐스트
```
POST /broadcast-qr
Headers: X-API-Key: <your-api-key>
Body: {
  "apk_url": "https://example.com/app.apk",
  "channels": ["#channel1", "#channel2"],
  "build_number": "123"  // optional
}
```

---

## 환경 변수

### 필수 환경 변수
| 변수 | 설명 | 예시 |
|------|------|------|
| `SLACK_BOT_TOKEN` | Slack Bot OAuth Token | `xoxb-123456...` |

### 선택 환경 변수
| 변수 | 설명 | 기본값 |
|------|------|--------|
| `API_KEY` | API 인증 키 (프로덕션 권장) | 없음 (인증 비활성화) |
| `RATE_LIMIT_ENABLED` | Rate Limiting 활성화 여부 | `true` |
| `PORT` | 서비스 포트 | `8080` |

---

## 보안 및 안정성 기능

### 인증 메커니즘
- API 키 기반 인증으로 무단 접근 방지
- 환경 변수로 관리되어 소스 코드에 노출되지 않음

### Rate Limiting
- 메모리 기반 저장소 사용
- 엔드포인트별 개별 설정 가능
- 과도한 요청 시 429 에러 반환

### 에러 처리
- 모든 에러에 대한 구조화된 응답
- Slack API 실패 시 자동 재시도
- 상세한 에러 로그 기록

### 로깅
- JSON 형식으로 구조화
- 요청 IP, 엔드포인트, 타임스탬프 포함
- 컨테이너 환경에서 stdout으로 출력

---

## 배포 방법

### Docker 로컬 실행
```bash
docker run -d \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e API_KEY=your-secret-key \
  -p 8080:8080 \
  your-registry/slack-qr-bot:latest
```

### Kubernetes 배포
```bash
# Secret 생성
kubectl apply -f k8s/slack-token-secret.yaml
kubectl apply -f k8s/api-key-secret.yaml

# 앱 배포
kubectl apply -f k8s/deployment.yaml
```

### 필요한 Kubernetes Secret
1. **slack-token-secret**: Slack Bot Token
2. **api-key-secret**: API 인증 키
3. **harbor-robot-secret**: Harbor 레지스트리 접근 (이미지 pull용)

---

## Slack App 설정

### 필수 Bot Token Scopes
- `chat:write` - 메시지 전송
- `files:write` - 파일 업로드
- `channels:read` - Public 채널 정보 읽기
- `groups:read` - Private 채널 정보 읽기
- `groups:write` - Private 채널 접근
- `incoming-webhook`

### 설정 단계
1. [Slack API](https://api.slack.com/apps)에서 새 앱 생성
2. "From scratch" 선택
3. OAuth & Permissions에서 위 스코프 추가
4. 워크스페이스에 앱 설치
5. Bot Token 복사 (`xoxb-`로 시작)
6. 채널에 Bot 초대: `/invite @your-bot-name`

---

## 주요 코드 모듈 설명

### `src/app.py`
- Flask 애플리케이션 팩토리 패턴 사용
- Blueprint 등록 및 Rate Limiter 초기화
- Swagger 문서화 설정

### `src/config.py`
- 환경 변수 검증 (`validate_env()`)
- Swagger 템플릿 및 설정
- JSON 로깅 설정 (`setup_logging()`)

### `src/decorators.py`
- `@require_api_key`: API 키 인증 데코레이터
- 헤더 검증 및 401/403 응답 처리

### `src/services.py`
- `generate_qr_code()`: QR 코드 이미지 생성
- `send_qr_to_slack()`: Slack API를 통한 파일 업로드
- `check_slack_connection()`: 연결 상태 확인
- `get_bot_channels()`: Bot이 접근 가능한 채널 목록 반환
- Tenacity를 통한 자동 재시도 로직 적용

### `src/utils.py`
- 표준화된 응답 포맷 함수들
- `success_response()`, `bad_request()`, `unauthorized()` 등

### `src/routes/`
- `health.py`: `/health` 헬스 체크
- `qr.py`: `/generate-qr`, `/broadcast-qr` QR 생성 API
- `channels.py`: `/channels` 채널 목록 API
- `slack_events.py`: Slack 이벤트 웹훅 핸들러

---

## 테스트 방법

### 로컬 테스트
```bash
# Python 가상 환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export SLACK_BOT_TOKEN=xoxb-your-token
export API_KEY=test-api-key

# 앱 실행
python -m src.app
```

### API 테스트 (curl)
```bash
# Health Check
curl http://localhost:8080/health

# QR 생성
curl -X POST http://localhost:8080/generate-qr \
  -H "X-API-Key: test-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "apk_url": "https://example.com/app.apk",
    "channel": "#test-channel",
    "build_number": "123"
  }'
```

### Swagger UI 테스트
- 브라우저에서 `http://localhost:8080/api-docs` 접속
- 각 엔드포인트를 인터랙티브하게 테스트

---

## CI/CD 통합 예시

### Jenkins Pipeline
```groovy
stage('Send QR to Slack') {
    steps {
        sh '''
            curl -X POST https://qr-bot.example.com/generate-qr \
                -H "X-API-Key: ${SLACK_QR_API_KEY}" \
                -H "Content-Type: application/json" \
                -d '{
                    "apk_url": "'${APK_URL}'",
                    "channel": "#apk-releases",
                    "build_number": "'${BUILD_NUMBER}'"
                }'
        '''
    }
}
```

### GitLab CI
```yaml
send_qr:
  stage: deploy
  script:
    - |
      curl -X POST $SLACK_QR_BOT_URL/generate-qr \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
          \"apk_url\": \"$APK_URL\",
          \"channel\": \"#apk-releases\",
          \"build_number\": \"$CI_PIPELINE_IID\"
        }"
```

---

## 문제 해결

### Slack API 에러
- **에러**: `not_in_channel`
  - **해결**: 채널에 Bot을 초대 (`/invite @bot-name`)
  
- **에러**: `invalid_auth`
  - **해결**: `SLACK_BOT_TOKEN` 확인, `xoxb-`로 시작하는지 확인

### Rate Limiting 비활성화
```bash
export RATE_LIMIT_ENABLED=false
```

### 로그 확인
```bash
# Docker 로그
docker logs <container-id>

# Kubernetes 로그
kubectl logs -f deployment/slack-qr-bot
```

---