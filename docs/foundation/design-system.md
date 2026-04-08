# Design System: Living Intelligence

## 1. Overview

### Creative North Star

**Living Intelligence**

Aurim의 시각 시스템은 정적인 업무 화면이 아니라, 반응하고 흐르는 협업 워크벤치를 지향한다.
이 시스템은 평면적인 템플릿형 SaaS 화면을 피하고,
공기감, 빛, 깊이, 비대칭, 위젯형 조합을 통해 정보가 살아 움직이는 인상을 만든다.

핵심 방향은 다음과 같다.

- static dashboard가 아니라 kinetic workspace
- bootstrap-style sectioning이 아니라 tonal layering
- rigid symmetry가 아니라 intentional asymmetry
- flat CRUD card가 아니라 editorial presentation

이 문서는 `docs/foundation/ui-direction.md`를 감성 문서로 두고,
실제 색상, 표면, 타이포, 컴포넌트 규칙을 정의하는 규격 문서다.

## 2. Color Philosophy

팔레트는 고명도 중성 배경 위에 kinetic accent를 얹는 구조다.
협업 제품이지만 지나치게 단조롭거나 보수적인 회색 업무툴처럼 보이지 않게 한다.

### Core Palette

- `surface`: `#f5f7f9`
- `surface_container_low`: `#eef1f3`
- `surface_container_lowest`: `#ffffff`
- `surface_bright`: `#f5f7f9`
- `on_surface`: `#2c2f31`
- `outline_variant`: `#d7dce0`

### Accent Palette

- `primary`: `#006760`
- `primary_container`: `#73f1e4`
- `secondary`: `#9b3e20`
- `secondary_container`: `#ffc4b3`
- `tertiary`: `#6d42b5`
- `tertiary_container`: `#c29fff`
- `sky_blue`: `#42A5F5`

### Semantic Use

- `primary` 계열은 주요 액션, 성장, 핵심 상태
- `secondary` 계열은 경고, 주의, 에너지 강한 하이라이트
- `tertiary` 계열은 깊은 인사이트, 고급 분석, 보조 데이터 흐름
- `sky_blue`는 보조 유틸리티 액션 및 연결성 표현

## 3. Surface Architecture

### No-Line Rule

섹션 구분이나 카드 경계에 기본적으로 `1px solid border`를 쓰지 않는다.
구조 경계는 아래 둘로만 만든다.

- 배경 톤 차이
- surface hierarchy에 따른 레이어링

### Surface Hierarchy

- base canvas: `surface`
- low priority section: `surface_container_low`
- standard card: `surface_container_lowest`
- elevated overlay: `surface_bright`

### Glass And Gradient Rule

floating navigation, tooltip, command surface에는 glass-like 처리를 허용한다.

- glass base: `surface_container_lowest` at `70%` opacity
- backdrop blur: `20px`
- primary CTA는 단일 flat fill보다 gradient 사용을 우선

## 4. Typography

기본 서체는 `Manrope`를 기준으로 한다.
기하학적이고 현대적인 인상을 유지하면서 소형 텍스트 가독성을 확보하기 위함이다.

### Type Tokens

- `display-lg`: `3.5rem`, `700`
- `headline-md`: `1.75rem`, `600`
- `title-md`: `1.125rem`, `500`
- `body-lg`: `1rem`, `400`
- `label-md`: `0.75rem`, `600`

### Typography Rules

- `label-md`는 넓은 letter-spacing을 사용해 메타데이터와 overline에 권위감을 준다
- pure black는 쓰지 않고 `on_surface`를 기본 텍스트 색으로 사용한다
- KPI나 메인 숫자는 display 계열을 사용하되 과도한 장식을 넣지 않는다

## 5. Elevation And Depth

깊이는 shadow보다 tonal layering으로 만든다.

### Layering Principle

- static card에는 과한 shadow를 쓰지 않는다
- `surface_container_lowest`를 `surface_container_low` 위에 놓아 부드러운 lift를 만든다

### Ambient Shadow

interactive 또는 floating 요소에만 확산된 shadow를 사용한다.

- blur: `40px - 60px`
- opacity: `4% - 8%`
- shadow tint: `on_surface`

### Ghost Border Fallback

접근성상 경계가 꼭 필요하면 `outline_variant`를 `15%` opacity 수준으로만 사용한다.
절대 진한 실선 경계 기본값으로 가지 않는다.

### Roundedness

- visible interactive container minimum: `0.75rem`
- preferred rounded scale: `1rem` or `1.5rem`

## 6. Component Rules

### Buttons

- primary: `primary -> primary_container` gradient, white text, rounded `xl`
- secondary: `surface_container_low` background, `on_surface` text, no border
- tertiary: ghost style, hover 시 subtle accent underline 허용

### Living Cards

- 내부 divider를 쓰지 않는다
- 내부 콘텐츠 구분은 spacing으로 해결한다
- hover 시 배경 톤이 미세하게 변하거나 ambient shadow가 조금 강해질 수 있다

### Kinetic Charts

- line stroke width: `3px`
- 가능한 경우 smooth interpolation 사용
- line 아래 area fill은 `10%` opacity 수준
- tooltip은 glass rule을 따른다
- chart는 약한 entry motion을 가진다

### Inputs

- 기본: `surface_container_low` 기반 soft-filled input
- focus: `surface_container_lowest`로 전환
- 필요 시 primary tinted ghost border 사용

## 7. Layout Principles

### Organic Minimalism

레이아웃은 지나치게 균일한 그리드 복제를 피한다.
다만 무질서하게 만들라는 뜻은 아니다.

- 카드 높이는 반드시 모두 같을 필요가 없다
- 비대칭은 의도적으로만 사용한다
- whitespace는 구조 요소다
- 정보 밀도는 높게 가져가되, 압축감보다 호흡을 우선한다

### Workbench Feel

Aurim은 단순 문서 관리 앱이 아니라 협업 워크벤치다.
다음 요소를 적극적으로 고려한다.

- customizable dashboard
- movable or rearrangeable panels
- floating command surface
- action rail
- split view or side inspector
- artifact and activity overlays

## 8. Do

- white space를 구조 요소로 사용한다
- secondary와 tertiary 색으로 서로 다른 정보 흐름을 분리한다
- 중요한 차트나 상태 변화에 약한 motion을 넣는다
- card, board, panel, overlay가 함께 있는 제품형 화면을 지향한다
- workspace home을 정적인 welcome page로 끝내지 않는다

## 9. Do Not

- pure black text를 쓰지 않는다
- 1px solid border로 리스트나 패널을 쪼개지 않는다
- sharp 90-degree corners를 사용하지 않는다
- 카드 하나에 너무 많은 복잡도를 밀어 넣지 않는다
- 평범한 템플릿형 엔터프라이즈 SaaS 화면으로 평탄화하지 않는다
- 보라색 한 톤에 치우친 기본 SaaS 스타일로 가지 않는다

## 10. Relationship To Implementation

다음 에이전트 또는 작업자는 프론트 작업 전 반드시 아래 문서를 읽는다.

- `docs/foundation/ui-direction.md`
- `docs/foundation/design-system.md`
- `docs/foundation/resume-context.md`

UI를 새로 만들 때는 이 문서를 기준으로 토큰, 카드, 패널, CTA, overlay 스타일을 잡는다.
원래 구현은 사라졌더라도, 감성과 규칙은 이 문서로 유지한다.
