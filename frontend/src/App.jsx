const nav = ['Overview', 'Work Items', 'Docs', 'Files', 'Activity', 'Harness'];

const workItems = [
  { id: 'WIT-101', title: 'Freeze API contracts', status: 'In Review' },
  { id: 'WIT-102', title: 'Build shell layout', status: 'In Progress' },
  { id: 'WIT-103', title: 'Model revision policy', status: 'Todo' },
];

export default function App() {
  return (
    <div className="app">
      <aside className="rail">
        <div className="brand">
          <div className="brand-mark">SZ</div>
          <div>
            <strong>Syszone Frontend</strong>
            <span>Product shell baseline</span>
          </div>
        </div>

        <nav className="nav">
          {nav.map((item, index) => (
            <button key={item} className={`nav-item${index === 0 ? ' active' : ''}`} type="button">
              {item}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main">
        <header className="hero">
          <div>
            <span className="eyebrow">Frontend Codebase</span>
            <h1>Product Shell Before Feature Work</h1>
            <p>
              이 프런트 코드는 하네스가 생성한 스프린트 계약을 받아 실제 제품 UI를 구현하는 코드베이스다.
              지금은 도메인 셸과 정보구조만 고정해 둔다.
            </p>
          </div>
          <div className="hero-card">
            <span>Next expected input</span>
            <strong>harness/artifacts/runs/*/01_sprint_contract.md</strong>
          </div>
        </header>

        <section className="grid">
          <article className="panel panel-wide">
            <h2>Frontend Boundaries</h2>
            <ul>
              <li>UI shell, routing, layout, and interaction states live here.</li>
              <li>Domain contracts come from backend and harness artifacts, not ad-hoc UI guesses.</li>
              <li>No sprint is considered complete until evaluator approval exists in harness artifacts.</li>
            </ul>
          </article>

          <article className="panel">
            <h2>Current Surface</h2>
            <div className="chips">
              <span>Workspace shell</span>
              <span>Work item views</span>
              <span>Document surface</span>
              <span>File surface</span>
            </div>
          </article>

          <article className="panel panel-wide">
            <h2>Example Work Queue</h2>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {workItems.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.title}</td>
                    <td>{item.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </article>

          <article className="panel">
            <h2>Harness Rule</h2>
            <p>
              프런트 변경은 반드시 스프린트 계약의 acceptance criteria와 touched paths 범위 안에서만 진행한다.
            </p>
          </article>
        </section>
      </main>
    </div>
  );
}
