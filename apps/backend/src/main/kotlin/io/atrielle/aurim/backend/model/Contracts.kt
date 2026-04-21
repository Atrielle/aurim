package io.atrielle.aurim.backend.model

import com.fasterxml.jackson.annotation.JsonIgnore
import jakarta.validation.constraints.AssertTrue
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Pattern
import jakarta.validation.constraints.Size
import java.time.OffsetDateTime

private const val SLUG_PATTERN = "^[a-z0-9]+(?:-[a-z0-9]+)*$"
private const val UUID_PATTERN = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
private const val WORKSPACE_STATUS_PATTERN = "^(active|archived|deleted)$"
private const val GIT_PROVIDER_PATTERN = "^(github|gitlab|bitbucket|generic)$"
private const val GIT_CONNECTION_STATUS_PATTERN = "^(connected|disconnected|error|archived)$"
private const val FACTORY_SPEC_STATUS_PATTERN = "^(draft|reviewed|approved|superseded)$"
private const val FACTORY_RUN_STATUS_PATTERN = "^(created|planned|running|blocked|closed)$"
private const val FACTORY_ARTIFACT_TYPE_PATTERN = "^(spec_snapshot|sprint_contract|planner_report|generator_report|evaluator_report|diff|log|trace)$"
private const val FACTORY_EVALUATION_RESULT_PATTERN = "^(PASS|FAIL)$"
private const val URI_PATTERN = "^[a-zA-Z][a-zA-Z0-9+.-]*://.+$"

data class HealthResponse(
    val status: String,
    val service: String,
    val timestamp: OffsetDateTime,
)

data class ItemsResponse<T>(
    val items: List<T>,
)

data class Workspace(
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:Pattern(regexp = SLUG_PATTERN)
    val slug: String,
    @field:Size(min = 1, max = 120)
    val name: String,
    @field:Pattern(regexp = WORKSPACE_STATUS_PATTERN)
    val status: String,
    val created_at: OffsetDateTime,
    @field:Size(min = 1, max = 120)
    val created_by: String,
    val updated_at: OffsetDateTime,
)

data class CreateWorkspaceRequest(
    @field:Pattern(regexp = SLUG_PATTERN)
    val slug: String,
    @field:NotBlank
    @field:Size(max = 120)
    val name: String,
    @field:NotBlank
    @field:Size(max = 120)
    val created_by: String,
)

data class UpdateWorkspaceRequest(
    @field:Size(min = 1, max = 120)
    val name: String? = null,
    @field:Pattern(regexp = WORKSPACE_STATUS_PATTERN)
    val status: String? = null,
) {
    @get:JsonIgnore
    @get:AssertTrue(message = "At least one workspace field must be provided.")
    val hasUpdates: Boolean
        get() = name != null || status != null
}

data class GitWorkspace(
    @field:Pattern(regexp = UUID_PATTERN)
    val git_workspace_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:Pattern(regexp = GIT_PROVIDER_PATTERN)
    val provider: String,
    @field:Pattern(regexp = URI_PATTERN)
    val repository_url: String,
    @field:NotBlank
    @field:Size(max = 255)
    val default_branch: String,
    @field:Pattern(regexp = GIT_CONNECTION_STATUS_PATTERN)
    val connection_status: String,
    val created_at: OffsetDateTime,
    @field:Size(min = 1, max = 120)
    val created_by: String,
)

data class CreateGitWorkspaceRequest(
    @field:Pattern(regexp = GIT_PROVIDER_PATTERN)
    val provider: String,
    @field:Pattern(regexp = URI_PATTERN)
    val repository_url: String,
    @field:NotBlank
    @field:Size(max = 255)
    val default_branch: String,
    @field:NotBlank
    @field:Size(max = 120)
    val created_by: String,
)

data class UpdateGitWorkspaceRequest(
    @field:Size(min = 1, max = 255)
    val default_branch: String? = null,
    @field:Pattern(regexp = GIT_CONNECTION_STATUS_PATTERN)
    val connection_status: String? = null,
) {
    @get:JsonIgnore
    @get:AssertTrue(message = "At least one git workspace field must be provided.")
    val hasUpdates: Boolean
        get() = default_branch != null || connection_status != null
}

data class FactorySpec(
    @field:Pattern(regexp = UUID_PATTERN)
    val factory_spec_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:NotBlank
    @field:Size(max = 160)
    val title: String,
    @field:NotBlank
    @field:Size(max = 280)
    val summary: String,
    @field:NotBlank
    val problem_statement: String,
    @field:NotBlank
    val goal: String,
    @field:Size(min = 1)
    val non_negotiable_constraints: List<String>,
    @field:Size(min = 1)
    val initial_scope: List<String>,
    val excluded_scope: List<String>,
    @field:NotBlank
    val acceptance_standard: String,
    @field:Pattern(regexp = FACTORY_SPEC_STATUS_PATTERN)
    val status: String,
    val created_at: OffsetDateTime,
    @field:Size(min = 1, max = 120)
    val created_by: String,
)

data class CreateFactorySpecRequest(
    @field:NotBlank
    @field:Size(max = 160)
    val title: String,
    @field:NotBlank
    @field:Size(max = 280)
    val summary: String,
    @field:NotBlank
    val problem_statement: String,
    @field:NotBlank
    val goal: String,
    @field:Size(min = 1)
    val non_negotiable_constraints: List<@NotBlank String>,
    @field:Size(min = 1)
    val initial_scope: List<@NotBlank String>,
    val excluded_scope: List<String> = emptyList(),
    @field:NotBlank
    val acceptance_standard: String,
    @field:NotBlank
    @field:Size(max = 120)
    val created_by: String,
)

data class UpdateFactorySpecRequest(
    @field:Size(min = 1, max = 160)
    val title: String? = null,
    @field:Size(min = 1, max = 280)
    val summary: String? = null,
    @field:Size(min = 1)
    val problem_statement: String? = null,
    @field:Size(min = 1)
    val goal: String? = null,
    @field:Size(min = 1)
    val non_negotiable_constraints: List<@NotBlank String>? = null,
    @field:Size(min = 1)
    val initial_scope: List<@NotBlank String>? = null,
    val excluded_scope: List<@NotBlank String>? = null,
    @field:Size(min = 1)
    val acceptance_standard: String? = null,
    @field:Pattern(regexp = FACTORY_SPEC_STATUS_PATTERN)
    val status: String? = null,
) {
    @get:JsonIgnore
    @get:AssertTrue(message = "At least one factory spec field must be provided.")
    val hasUpdates: Boolean
        get() = listOf(
            title,
            summary,
            problem_statement,
            goal,
            acceptance_standard,
            status,
        ).any { it != null } ||
            non_negotiable_constraints != null ||
            initial_scope != null ||
            excluded_scope != null
}

data class FactoryRun(
    @field:Pattern(regexp = UUID_PATTERN)
    val factory_run_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val factory_spec_id: String,
    @field:Pattern(regexp = FACTORY_RUN_STATUS_PATTERN)
    val status: String,
    @field:NotBlank
    val planner_prompt_ref: String,
    @field:NotBlank
    val generator_prompt_ref: String,
    @field:NotBlank
    val evaluator_prompt_ref: String,
    @field:NotBlank
    val contract_snapshot_ref: String,
    @field:NotBlank
    val artifact_root_ref: String,
    val touched_paths: List<String>,
    val created_at: OffsetDateTime,
    @field:Size(min = 1, max = 120)
    val created_by: String,
)

data class CreateFactoryRunRequest(
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val factory_spec_id: String,
    @field:NotBlank
    val planner_prompt_ref: String,
    @field:NotBlank
    val generator_prompt_ref: String,
    @field:NotBlank
    val evaluator_prompt_ref: String,
    @field:NotBlank
    val contract_snapshot_ref: String,
    @field:NotBlank
    val artifact_root_ref: String,
    val touched_paths: List<@NotBlank String> = emptyList(),
    @field:NotBlank
    @field:Size(max = 120)
    val created_by: String,
)

data class CloseFactoryRunRequest(
    @field:Pattern(regexp = FACTORY_EVALUATION_RESULT_PATTERN)
    val evaluation_result: String,
    @field:NotBlank
    @field:Size(max = 120)
    val closed_by: String,
)

data class FactoryArtifact(
    @field:Pattern(regexp = UUID_PATTERN)
    val factory_artifact_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val factory_run_id: String,
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:Pattern(regexp = FACTORY_ARTIFACT_TYPE_PATTERN)
    val artifact_type: String,
    @field:NotBlank
    @field:Size(max = 160)
    val name: String,
    @field:NotBlank
    val content_ref: String,
    @field:NotBlank
    @field:Size(max = 255)
    val checksum: String,
    val created_at: OffsetDateTime,
    @field:Size(min = 1, max = 120)
    val created_by: String,
)

data class CreateFactoryArtifactRequest(
    @field:Pattern(regexp = UUID_PATTERN)
    val workspace_id: String,
    @field:Pattern(regexp = FACTORY_ARTIFACT_TYPE_PATTERN)
    val artifact_type: String,
    @field:NotBlank
    @field:Size(max = 160)
    val name: String,
    @field:NotBlank
    val content_ref: String,
    @field:NotBlank
    @field:Size(max = 255)
    val checksum: String,
    @field:NotBlank
    @field:Size(max = 120)
    val created_by: String,
)
