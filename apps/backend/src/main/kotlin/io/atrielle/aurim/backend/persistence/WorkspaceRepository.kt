package io.atrielle.aurim.backend.persistence

import io.atrielle.aurim.backend.model.Workspace
import java.time.OffsetDateTime
import java.util.UUID
import kotlinx.coroutines.reactor.awaitSingle
import kotlinx.coroutines.reactor.awaitSingleOrNull
import org.springframework.r2dbc.core.DatabaseClient
import org.springframework.stereotype.Repository

@Repository
class WorkspaceRepository(
    private val databaseClient: DatabaseClient,
) {

    suspend fun create(
        workspaceId: UUID,
        slug: String,
        name: String,
        status: String,
        createdAt: OffsetDateTime,
        createdBy: String,
        updatedAt: OffsetDateTime,
    ): Workspace {
        databaseClient
            .sql(
                """
                insert into workspace (
                    workspace_id,
                    slug,
                    name,
                    status,
                    created_at,
                    created_by,
                    updated_at
                ) values (
                    :workspace_id,
                    :slug,
                    :name,
                    :status,
                    :created_at,
                    :created_by,
                    :updated_at
                )
                """.trimIndent(),
            )
            .bind("workspace_id", workspaceId)
            .bind("slug", slug)
            .bind("name", name)
            .bind("status", status)
            .bind("created_at", createdAt)
            .bind("created_by", createdBy)
            .bind("updated_at", updatedAt)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(workspaceId.toString())!!
    }

    suspend fun list(): List<Workspace> =
        databaseClient
            .sql(
                """
                select workspace_id, slug, name, status, created_at, created_by, updated_at
                from workspace
                order by created_at desc
                """.trimIndent(),
            )
            .map { row, _ -> row.toWorkspace() }
            .all()
            .collectList()
            .awaitSingle()

    suspend fun findById(workspaceId: String): Workspace? =
        databaseClient
            .sql(
                """
                select workspace_id, slug, name, status, created_at, created_by, updated_at
                from workspace
                where workspace_id = :workspace_id
                """.trimIndent(),
            )
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .map { row, _ -> row.toWorkspace() }
            .one()
            .awaitSingleOrNull()

    suspend fun update(workspace: Workspace): Workspace {
        databaseClient
            .sql(
                """
                update workspace
                set name = :name,
                    status = :status,
                    updated_at = :updated_at
                where workspace_id = :workspace_id
                """.trimIndent(),
            )
            .bind("workspace_id", parseUuid(workspace.workspace_id, "workspace_id"))
            .bind("name", workspace.name)
            .bind("status", workspace.status)
            .bind("updated_at", workspace.updated_at)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(workspace.workspace_id)!!
    }
}

private fun io.r2dbc.spi.Row.toWorkspace(): Workspace =
    Workspace(
        workspace_id = requiredUuid("workspace_id").toString(),
        slug = requiredString("slug"),
        name = requiredString("name"),
        status = requiredString("status"),
        created_at = requiredOffsetDateTime("created_at"),
        created_by = requiredString("created_by"),
        updated_at = requiredOffsetDateTime("updated_at"),
    )
