create table if not exists workspace (
    workspace_id uuid primary key,
    slug text not null unique,
    name text not null,
    status text not null check (status in ('active', 'archived', 'deleted')),
    created_at timestamptz not null,
    created_by text not null,
    updated_at timestamptz not null
);

create table if not exists git_workspace (
    git_workspace_id uuid primary key,
    workspace_id uuid not null references workspace(workspace_id),
    provider text not null check (provider in ('github', 'gitlab', 'bitbucket', 'generic')),
    repository_url text not null,
    default_branch text not null,
    connection_status text not null check (connection_status in ('connected', 'disconnected', 'error', 'archived')),
    created_at timestamptz not null,
    created_by text not null
);

create table if not exists factory_spec (
    factory_spec_id uuid primary key,
    workspace_id uuid not null references workspace(workspace_id),
    title text not null,
    summary text not null,
    problem_statement text not null,
    goal text not null,
    non_negotiable_constraints_json text not null,
    initial_scope_json text not null,
    excluded_scope_json text not null,
    acceptance_standard text not null,
    status text not null check (status in ('draft', 'reviewed', 'approved', 'superseded')),
    created_at timestamptz not null,
    created_by text not null
);

create table if not exists factory_run (
    factory_run_id uuid primary key,
    workspace_id uuid not null references workspace(workspace_id),
    factory_spec_id uuid not null references factory_spec(factory_spec_id),
    status text not null check (status in ('created', 'planned', 'running', 'blocked', 'passed', 'failed', 'closed')),
    planner_prompt_ref text not null,
    generator_prompt_ref text not null,
    evaluator_prompt_ref text not null,
    contract_snapshot_ref text not null,
    artifact_root_ref text not null,
    touched_paths_json text not null,
    created_at timestamptz not null,
    created_by text not null,
    closed_at timestamptz null,
    closed_by text null
);

create table if not exists factory_artifact (
    factory_artifact_id uuid primary key,
    factory_run_id uuid not null references factory_run(factory_run_id),
    workspace_id uuid not null references workspace(workspace_id),
    artifact_type text not null check (
        artifact_type in (
            'spec_snapshot',
            'sprint_contract',
            'planner_report',
            'generator_report',
            'evaluator_report',
            'diff',
            'log',
            'trace'
        )
    ),
    name text not null,
    content_ref text not null,
    checksum text not null,
    created_at timestamptz not null,
    created_by text not null
);

create index if not exists idx_git_workspace_workspace_id on git_workspace(workspace_id);
create index if not exists idx_factory_spec_workspace_id on factory_spec(workspace_id);
create index if not exists idx_factory_run_workspace_id on factory_run(workspace_id);
create index if not exists idx_factory_run_factory_spec_id on factory_run(factory_spec_id);
create index if not exists idx_factory_artifact_factory_run_id on factory_artifact(factory_run_id);
