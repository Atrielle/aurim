package io.atrielle.aurim.backend.model

import java.time.OffsetDateTime

data class HealthResponse(
    val status: String,
    val service: String,
    val timestamp: OffsetDateTime,
)

data class ItemsResponse<T>(
    val items: List<T>,
)

data class Workspace(
    val workspace_id: String,
    val slug: String,
    val name: String,
    val status: String,
    val created_at: OffsetDateTime,
    val created_by: String,
    val updated_at: OffsetDateTime,
)

data class CreateWorkspaceRequest(
    val slug: String,
    val name: String,
    val created_by: String,
)

data class UpdateWorkspaceRequest(
    val name: String? = null,
    val status: String? = null,
)

data class GitWorkspace(
    val git_workspace_id: String,
    val workspace_id: String,
    val provider: String,
    val repository_url: String,
    val default_branch: String,
    val connection_status: String,
    val created_at: OffsetDateTime,
    val created_by: String,
)

data class CreateGitWorkspaceRequest(
    val provider: String,
    val repository_url: String,
    val default_branch: String,
    val created_by: String,
)

data class UpdateGitWorkspaceRequest(
    val default_branch: String? = null,
    val connection_status: String? = null,
)

data class FactorySpec(
    val factory_spec_id: String,
    val workspace_id: String,
    val title: String,
    val summary: String,
    val problem_statement: String,
    val goal: String,
    val non_negotiable_constraints: List<String>,
    val initial_scope: List<String>,
    val excluded_scope: List<String>,
    val acceptance_standard: String,
    val status: String,
    val created_at: OffsetDateTime,
    val created_by: String,
)

data class CreateFactorySpecRequest(
    val title: String,
    val summary: String,
    val problem_statement: String,
    val goal: String,
    val non_negotiable_constraints: List<String>,
    val initial_scope: List<String>,
    val excluded_scope: List<String> = emptyList(),
    val acceptance_standard: String,
    val created_by: String,
)

data class UpdateFactorySpecRequest(
    val title: String? = null,
    val summary: String? = null,
    val problem_statement: String? = null,
    val goal: String? = null,
    val non_negotiable_constraints: List<String>? = null,
    val initial_scope: List<String>? = null,
    val excluded_scope: List<String>? = null,
    val acceptance_standard: String? = null,
    val status: String? = null,
)

data class FactoryRun(
    val factory_run_id: String,
    val workspace_id: String,
    val factory_spec_id: String,
    val status: String,
    val planner_prompt_ref: String,
    val generator_prompt_ref: String,
    val evaluator_prompt_ref: String,
    val contract_snapshot_ref: String,
    val artifact_root_ref: String,
    val touched_paths: List<String>,
    val created_at: OffsetDateTime,
    val created_by: String,
)

data class CreateFactoryRunRequest(
    val workspace_id: String,
    val factory_spec_id: String,
    val planner_prompt_ref: String,
    val generator_prompt_ref: String,
    val evaluator_prompt_ref: String,
    val contract_snapshot_ref: String,
    val artifact_root_ref: String,
    val touched_paths: List<String> = emptyList(),
    val created_by: String,
)

data class CloseFactoryRunRequest(
    val evaluation_result: String,
    val closed_by: String,
)

data class FactoryArtifact(
    val factory_artifact_id: String,
    val factory_run_id: String,
    val workspace_id: String,
    val artifact_type: String,
    val name: String,
    val content_ref: String,
    val checksum: String,
    val created_at: OffsetDateTime,
    val created_by: String,
)

data class CreateFactoryArtifactRequest(
    val workspace_id: String,
    val artifact_type: String,
    val name: String,
    val content_ref: String,
    val checksum: String,
    val created_by: String,
)
