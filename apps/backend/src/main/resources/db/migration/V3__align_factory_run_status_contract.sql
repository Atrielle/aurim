alter table factory_run
drop constraint if exists factory_run_status_check;

alter table factory_run
add constraint factory_run_status_check
check (status in ('created', 'planned', 'running', 'blocked', 'closed'));
