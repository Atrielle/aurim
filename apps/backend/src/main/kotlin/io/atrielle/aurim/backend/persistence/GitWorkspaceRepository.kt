package io.atrielle.aurim.backend.persistence

import io.atrielle.aurim.backend.model.GitWorkspace
import java.time.OffsetDateTime
import java.util.UUID
import kotlinx.coroutines.reactor.awaitSingle
import kotlinx.coroutines.reactor.awaitSingleOrNull
import org.springframework.r2dbc.core.DatabaseClient
import org.springframework.stereotype.Repository

@Repository
class GitWorkspaceRepository(
    private val databaseClient: DatabaseClient,
) {

    suspend fun create(
        gitWorkspaceId: UUID,
        workspaceId: String,
        provider: String,
        repositoryUrl: String,
        defaultBranch: String,
        connectionStatus: String,
        createdAt: OffsetDateTime,
        createdBy: String,
    ): GitWorkspace {
        databaseClient
            .sql(
                """
                insert into git_workspace (
                    git_workspace_id,
                    workspace_id,
                    provider,
                    repository_url,
                    default_branch,
                    connection_status,
                    created_at,
                    created_by
                ) values (
                    :git_workspace_id,
                    :workspace_id,
                    :provider,
                    :repository_url,
                    :default_branch,
                    :connection_status,
                    :created_at,
                    :created_by
                )
                """.trimIndent(),
            )
            .bind("git_workspace_id", gitWorkspaceId)
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .bind("provider", provider)
            .bind("repository_url", repositoryUrl)
            .bind("default_branch", defaultBranch)
            .bind("connection_status", connectionStatus)
            .bind("created_at", createdAt)
            .bind("created_by", createdBy)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(gitWorkspaceId.toString())!!
    }

    suspend fun listByWorkspaceId(workspaceId: String): List<GitWorkspace> =
        databaseClient
            .sql(
                """
                select git_workspace_id, workspace_id, provider, repository_url, default_branch, connection_status, created_at, created_by
                from git_workspace
                where workspace_id = :workspace_id
                order by created_at desc
                """.trimIndent(),
            )
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .map { row, _ -> row.toGitWorkspace() }
            .all()
            .collectList()
            .awaitSingle()

    suspend fun findById(gitWorkspaceId: String): GitWorkspace? =
        databaseClient
            .sql(
                """
                select git_workspace_id, workspace_id, provider, repository_url, default_branch, connection_status, created_at, created_by
                from git_workspace
                where git_workspace_id = :git_workspace_id
                """.trimIndent(),
            )
            .bind("git_workspace_id", parseUuid(gitWorkspaceId, "git_workspace_id"))
            .map { row, _ -> row.toGitWorkspace() }
            .one()
            .awaitSingleOrNull()

    suspend fun update(gitWorkspace: GitWorkspace): GitWorkspace {
        databaseClient
            .sql(
                """
                update git_workspace
                set default_branch = :default_branch,
                    connection_status = :connection_status
                where git_workspace_id = :git_workspace_id
                """.trimIndent(),
            )
            .bind("git_workspace_id", parseUuid(gitWorkspace.git_workspace_id, "git_workspace_id"))
            .bind("default_branch", gitWorkspace.default_branch)
            .bind("connection_status", gitWorkspace.connection_status)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(gitWorkspace.git_workspace_id)!!
    }
}

private fun io.r2dbc.spi.Row.toGitWorkspace(): GitWorkspace =
    GitWorkspace(
        git_workspace_id = requiredUuid("git_workspace_id").toString(),
        workspace_id = requiredUuid("workspace_id").toString(),
        provider = requiredString("provider"),
        repository_url = requiredString("repository_url"),
        default_branch = requiredString("default_branch"),
        connection_status = requiredString("connection_status"),
        created_at = requiredOffsetDateTime("created_at"),
        created_by = requiredString("created_by"),
    )
