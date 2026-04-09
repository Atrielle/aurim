package io.atrielle.aurim.backend.persistence

import io.atrielle.aurim.backend.model.FactorySpec
import java.time.OffsetDateTime
import java.util.UUID
import kotlinx.coroutines.reactor.awaitSingle
import kotlinx.coroutines.reactor.awaitSingleOrNull
import org.springframework.r2dbc.core.DatabaseClient
import org.springframework.stereotype.Repository

@Repository
class FactorySpecRepository(
    private val databaseClient: DatabaseClient,
    private val jsonListCodec: JsonListCodec,
) {

    suspend fun create(
        factorySpecId: UUID,
        workspaceId: String,
        title: String,
        summary: String,
        problemStatement: String,
        goal: String,
        nonNegotiableConstraints: List<String>,
        initialScope: List<String>,
        excludedScope: List<String>,
        acceptanceStandard: String,
        status: String,
        createdAt: OffsetDateTime,
        createdBy: String,
    ): FactorySpec {
        databaseClient
            .sql(
                """
                insert into factory_spec (
                    factory_spec_id,
                    workspace_id,
                    title,
                    summary,
                    problem_statement,
                    goal,
                    non_negotiable_constraints_json,
                    initial_scope_json,
                    excluded_scope_json,
                    acceptance_standard,
                    status,
                    created_at,
                    created_by
                ) values (
                    :factory_spec_id,
                    :workspace_id,
                    :title,
                    :summary,
                    :problem_statement,
                    :goal,
                    :non_negotiable_constraints_json,
                    :initial_scope_json,
                    :excluded_scope_json,
                    :acceptance_standard,
                    :status,
                    :created_at,
                    :created_by
                )
                """.trimIndent(),
            )
            .bind("factory_spec_id", factorySpecId)
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .bind("title", title)
            .bind("summary", summary)
            .bind("problem_statement", problemStatement)
            .bind("goal", goal)
            .bind("non_negotiable_constraints_json", jsonListCodec.encode(nonNegotiableConstraints))
            .bind("initial_scope_json", jsonListCodec.encode(initialScope))
            .bind("excluded_scope_json", jsonListCodec.encode(excludedScope))
            .bind("acceptance_standard", acceptanceStandard)
            .bind("status", status)
            .bind("created_at", createdAt)
            .bind("created_by", createdBy)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(factorySpecId.toString())!!
    }

    suspend fun listByWorkspaceId(workspaceId: String): List<FactorySpec> =
        databaseClient
            .sql(
                """
                select factory_spec_id, workspace_id, title, summary, problem_statement, goal,
                       non_negotiable_constraints_json, initial_scope_json, excluded_scope_json,
                       acceptance_standard, status, created_at, created_by
                from factory_spec
                where workspace_id = :workspace_id
                order by created_at desc
                """.trimIndent(),
            )
            .bind("workspace_id", parseUuid(workspaceId, "workspace_id"))
            .map { row, _ -> row.toFactorySpec(jsonListCodec) }
            .all()
            .collectList()
            .awaitSingle()

    suspend fun findById(factorySpecId: String): FactorySpec? =
        databaseClient
            .sql(
                """
                select factory_spec_id, workspace_id, title, summary, problem_statement, goal,
                       non_negotiable_constraints_json, initial_scope_json, excluded_scope_json,
                       acceptance_standard, status, created_at, created_by
                from factory_spec
                where factory_spec_id = :factory_spec_id
                """.trimIndent(),
            )
            .bind("factory_spec_id", parseUuid(factorySpecId, "factory_spec_id"))
            .map { row, _ -> row.toFactorySpec(jsonListCodec) }
            .one()
            .awaitSingleOrNull()

    suspend fun update(factorySpec: FactorySpec): FactorySpec {
        databaseClient
            .sql(
                """
                update factory_spec
                set title = :title,
                    summary = :summary,
                    problem_statement = :problem_statement,
                    goal = :goal,
                    non_negotiable_constraints_json = :non_negotiable_constraints_json,
                    initial_scope_json = :initial_scope_json,
                    excluded_scope_json = :excluded_scope_json,
                    acceptance_standard = :acceptance_standard,
                    status = :status
                where factory_spec_id = :factory_spec_id
                """.trimIndent(),
            )
            .bind("factory_spec_id", parseUuid(factorySpec.factory_spec_id, "factory_spec_id"))
            .bind("title", factorySpec.title)
            .bind("summary", factorySpec.summary)
            .bind("problem_statement", factorySpec.problem_statement)
            .bind("goal", factorySpec.goal)
            .bind("non_negotiable_constraints_json", jsonListCodec.encode(factorySpec.non_negotiable_constraints))
            .bind("initial_scope_json", jsonListCodec.encode(factorySpec.initial_scope))
            .bind("excluded_scope_json", jsonListCodec.encode(factorySpec.excluded_scope))
            .bind("acceptance_standard", factorySpec.acceptance_standard)
            .bind("status", factorySpec.status)
            .fetch()
            .rowsUpdated()
            .awaitSingle()

        return findById(factorySpec.factory_spec_id)!!
    }
}

private fun io.r2dbc.spi.Row.toFactorySpec(jsonListCodec: JsonListCodec): FactorySpec =
    FactorySpec(
        factory_spec_id = requiredUuid("factory_spec_id").toString(),
        workspace_id = requiredUuid("workspace_id").toString(),
        title = requiredString("title"),
        summary = requiredString("summary"),
        problem_statement = requiredString("problem_statement"),
        goal = requiredString("goal"),
        non_negotiable_constraints = jsonListCodec.decode(requiredString("non_negotiable_constraints_json")),
        initial_scope = jsonListCodec.decode(requiredString("initial_scope_json")),
        excluded_scope = jsonListCodec.decode(requiredString("excluded_scope_json")),
        acceptance_standard = requiredString("acceptance_standard"),
        status = requiredString("status"),
        created_at = requiredOffsetDateTime("created_at"),
        created_by = requiredString("created_by"),
    )
