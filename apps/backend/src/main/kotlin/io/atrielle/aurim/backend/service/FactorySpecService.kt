package io.atrielle.aurim.backend.service

import io.atrielle.aurim.backend.model.CreateFactorySpecRequest
import io.atrielle.aurim.backend.model.FactorySpec
import io.atrielle.aurim.backend.model.UpdateFactorySpecRequest
import io.atrielle.aurim.backend.persistence.FactorySpecRepository
import java.time.OffsetDateTime
import java.util.UUID
import org.springframework.stereotype.Service

@Service
class FactorySpecService(
    private val workspaceService: WorkspaceService,
    private val factorySpecRepository: FactorySpecRepository,
) {

    suspend fun create(
        workspaceId: String,
        request: CreateFactorySpecRequest,
    ): FactorySpec {
        workspaceService.get(workspaceId)
        return factorySpecRepository.create(
            factorySpecId = UUID.randomUUID(),
            workspaceId = workspaceId,
            title = request.title,
            summary = request.summary,
            problemStatement = request.problem_statement,
            goal = request.goal,
            nonNegotiableConstraints = request.non_negotiable_constraints,
            initialScope = request.initial_scope,
            excludedScope = request.excluded_scope,
            acceptanceStandard = request.acceptance_standard,
            status = "draft",
            createdAt = OffsetDateTime.now(),
            createdBy = request.created_by,
        )
    }

    suspend fun listByWorkspaceId(workspaceId: String): List<FactorySpec> {
        workspaceService.get(workspaceId)
        return factorySpecRepository.listByWorkspaceId(workspaceId)
    }

    suspend fun get(factorySpecId: String): FactorySpec =
        factorySpecRepository.findById(factorySpecId) ?: notFound("Factory spec", factorySpecId)

    suspend fun update(
        factorySpecId: String,
        request: UpdateFactorySpecRequest,
    ): FactorySpec {
        val current = get(factorySpecId)
        return factorySpecRepository.update(
            current.copy(
                title = request.title ?: current.title,
                summary = request.summary ?: current.summary,
                problem_statement = request.problem_statement ?: current.problem_statement,
                goal = request.goal ?: current.goal,
                non_negotiable_constraints = request.non_negotiable_constraints ?: current.non_negotiable_constraints,
                initial_scope = request.initial_scope ?: current.initial_scope,
                excluded_scope = request.excluded_scope ?: current.excluded_scope,
                acceptance_standard = request.acceptance_standard ?: current.acceptance_standard,
                status = request.status ?: current.status,
            ),
        )
    }

    suspend fun approve(factorySpecId: String): FactorySpec {
        val current = get(factorySpecId)
        return factorySpecRepository.update(
            current.copy(
                status = "approved",
            ),
        )
    }
}
