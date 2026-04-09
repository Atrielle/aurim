package io.atrielle.aurim.backend.service

import io.atrielle.aurim.backend.model.CloseFactoryRunRequest
import io.atrielle.aurim.backend.model.CreateFactoryRunRequest
import io.atrielle.aurim.backend.model.FactoryRun
import io.atrielle.aurim.backend.persistence.FactoryRunRepository
import java.time.OffsetDateTime
import java.util.UUID
import org.springframework.http.HttpStatus
import org.springframework.stereotype.Service
import org.springframework.web.server.ResponseStatusException

@Service
class FactoryRunService(
    private val workspaceService: WorkspaceService,
    private val factorySpecService: FactorySpecService,
    private val factoryRunRepository: FactoryRunRepository,
) {

    suspend fun create(request: CreateFactoryRunRequest): FactoryRun {
        workspaceService.get(request.workspace_id)
        val factorySpec = factorySpecService.get(request.factory_spec_id)
        if (factorySpec.workspace_id != request.workspace_id) {
            throw ResponseStatusException(
                HttpStatus.CONFLICT,
                "Factory spec does not belong to the requested workspace.",
            )
        }
        return factoryRunRepository.create(
            factoryRunId = UUID.randomUUID(),
            workspaceId = request.workspace_id,
            factorySpecId = request.factory_spec_id,
            status = "created",
            plannerPromptRef = request.planner_prompt_ref,
            generatorPromptRef = request.generator_prompt_ref,
            evaluatorPromptRef = request.evaluator_prompt_ref,
            contractSnapshotRef = request.contract_snapshot_ref,
            artifactRootRef = request.artifact_root_ref,
            touchedPaths = request.touched_paths,
            createdAt = OffsetDateTime.now(),
            createdBy = request.created_by,
        )
    }

    suspend fun listByWorkspaceId(workspaceId: String): List<FactoryRun> {
        workspaceService.get(workspaceId)
        return factoryRunRepository.listByWorkspaceId(workspaceId)
    }

    suspend fun get(factoryRunId: String): FactoryRun =
        factoryRunRepository.findById(factoryRunId) ?: notFound("Factory run", factoryRunId)

    suspend fun start(factoryRunId: String): FactoryRun {
        val current = get(factoryRunId)
        return factoryRunRepository.update(
            current.copy(
                status = "running",
            ),
        )
    }

    suspend fun close(
        factoryRunId: String,
        request: CloseFactoryRunRequest,
    ): FactoryRun {
        if (request.evaluation_result != "PASS") {
            throw ResponseStatusException(
                HttpStatus.CONFLICT,
                "Factory run cannot close without evaluator PASS.",
            )
        }
        val current = get(factoryRunId)
        return factoryRunRepository.update(
            factoryRun = current.copy(
                status = "closed",
            ),
            closedAt = OffsetDateTime.now(),
            closedBy = request.closed_by,
        )
    }
}
