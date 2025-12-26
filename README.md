# Curator Toy Project

개인 관심사를 기반으로 뉴스·콘텐츠를 수집하고 저장하는  
**개인화 콘텐츠 큐레이션 MVP**입니다.

RSS 기반 수집 → PostgreSQL 저장 → API 조회까지의  
엔드투엔드 파이프라인을 목표로 합니다.

---

## 1. 프로젝트 목표

- RSS 기반 콘텐츠 자동 수집
- 중복 제거된 데이터 저장
- 간단한 조회 API 제공
- 확장 가능한 구조 설계 (추천, 요약, 스케줄링)

---

## 2. 기술 스택

- Python 3.9.6
- FastAPI
- PostgreSQL (Docker)
- SQLAlchemy 2.x
- feedparser (RSS)
- Docker Compose

---
