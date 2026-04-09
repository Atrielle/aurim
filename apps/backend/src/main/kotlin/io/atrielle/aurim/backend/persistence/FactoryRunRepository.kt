package io.atrielle.aurim.backend.persistence

import io.atrielle.aurim.backend.model.FactoryRun
import java.time.OffsetDateTime
import java.util.UUID
import kotlinx.coroutines.reactor.awaitSingle
import kotlinx.coroutines.reactor.awaitSingleOrNull
import org.springframework.r2dbc.core.DatabaseClient
import org.springframework.stereotype.Repository

@Repository
class FactoryRunRepository(
    private val databaseClient: DatabaseClient,
    private val jsonListCodec: JsonListCodec,
) {

    suspend fun create(
        factoryRunId: UUID,
        workspaceId: String,
        factorySpecId: String,
        status: String,
        plannerPromptRef: String,
        generatorPromptRef: String,
        evaluatorPromptRef: String,
        contractSnapshotRef: String,
        artifactRootRef: String,
        touchedPaths: List<String>,
        createdAt: OffsetDateTime,
        createdBy: String,
    ): FactoryRun {
        databaseClient
            .sql(
                """
                insert into factory_run (
                    factory_run_id,
                    workspace_id,
                    factory_spec_id,
                    status,
                    planner_prompt_ref,
                    generator_prompt_ref,
                    evaluator_prompt_ref,
                    contract_snapshot_ref,
                    artifact_root_ref,
                    touched_paths_json,
                    created_at,
                    created_by
                ) values (
                    :factory_run_id,
                    :workspace_id,
                    :factory_spec_id,
                    :status,
                    :planner_prompt_ref,
                    :generator_prompt_ref,
                    :evaluator_prompt_ref,
                    :contract_snapshot_ref,
                    :artifact_root_ref,
                    :touched_paths_json,
                    :created_at,
                    :created_by
                )
                """.trimIndent(),
            )
            .bind("factory_run_id", factoryRunId)
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .bind("factory_spec_id", parseUuid(factorySpecId, "factory_spec_id"))
            .bind("status", status)
            .bind("planner_prompt_ref", plannerPromptRef)
            .bind("generator_prompt_ref", generatorPromptRef)
            .bind("evaluator_prompt_ref", evaluatorPromptRef)
            .bind("contract_snapshot_ref", contractSnapshotRef)
            .bind("artifact_root_ref", artifactRootRef)
            .bind("touched_paths_json", jsonListCodec.encode(touchedPaths))
            .bind("created_at", createdAt)
            .bind("created_by", createdBy)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(factoryRunId.toString())!!
    }

    suspend fun listByWorkspaceId(workspaceId: String): List<FactoryRun> =
        databaseClient
            .sql(
                """
                select factory_run_id, workspace_id, factory_spec_id, status, planner_prompt_ref,
                       generator_prompt_ref, evaluator_prompt_ref, contract_snapshot_ref,
                       artifact_root_ref, touched_paths_json, created_at, created_by
                from factory_run
                where workspace_id = :workspace_id
                order by created_at desc
                """.trimIndent(),
            )
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .map { row, _ -> row.toFactoryRun(jsonListCodec) }
            .all()
            .collectList()
            .awaitSingle()

    suspend fun findById(factoryRunId: String): FactoryRun? =
        databaseClient
            .sql(
                """
                select factory_run_id, workspace_id, factory_spec_id, status, planner_prompt_ref,
                       generator_prompt_ref, evaluator_prompt_ref, contract_snapshot_ref,
                       artifact_root_ref, touched_paths_json, created_at, created_by
                from factory_run
                where factory_run_id = :factory_run_id
                """.trimIndent(),
            )
            .bind("factory_run_id", parseUuid(factoryRunId, "factory_run_id"))
            .map { row, _ -> row.toFactoryRun(jsonListCodec) }
            .one()
            .awaitSingleOrNull()

    suspend fun update(
        factoryRun: FactoryRun,
        closedAt: OffsetDateTime? = null,
        closedBy: String? = null,
    ): FactoryRun {
        var statement = databaseClient
            .sql(
                """
                update factory_run
                set status = :status,
                    planner_prompt_ref = :planner_prompt_ref,
                    generator_prompt_ref = :generator_prompt_ref,
                    evaluator_prompt_ref = :evaluator_prompt_ref,
                    contract_snapshot_ref = :contract_snapshot_ref,
                    artifact_root_ref = :artifact_root_ref,
                    touched_paths_json = :touched_paths_json,
                    closed_at = :closed_at,
                    closed_by = :closed_by
                where factory_run_id = :factory_run_id
                """.trimIndent(),
            )
            .bind("factory_run_id", parseUuid(factoryRun.factory_run_id, "factory_run_id"))
            .bind("status", factoryRun.status)
            .bind("planner_prompt_ref", factoryRun.planner_prompt_ref)
            .bind("generator_prompt_ref", factoryRun.generator_prompt_ref)
            .bind("evaluator_prompt_ref", factoryRun.evaluator_prompt_ref)
            .bind("contract_snapshot_ref", factoryRun.contract_snapshot_ref)
            .bind("artifact_root_ref", factoryRun.artifact_root_ref)
            .bind("touched_paths_json", jsonListCodec.encode(factoryRun.touched_paths))

        statement =
            if (closedAt == null) {
                statement.bindNull("closed_at", OffsetDateTime::class.java)
            } else {
                statement.bind("closed_at", closedAt)
            }

        statement =
            if (closedBy == null) {
                statement.bindNull("closed_by", String::class.java)
            } else {
                statement.bind("closed_by", closedBy)
            }

        statement.fetch().rowsUpdated().awaitSingle()

        return findById(factoryRun.factory_run_id)!!
    }
}

private fun io.r2dbc.spi.Row.toFactoryRun(jsonListCodec: JsonListCodec): FactoryRun =
    FactoryRun(
        factory_run_id = requiredUuid("factory_run_id").toString(),
        workspace_id = requiredUuid("workspace_id").toString(),
        factory_spec_id = requiredUuid("factory_spec_id").toString(),
        status = requiredString("status"),
        planner_prompt_ref = requiredString("planner_prompt_ref"),
        generator_prompt_ref = requiredString("generator_prompt_ref"),
        evaluator_prompt_ref = requiredString("evaluator_prompt_ref"),
        contract_snapshot_ref = requiredString("contract_snapshot_ref"),
        artifact_root_ref = requiredString("artifact_root_ref"),
        touched_paths = jsonListCodec.decode(requiredString("touched_paths_json")),
        created_at = requiredOffsetDateTime("created_at"),
        created_by = requiredString("created_by"),
    )
