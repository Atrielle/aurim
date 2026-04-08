> Note
> 이 문서는 특정 시점의 비용/아키텍처 리서치 결과를 보존한 참고 자료다.
> 현재 Aurim의 기준 스택이나 저장소 구조의 authoritative 문서는 아니다.
> 현재 기준은 `README.md`, `docs/foundation/product-philosophy.md`, `docs/foundation/governance-model.md`, `docs/foundation/cloud-handoff.md`를 따른다.
# 월 $100 이하 멀티에이전트 AI 개발·운영 사이클을 가장 밸런스 있게 설계하는 방법

## Executive Summary

월 $100 이하에서 “계획→실행→평가→반복”을 **실제로 굴러가게** 만들려면, 모델 성능 경쟁보다 **(1) 비용을 예측 가능하게 만들고 (2) 에이전트 폭주를 제어하며 (3) 평가·관측을 먼저 깔아** 반복 개선이 가능하도록 해야 합니다. 특히 멀티에이전트는 호출 수가 늘어나는 순간 비용·지연·디버깅 난이도가 기하급수로 악화되므로, 초반에는 **에이전트 수를 최소화(3~5개)** 하고 “동기(실시간) 경로”와 “비동기(배치/야간) 경로”를 분리하는 게 가장 큰 승부처입니다. citeturn18search5turn19search34

본 보고서는 비용대를 3개로 나눠, 각 구간에서 가장 균형이 잘 맞는 아키텍처를 제안합니다(2026-04-08 기준 요금/문서 기반).

- **저가(≤$30): “모델 라우팅 + 무료 관측(OTel/Grafana) + 배치 평가”**  
  메인 추론은 비용 대비 성능이 좋은 미니급 모델로 고정하고, 평가/회귀 테스트는 할인(배치)로 돌려 비용을 잠급니다. 캐싱(프롬프트/시맨틱)로 호출 수를 줄이는 쪽이 핵심입니다. citeturn10view3turn18search3turn9search0
- **중간($31–$70): “유료 LLM옵스(예: Langfuse Core)로 실험·A/B·리그레션을 체계화”**  
  이 구간부터는 모델 비용보다 **관측/평가 체계 부재가 더 큰 손실**을 만듭니다. $29 수준의 관리형 관측/평가를 깔고, 라우팅(미니↔상위 모델)로 품질을 올립니다. citeturn10view5turn10view3
- **고가($71–$100): “상위 모델(또는 상위 비중 확대) + 유료 관측/평가 + 운영 안전장치(가드레일/승인)”**  
  이 구간은 “정답률/추론력”에 예산을 더 써도 되는 구간입니다. 단, 상위 모델만 늘리면 비용 폭주가 쉬우니 **에이전트 실행을 그래프/상태기계로 고정**하고, 평가 결과로만 프롬프트/정책을 업데이트하는 폐루프를 권합니다. citeturn19search34turn18search1

---

## 문제 정의와 설계 목표

멀티에이전트 기반 개발·운영 사이클은 본질적으로 아래의 루프입니다.

- **계획(Plan)**: 목표 분해, 역할 할당, 도구/데이터 계획, 비용/시간 예산 설정  
- **실행(Act)**: 에이전트(또는 도구)가 작업 수행, 상태/로그 저장, 실패 시 재시도/대체 경로  
- **평가(Evaluate)**: 정량 지표(성공률/지연/비용) + 정성 지표(품질/안전)로 점수화  
- **반복(Iterate)**: 프롬프트/정책/라우팅/도구를 변경하고 다시 비교(A/B, 회귀 테스트)

문제는 “루프를 만들었다”로 끝나지 않습니다. 월 $100 이하라는 제약에선 특히 다음 두 가지가 실패 원인입니다.

1) **에이전트 호출 수 폭증**: 멀티에이전트는 “에이전트 수 × 단계 수 × 재시도”로 호출이 늘며, 품질이 조금 좋아져도 운영이 불가능해집니다. 그래서 **동기 경로는 짧고 결정적으로**, 비동기 경로에서 대량 평가를 처리해야 합니다. citeturn19search34turn10view3  
2) **평가·관측 부재**: 평가가 없으면 개선이 “감”에 의존하고, 결국 모델만 키우다 비용이 터집니다. OpenAI/Anthropic 모두 평가(evals)를 통해 변동성을 관리하라고 명시합니다. citeturn19search34turn7search2  

---

## 밸런스 설계 원칙

### 비용을 “상한선 있는 구조”로 만든다

- **프롬프트 캐싱을 기본 전제로 설계**: 반복되는 시스템 프롬프트/툴 스키마/정책 텍스트는 캐싱이 먹도록 고정(prefix 안정화)해야 합니다. OpenAI는 프롬프트 캐싱이 **지연을 최대 80%**, **입력 비용을 최대 90%** 줄일 수 있다고 명시합니다. citeturn18search3turn10view3  
- **배치(비동기)로 평가·대량 작업 비용을 잠근다**: OpenAI는 Batch에서 동일 모델 입력/출력 단가가 크게 낮습니다(예: GPT-5.4-mini가 Standard 대비 절반 수준). citeturn10view3  
- **“상위 모델은 일부 구간에만”**: 계획/비평/난해한 추론에만 상위 모델을 쓰고, 나머지는 미니/나노/저가 모델로 처리합니다(모델 라우팅). 모델 라우팅이 없으면 월 $100을 유지하면서 멀티에이전트를 돌리기 어렵습니다. citeturn10view3turn19search34  

### 성능은 “지연”과 “품질”을 분리해 다룬다

- 사용자 체감 지연을 줄이려면 **동기 경로**에서 계획 단계가 길어지지 않게 해야 합니다.  
- 반대로 품질을 올리려면 **비동기 경로**에서 평가(회귀/리그)와 프롬프트 개선을 돌려야 합니다. 평가가 없으면 품질을 올릴 방법이 “더 비싼 모델”밖에 남지 않습니다. citeturn19search34turn7search2  

### 확장성은 “에이전트 수”가 아니라 “병렬 단위(작업)”로 잡는다

- 에이전트 수를 늘리기 전에, **작업 큐(버스)** 와 **idempotency(중복 실행 안전)** 를 먼저 갖춥니다.  
- 동기 경로는 1~2개 핵심 에이전트(오케스트레이터/툴 실행)만, 나머지는 비동기로 분산시키는 게 운영 난이도를 급격히 낮춥니다.

### 통합과 생산성은 “하네스(harness)”를 얼마나 직접 짤지로 결정된다

멀티에이전트에서 하네스는 “루프를 돌리는 런타임”입니다. 최소한 아래를 포함합니다.

- 상태 관리(대화/작업 ID, 단계, 체크포인트)
- 도구 호출(함수/HTTP/DB) 스키마 검증
- 재시도/타임아웃/서킷 브레이커
- 로깅/트레이싱/비용 집계
- 평가 실행 및 결과 비교(A/B, 회귀)

하네스를 직접 짜면 유연하지만 운영 복잡도가 폭증합니다. 따라서 초반엔 SDK/프레임워크를 쓰는 게 이득입니다.

- **entity["company","OpenAI","ai research company"] Agents SDK**는 에이전트 실행 루프/핸드오프/도구/트레이싱을 제공하며, “에이전트는 계획하고 도구를 호출하며 여러 전문가(에이전트)와 협업한다”는 정의를 명시합니다. citeturn18search1turn18search5turn18search11  
- 트레이싱은 에이전트 실행 중 발생한 LLM 생성/툴 호출/핸드오프/가드레일 이벤트를 기록한다고 문서에 명시되어, 디버깅·운영 관측의 기반이 됩니다. citeturn18search11  

### 평가·모니터링은 “정량+정성”을 동시에 자동화한다

- OpenAI는 “모델 출력은 변동적이라 전통적 테스트만으로 부족하며 evals로 시험해야 한다”고 평가 베스트 프랙티스에서 강조합니다. citeturn19search34  
- RAG/에이전트 워크플로우는 “정답성/근거성/맥락 적합성”이 핵심이므로, Ragas/DeepEval 같은 프레임워크로 자동 점수화를 권합니다. citeturn8search4turn8search5  

---

## 비용대별 추천 아키텍처

아래 3개 아키텍처 모두 공통적으로 “계획→실행→평가→반복” 폐루프를 갖습니다. 차이는 **(1) 관측/평가를 어디까지 유료로 사는지 (2) 상위 모델 비중을 얼마나 늘리는지 (3) 운영 복잡도를 어디에 두는지** 입니다.

### 저가 아키텍처

#### 개념

“최소 비용으로도 멀티에이전트를 운영 가능한 형태로 만들기”가 목적입니다. 핵심은 **(a) 미니급 모델 고정 (b) 캐싱/배치 평가로 비용 상한을 잠금 (c) 관측은 무료 스택으로 해결** 입니다. OpenAI의 프롬프트 캐싱/배치 단가 구조를 적극 활용합니다. citeturn10view3turn18search3  

#### 구성요소

- **모델**
  - 동기(실시간) 실행: GPT-5.4-mini (메인) citeturn10view3  
  - 가드레일/분류/간단 판단: GPT-5.4-nano (저가) citeturn10view3  
  - 오프라인 평가: Batch로 GPT-5.4-mini 사용(단가 절감) citeturn10view3  
- **호스팅**
  - entity["company","Fly.io","cloud hosting company"]: shared-cpu-1x(1GB) 기준 월 $5.70 수준(상시 구동 가정) citeturn10view6  
- **오케스트레이션**
  - OpenAI Agents SDK(파이썬)로 “오케스트레이터 1 + 서브에이전트(전문가) 2~3” 구성 citeturn18search12turn18search4turn18search11  
- **데이터 스토리지**
  - entity["company","Neon","serverless postgres provider"] Free plan(월 $0) citeturn3search9  
  - (선택) 로컬/서버 SQLite: 세션 캐시/임시 상태
- **모니터링/로그**
  - entity["company","Grafana Labs","observability company"] Grafana Cloud Free($0) citeturn9search0  
  - OpenTelemetry 기반 트레이스/메트릭(수집→Grafana Cloud로 전송)  
- **CI/CD**
  - entity["company","GitHub","code hosting company"] Actions(기본 무료 쿼터 + 사용량 과금 구조) citeturn9search3turn9search19  

#### 멀티에이전트 통신 패턴 및 동기/비동기 권장

- **통신 패턴(권장): 중앙집중 오케스트레이터 + 핸드오프(계층형)**  
  핸드오프는 “특화 에이전트에게 작업을 위임”하는 개념(툴 형태)로 문서화되어 있습니다. citeturn18search4turn18search16  
- **동기(실시간)**: 사용자 응답 경로는 최대 3스텝으로 제한(분류→계획→실행/요약)  
- **비동기(배치)**: 평가/리그레션/대량 분류는 Batch로 분리(24시간 내 처리 허용) citeturn10view3turn19search34  

#### 하네스 엔지니어링 필요성 및 대체

- **필요 수준: 중급(프레임워크 사용 전제)**  
  Agents SDK가 루프와 트레이싱을 제공하므로 “상태 모델/재시도/도구 래퍼” 정도만 직접 구현하면 됩니다. 트레이싱이 기본 제공된다고 명시되어 관측 부담이 줄어듭니다. citeturn18search11turn18search9  
- **대체 옵션**
  - “평가를 더 강하게” 하고 싶으면 openai/evals(오픈소스 프레임워크)로 회귀 테스트를 구성 citeturn7search2turn7search6  
  - RAG가 있으면 Ragas(예: ContextPrecision, Faithfulness)로 자동 점수화 citeturn8search0turn8search11  
  - 유닛테스트 스타일이면 DeepEval(LLM 앱용 pytest 유사) citeturn8search5  

#### 예상 월비용 산정(예시)

**전제(예시 워크로드)**  
- 월 500 워크플로우 실행  
- 워크플로우당 8회 LLM 호출(오케스트레이터+서브에이전트)  
- 호출 1회 평균: 입력 1,500 토큰 / 출력 900 토큰  
- 이 중 500 토큰은 캐시되는 고정 prefix(시스템/정책/툴 스키마)로 가정  
- 월 200 워크플로우는 오프라인 평가(배치)로 추가 실행

**비용(대략)**
- LLM(실시간): GPT-5.4-mini 기준 약 **$19.35/월**(캐시 반영) citeturn10view3  
- LLM(오프라인 평가): 같은 패턴을 Batch로 200회 실행 시 약 **$3.87/월**(Batch 단가 반영) citeturn10view3  
- 호스팅: Fly.io shared-cpu-1x 1GB **$5.70/월** citeturn10view6  
- DB: Neon Free **$0/월** citeturn3search9  
- 모니터링: Grafana Cloud Free **$0/월** citeturn9search0  

→ **합계 약 $28.9/월** (저가 구간 충족)

#### 장단점

- 장점:  
  비용 상한선이 매우 명확(캐시+배치)하며, SDK 기반으로 멀티에이전트 루프/트레이싱을 빠르게 마련 가능. citeturn10view3turn18search11turn18search3  
- 단점:  
  관리형 LLM 옵스(실험/데이터셋/라벨링/리포트)가 없어서, 팀/프로덕션 규모로 커질 때 “분석 업무”가 개발자에게 전가됨.

#### 구현 난이도

- **중급**(SDK를 쓴다면) / **고급**(전부 직접 하네스 구현 시)

#### 샘플 기술 스택

- Runtime/API: Python 3.12 + FastAPI  
- Orchestrator: OpenAI Agents SDK(Python) citeturn18search12turn18search5  
- Observability: OpenTelemetry → Grafana Cloud citeturn9search0  
- Eval: openai/evals + DeepEval + (RAG 시) Ragas citeturn7search2turn8search5turn8search4  
- 대체 모델 옵션(저비용):
  - entity["company","Mistral AI","ai company france"] Mistral Large 3는 $0.5/$1.5 per 1M tokens(입/출)로 공식 문서에 명시되어 매우 저렴합니다. citeturn20view2  
  - entity["company","Cohere","ai company canada"] Command/Command-light 등도 공식 가격 FAQ에 입력/출력 단가 예시가 있습니다. citeturn20view1  

---

### 중간 아키텍처

#### 개념

이 구간은 “모델을 키우는 비용”보다 “**실험/평가/관측의 결여로 인한 개발 시간 낭비**”가 더 큽니다. 따라서 **관리형 LLM 옵스(관측+평가+프롬프트 버전/A·B)** 를 하나 붙이는 게 가장 밸런스가 좋습니다.

여기서는 Langfuse Cloud Core($29/월)를 중심으로 설계합니다. citeturn10view5  

#### 구성요소

- **모델**
  - 기본: GPT-5.4-mini  
  - 상위 작업(난해한 문제/정책 생성/리그레션 원인 분석): GPT-5.4 일부 비중 투입(예: 10~30%) citeturn10view3  
- **호스팅**
  - Fly.io(1GB) 또는 Render Starter($7) 같은 “항상 켜진” 소형 서비스 citeturn10view6turn5search1  
- **오케스트레이션**
  - OpenAI Agents SDK + 작업 큐(간단히는 Postgres 기반 job 테이블)  
- **데이터 스토리지**
  - Neon Free + pgvector(가능 시) 또는 벡터DB 무료 티어(Qdrant 등)  
- **모니터링/평가**
  - entity["company","Langfuse","llm observability company"] Langfuse Cloud Core **$29/월**, 100k units 포함(초과 $8/100k) citeturn10view5turn7search28  
  - Langfuse는 self-host도 가능(오픈소스/MIT, 무료)지만, 이 비용대에선 “운영 시간”이 더 비싸므로 Cloud Core를 추천합니다. citeturn15search14turn10view5  
- **CI/CD**
  - GitHub Actions + “평가 실패 시 배포 차단” 게이트

#### 통신 패턴 및 동기/비동기 권장

- **통신 패턴(권장): 중앙집중 + 작업 버스(혼합형)**  
  - 실시간: 오케스트레이터가 동기 처리(최대 3~4스텝)  
  - 비동기: 큐/워커가 “추가 조사·재시도·후평가”를 처리  
- Langfuse는 “Traces + Observations + Scores”를 units로 과금하는 구조이므로, 로그를 무조건 다 남기기보다 **샘플링(예: 10~30%)** 을 도입해 비용을 통제합니다. citeturn7search28turn7search36  

#### 하네스 엔지니어링 필요성 및 대체

- **필요 수준: 중급**  
  - Agents SDK로 실행 루프/핸드오프/트레이싱을 해결 citeturn18search11turn18search4  
  - Langfuse가 관측·평가·프롬프트 버전 관리 역할을 일부 흡수  
- **대체**
  - 관측을 프록시 방식으로 최소 코드 변경으로 붙이고 싶으면 entity["company","Helicone","llm observability company"] 같은 게이트웨이도 고려 가능(단, 유료 플랜은 이 구간에선 비쌈). 무료 tier는 10,000 requests 제공. citeturn10view4  
  - 완전 데이터 통제를 원하면 Langfuse self-host(무료/MIT) 또는 Phoenix self-host(무료) citeturn15search14turn17search1  

#### 예상 월비용 산정(예시)

**전제(혼합 라우팅 예시)**  
- 월 500 워크플로우 중 25%는 GPT-5.4(상위)로, 75%는 GPT-5.4-mini로 실행(대표적으로 “계획/비평 단계만 상위 모델”) citeturn10view3  
- Langfuse Cloud Core 사용

**비용(대략)**
- LLM: 약 **$33/월**(혼합 라우팅 가정, 토큰/캐시 반영) citeturn10view3  
- Langfuse Cloud Core: **$29/월** citeturn10view5  
- 호스팅(Fly 1GB): **$5.70/월** citeturn10view6  
- DB(Neon Free): **$0/월** citeturn3search9  

→ **합계 약 $67.7/월** (중간 구간 충족)

#### 장단점

- 장점:  
  - “실험-평가-배포” 루프가 실제로 굴러갑니다(프롬프트 버전/A·B/점수/리포트). citeturn10view5turn19search34  
  - 상위 모델을 “필요한 구간만” 쓰므로 품질과 비용을 동시에 관리 가능. citeturn10view3  
- 단점:  
  - 관측 데이터가 늘면 units 과금이 올라갈 수 있어 샘플링/요약 로그 전략이 필요합니다. citeturn7search28turn7search36  

#### 구현 난이도

- **중급**(추천)  
  - 단, “이벤트 기반 비동기 워커 + 재시도 정책 + 멱등성”까지 깔면 중상급

#### 샘플 기술 스택

- Runtime/API: Python 3.12, FastAPI  
- Agent loop: OpenAI Agents SDK citeturn18search12  
- Observability/Evals: Langfuse Cloud Core citeturn10view5  
- Offline eval: openai/evals + DeepEval(회귀/채점) citeturn7search2turn8search5  

---

### 고가 아키텍처

#### 개념

이 구간은 “품질/안전/운영 안정성”을 우선순위로 둘 수 있습니다. 추천은 **상위 모델 비중 확대 + 유료 관측/평가 유지 + 가드레일/승인(approvals)로 도구 오남용 방지** 입니다. Agents SDK는 가드레일 개념을 제공하며(빠른/저가 모델로 입력·출력 검증), 트레이싱을 통해 실행 흐름을 관측할 수 있습니다. citeturn18search15turn18search11  

#### 구성요소

- **모델**
  - 상위 추론: GPT-5.4 (핵심 단계에 넓게 투입) citeturn10view3turn19search28  
  - 보조/서브에이전트: GPT-5.4-mini(속도/비용) citeturn10view3  
  - 대안(다른 벤더 상위 모델):  
    - entity["company","Anthropic","ai safety company"] Claude Sonnet 4.6는 $3/$15 per MTok(입/출)로 문서에 명시되어 있고, Batch는 $1.5/$7.5로 할인됩니다. citeturn21view0  
- **호스팅**
  - Fly.io 2GB 또는 Render Standard($25)로 여유를 확보(동시성/워크큐 처리량) citeturn10view6turn5search1  
- **오케스트레이션**
  - Agents SDK + “그래프형 실행(단계 고정)” 운영 규칙(무한 루프/자기반복 방지)
- **데이터 스토리지**
  - Neon Free 또는 필요 시 유료 Postgres(예: Supabase Pro $25 등)  
- **모니터링/평가**
  - Langfuse Cloud Core($29) 유지  
  - 또는 self-host Phoenix로 “데이터 외부 반출 최소화” (Phoenix self-host는 기능 제한 없이 무료이며 데이터가 인프라 내부에 남는다고 명시) citeturn17search1  
- **CI/CD**
  - PR마다 “스모크 eval(짧은 데이터셋)” 실행 + merge 차단  
  - 야간에 “풀 리그레션 eval(큰 데이터셋)” 실행(배치/할인 활용)

#### 통신 패턴 및 동기/비동기 권장

- **통신 패턴(권장): 중앙집중 오케스트레이터 + 분산 워커(버스형)**  
  - 실시간 응답은 오케스트레이터가 책임지고,  
  - 검색/장문 분석/대량 검증/리그레션은 워커로 비동기 처리  
- **동기 추천**: 사용자에게는 “중간 결과(작업 계획/진행률)”를 먼저 스트리밍하고, 최종 품질 보정(리라이트/팩트체크)은 비동기 후속으로 붙이는 방식이 실무적으로 가장 안정적입니다.

#### 하네스 엔지니어링 필요성 및 대체

- **필요 수준: 중상급**  
  - 상위 모델 비중이 커지면 “실패 비용”이 증가하므로, 재시도/승인/가드레일/샘플링을 더 정교하게 구성해야 합니다.  
  - Agents SDK는 트레이싱과 가드레일 개념을 제공(입·출력 검증)합니다. citeturn18search11turn18search15  
- **대체**  
  - 프라이버시 요구가 강하면: OpenAI API 데이터는 기본적으로 학습에 쓰이지 않는다고 명시되어 있으나(옵트인 제외), “Zero Data Retention” 같은 특수 요구가 있으면 별도 정책/설정이 필요합니다. citeturn13search0turn13search20  
  - Anthropic은 상업용 제품 입력/출력이 기본적으로 학습에 사용되지 않는다고 Privacy Center에 명시합니다. citeturn14search19  

#### 예상 월비용 산정(예시)

**전제(상위 모델 비중 확대)**  
- 월 500 워크플로우 대부분을 GPT-5.4로 처리(저가 대비 품질 우선)  
- Langfuse Core 유지

**비용(대략)**
- LLM: GPT-5.4 기준 약 **$64.5/월**(예시 워크로드 기준) citeturn10view3turn19search28  
- Langfuse Core: **$29/월** citeturn10view5  
- 호스팅(Fly 1GB 유지 가정): **$5.70/월** citeturn10view6  

→ **합계 약 $99.2/월** (고가 구간 충족)

#### 장단점

- 장점:  
  - 추론/코딩/도구 사용 등 복합 작업에서 정답률을 올리기 쉬움(상위 모델 비중). citeturn19search28  
  - 유료 관측/평가로 “좋아졌는지”를 수치로 검증 가능. citeturn10view5turn19search34  
- 단점:  
  - 하네스 품질(루프 제어/승인/비용 통제)이 떨어지면 비용이 즉시 폭주합니다. 이 구간은 “모델”이 아니라 “운영 통제”가 병목입니다.

#### 구현 난이도

- **중상급 ~ 고급**

#### 샘플 기술 스택

- Runtime: Python 3.12  
- Agent loop: OpenAI Agents SDK(핸드오프/가드레일/트레이싱) citeturn18search4turn18search15turn18search11  
- LLM routing: GPT-5.4 ↔ GPT-5.4-mini citeturn10view3turn19search28  
- Observability: Langfuse Cloud Core 또는 Phoenix self-host citeturn10view5turn17search1  

---

### 아키텍처 비교 표

| 항목 | 저가(≤$30) | 중간($31–$70) | 고가($71–$100) |
|---|---|---|---|
| 월비용(예시) | ~$29 | ~$68 | ~$99 |
| 성능(응답 품질) | 중(미니 고정) | 중상(부분 상위) | 상(상위 비중) |
| 지연(주관) | 낮음~중 | 중 | 중~높음(상위 호출 증가) |
| 확장성(병렬성) | 제한적(단일 서비스/간단 워커) | 양호(관측+워커 체계) | 양호(단, 비용 통제 필수) |
| 통합 용이성 | 높음(API 중심) | 높음 + LLM옵스 | 높음 + 운영 통제 강화 |
| 개발 생산성 | 중(관측 수작업 많음) | 높음(실험/리포트 자동) | 중~높음(복잡도↑) |
| 평가·모니터링 | Grafana/OTel 중심 | Langfuse로 체계화 | Langfuse/Phoenix + 강한 게이트 |
| 보안/프라이버시 | 기본 수준(키 관리/로그 샘플링) | 중(로그 정책/샘플링 정교화) | 상(가드레일/승인/ZDR 고려) |
| 운영 복잡도 | 낮음~중 | 중 | 중상~고 |

---

## 평가·모니터링·A/B 및 자동화된 평가 파이프라인 설계

### 평가 지표 설계

멀티에이전트는 “최종 답”만 보면 실패 원인을 못 찾습니다. 최소한 아래를 분리해 측정해야 합니다.

**정량(객관) 지표**
- 성공률: 태스크 완료/오류/타임아웃 비중
- 비용: 워크플로우당 $ (토큰/툴 호출/재시도 포함)
- 지연: end-to-end p50/p95
- 에이전트 효율: 워크플로우당 LLM 호출 횟수, 재시도 횟수, 툴 호출 성공률
- RAG 품질(사용 시): Context Precision, Faithfulness 등  
  - ContextPrecision은 “검색된 컨텍스트가 답변에 유용한지”를 레퍼런스 답과 비교한다고 Ragas 문서에 명시되어 있습니다. citeturn8search0  
  - Faithfulness는 “응답의 주장들이 검색 컨텍스트로 지지되는지”를 0~1로 측정한다고 명시되어 있습니다. citeturn8search11  

**정성(주관) 지표**
- 답변 품질(루브릭 기반): 정답성/완결성/간결성/근거 제시
- 안전성: 규정 위반/민감정보 노출/프롬프트 인젝션 대응
- UX: 사용자가 “바로 실행 가능한 결과”를 받았는지

### 자동 평가 파이프라인 권장 구조

- **오프라인 평가(회귀/리그레션)**
  - openai/evals는 “LLM 또는 LLM 시스템 평가 프레임워크”이며, 커스텀 eval을 작성할 수 있다고 명시합니다. citeturn7search2turn7search6  
  - DeepEval은 “LLM 시스템을 유닛테스트처럼 평가하는 오픈소스 프레임워크”라고 설명합니다. citeturn8search5  
- **온라인 평가(프로덕션)**
  - 트레이싱/로그에서 샘플을 뽑아 루브릭/LLM-judge로 점수화  
  - 모델/프롬프트 버전별 A/B 비교(통계적 유의미성은 최소 표본 확보 후)

아래는 “계획→실행→평가→반복”을 **자동화 파이프라인으로 고정**하는 최소 다이어그램입니다.

```mermaid
flowchart LR
  subgraph Dev["개발/실험"]
    P[프롬프트/정책/라우터 변경] --> V[버전 태깅]
    V --> PR[PR/CI]
  end

  subgraph CI["CI에서 자동 평가"]
    PR --> S[스모크 시나리오 20~50개]
    S --> R{기준 충족?}
    R -- 아니오 --> F[머지 차단/리포트]
    R -- 예 --> M[머지]
  end

  subgraph Prod["프로덕션"]
    M --> D[배포]
    D --> T[트레이싱/로그/비용 수집]
    T --> A[A/B 라우팅]
    A --> O[온라인 점수화(샘플)]
  end

  subgraph Nightly["야간/배치 평가"]
    O --> N[회귀 데이터셋 확장]
    N --> B[배치 실행 + 자동 채점]
    B --> G[리그레션 탐지/원인 분석]
    G --> P
  end
```

### 메트릭 수집 방법(실무형)

- **트레이스 단위**: workflow_id(요청), run_id(실행), agent_id, step_id, tool_name, model_name, 토큰/비용, latency, outcome  
- **로그 샘플링**:  
  - 비용대 중간/고가에서 특히 중요(로그 과다 수집은 과금/저장/분석 비용을 올림). Langfuse는 units가 Traces+Observations+Scores로 합산된다고 명시합니다. citeturn7search28turn7search36  
- **프롬프트 캐시 적중률**: 캐싱이 깨지면 비용이 바로 상승하므로 “prefix 안정성”을 지표로 둡니다. OpenAI는 캐싱이 자동 동작하며 비용/지연을 크게 줄일 수 있다고 명시합니다. citeturn18search3  

---

## 구현 로드맵과 리스크 완화

### 구현 로드맵

아래는 “저가 아키텍처로 시작 → 중간/고가로 확장”을 전제로 한 12주 로드맵입니다.

- **1–2주차: 최소 워크플로우 완성**
  - 단일 오케스트레이터 + 2개 서브에이전트(리서치/리라이트)로 고정
  - workflow_id, 상태 저장, 툴 호출 래퍼, 타임아웃/재시도 1회 제한
  - 프롬프트 prefix 고정(캐시 친화)
- **3–4주차: 관측·비용 집계**
  - 트레이싱/로그 스키마 확정 + 대시보드 1차(비용/지연/실패율)
  - 프롬프트 캐싱 적중률과 호출 수 KPI를 추가(비용 통제용) citeturn18search3turn10view3  
- **5–6주차: 평가 데이터셋과 회귀 테스트 도입**
  - 시나리오 50~100개를 JSONL로 관리
  - openai/evals 또는 DeepEval로 CI 회귀 테스트 구성 citeturn7search2turn8search5  
- **7–8주차: A/B 라우팅**
  - 프롬프트/모델 버전 2개로 A/B  
  - 지표: 성공률/비용/지연/LLM-judge 점수
- **9–10주차: 비동기 워커/배치 평가**
  - 야간 배치로 리그레션 200~500개 실행
  - Batch 할인 적용(가능한 작업은 비동기로 전환) citeturn10view3turn21view0  
- **11–12주차: 운영 안전장치**
  - 가드레일(입·출력 검증) 및 위험 툴 승인(수동/정책 기반)  
  - 실패 모드별 플레이북(레이트리밋, 외부 API 실패, 검색 실패 등)

### 주요 리스크와 완화책

- **비용 폭주(가장 흔함)**  
  - 완화: 호출 수 상한(워크플로우당 최대 N회), 재시도 1회 제한, 상위 모델 비중 상한, 배치 전환, 캐시 prefix 안정화 citeturn18search3turn10view3  
- **품질 퇴행(프롬프트 수정 후 망가짐)**  
  - 완화: PR 스모크 eval + 야간 회귀 eval(데이터셋 기반). Evals는 변동성을 다루기 위한 필수 장치라고 명시됩니다. citeturn19search34turn7search2  
- **관측 과다로 인한 과금/저장 문제**  
  - 완화: 샘플링, 요약 로그(핵심 필드만), 실패 케이스 100% 보존 정책  
- **데이터 프라이버시/학습 사용 우려**  
  - entity["company","Mistral AI","ai company france"]: 입력/출력 데이터가 학습에 사용될 수 있으며 옵트아웃 가능, 일부 플랜은 기본 옵트아웃이라고 Help Center에 명시되어 있습니다. citeturn20view3  
  - OpenAI: API 데이터는 기본적으로 학습에 사용되지 않는다고 명시(옵트인 제외). citeturn13search0  
  - Anthropic: 상업용 제품 입력/출력은 기본적으로 학습에 사용되지 않는다고 Privacy Center에 명시. citeturn14search19  
  - 완화: PII 마스킹/토큰화, 로그 최소화, 필요 시 self-host 관측(Phoenix) citeturn17search1  
- **운영 복잡도 증가(자체 하네스/자체 관측 스택)**  
  - 완화: 초기엔 SDK/관리형(Langfuse Core)로 시작하고, 정말 필요할 때만 self-host로 이동. Langfuse는 self-host가 무료(MIT)라고 명시합니다. citeturn15search14turn10view5  

---
