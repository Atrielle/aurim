# UI Direction

## Why This Exists

이 문서는 현재 저장소에 남아 있지 않은 초기 UI 감성을 보존하기 위해 만든다.
초기 코드베이스에는 차량 관제 도메인 위에 얹힌 대시보드형 인터랙션 UI가 있었고,
그 구조와 시각적 인상을 Aurim에 재해석해서 가져오는 것이 목표다.

## Original Interaction Memory

원래 UI에서 기억해야 할 요소는 아래와 같다.

- 강한 대시보드형 색감
- 카드와 패널 중심 레이아웃
- 위젯 단위 정보 조합
- 일부 패널 또는 위젯을 움직이거나 재배치할 수 있는 감각
- 정적인 사이드바만이 아닌 떠 있는 메뉴나 액션 UI
- 편집 모드, 조작 가능성, 운영 콘솔 같은 분위기

이 감성은 현재 코드에 남아 있지 않지만, 제품 방향으로 계속 유지해야 한다.

## Translation Into Aurim

Aurim은 협업 플랫폼이므로 과거의 차량 관제 UI를 그대로 복제하지 않는다.
대신 아래처럼 재해석한다.

- workspace home은 단순 landing page가 아니라 customizable dashboard가 된다
- 문서, 파일, 작업, 활동은 카드형 패널과 정보 밀도 높은 블록으로 표현한다
- 사용자는 일부 패널, 컬렉션, 보드 구성을 재배치할 수 있어야 한다
- 주요 액션은 정적인 메뉴 외에 floating command 또는 action rail 형태도 고려한다
- 화면은 너무 가벼운 소비형 SaaS보다 운영 콘솔과 협업 워크벤치 사이 감각을 가진다

## Visual Guardrails

- 기본 흰색 바탕에 연한 보라색 SaaS 템플릿 같은 화면으로 가지 않는다
- 지나치게 장식적인 마케팅 사이트 스타일로 가지 않는다
- 카드, 보드, 사이드 패널, 오버레이, 명령 UI가 공존하는 제품형 화면을 지향한다
- 정보 밀도는 어느 정도 높게 유지하되 혼잡하지 않게 정리한다
- 웹과 모바일은 같은 도메인 모델을 쓰되, 웹은 더 도구적이고 조작 가능한 UI를 가진다

## Product Areas That Should Inherit This Feel

- Workspace Home
- Work Item board and planning views
- Factory App dashboard
- Artifact viewer
- Activity and audit surfaces
- Git workspace surface

## Do Not Forget

Aurim의 UI는 단순 CRUD 앱이 아니라 다음 두 이미지를 동시에 가져야 한다.

1. 협업 플랫폼
2. 조작 가능한 작업 워크벤치

다음 에이전트는 새 화면을 만들 때 이 문서를 먼저 읽고,
너무 평범한 엔터프라이즈 SaaS UI로 평탄화하지 않도록 주의해야 한다.
