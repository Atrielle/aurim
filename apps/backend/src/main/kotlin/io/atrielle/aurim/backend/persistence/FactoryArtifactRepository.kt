package io.atrielle.aurim.backend.persistence

import io.atrielle.aurim.backend.model.FactoryArtifact
import java.time.OffsetDateTime
import java.util.UUID
import kotlinx.coroutines.reactor.awaitSingle
import kotlinx.coroutines.reactor.awaitSingleOrNull
import org.springframework.r2dbc.core.DatabaseClient
import org.springframework.stereotype.Repository

@Repository
class FactoryArtifactRepository(
    private val databaseClient: DatabaseClient,
) {

    suspend fun create(
        factoryArtifactId: UUID,
        factoryRunId: String,
        workspaceId: String,
        artifactType: String,
        name: String,
        contentRef: String,
        checksum: String,
        createdAt: OffsetDateTime,
        createdBy: String,
    ): FactoryArtifact {
        databaseClient
            .sql(
                """
                insert into factory_artifact (
                    factory_artifact_id,
                    factory_run_id,
                    workspace_id,
                    artifact_type,
                    name,
                    content_ref,
                    checksum,
                    created_at,
                    created_by
                ) values (
                    :factory_artifact_id,
                    :factory_run_id,
                    :workspace_id,
                    :artifact_type,
                    :name,
                    :content_ref,
                    :checksum,
                    :created_at,
                    :created_by
                )
                """.trimIndent(),
            )
            .bind("factory_artifact_id", factoryArtifactId)
            .bind("factory_run_id", parseUuid(factoryRunId, "factory_run_id"))
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .bind("artifact_type", artifactType)
            .bind("name", name)
            .bind("content_ref", contentRef)
            .bind("checksum", checksum)
            .bind("created_at", createdAt)
            .bind("created_by", createdBy)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(factoryArtifactId.toString())!!
    }

    suspend fun listByFactoryRunId(factoryRunId: String): List<FactoryArtifact> =
        databaseClient
            .sql(
                """
                select factory_artifact_id, factory_run_id, workspace_id, artifact_type, name,
                       content_ref, checksum, created_at, created_by
                from factory_artifact
                where factory_run_id = :factory_run_id
                order by created_at desc
                """.trimIndent(),
            )
            .bind("factory_run_id", parseUuid(factoryRunId, "factory_run_id"))
            .map { row, _ -> row.toFactoryArtifact() }
            .all()
            .collectList()
            .awaitSingle()

    suspend fun findById(factoryArtifactId: String): FactoryArtifact? =
        databaseClient
            .sql(
                """
                select factory_artifact_id, factory_run_id, workspace_id, artifact_type, name,
                       content_ref, checksum, created_at, created_by
                from factory_artifact
                where factory_artifact_id = :factory_artifact_id
                """.trimIndent(),
            )
            .bind("factory_artifact_id", parseUuid(factoryArtifactId, "factory_artifact_id"))
            .map { row, _ -> row.toFactoryArtifact() }
            .one()
            .awaitSingleOrNull()
}

private fun io.r2dbc.spi.Row.toFactoryArtifact(): FactoryArtifact =
    FactoryArtifact(
        factory_artifact_id = requiredUuid("factory_artifact_id").toString(),
        factory_run_id = requiredUuid("factory_run_id").toString(),
        workspace_id = requiredUuid("workspace_id").toString(),
        artifact_type = requiredString("artifact_type"),
        name = requiredString("name"),
        content_ref = requiredString("content_ref"),
        checksum = requiredString("checksum"),
        created_at = requiredOffsetDateTime("created_at"),
        created_by = requiredString("created_by"),
    )
