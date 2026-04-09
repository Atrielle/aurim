package io.atrielle.aurim.backend.service

import io.atrielle.aurim.backend.model.CreateFactoryArtifactRequest
import io.atrielle.aurim.backend.model.FactoryArtifact
import io.atrielle.aurim.backend.persistence.FactoryArtifactRepository
import java.time.OffsetDateTime
import java.util.UUID
import org.springframework.stereotype.Service

@Service
class FactoryArtifactService(
    private val workspaceService: WorkspaceService,
    private val factoryRunService: FactoryRunService,
    private val factoryArtifactRepository: FactoryArtifactRepository,
) {

    suspend fun create(
        factoryRunId: String,
        request: CreateFactoryArtifactRequest,
    ): FactoryArtifact {
        workspaceService.get(request.workspace_id)
        val factoryRun = factoryRunService.get(factoryRunId)
        if (factoryRun.workspace_id != request.workspace_id) {
            throw notFound("Factory run for workspace", "$factoryRunId / ${request.workspace_id}")
        }
        return factoryArtifactRepository.create(
            factoryArtifactId = UUID.randomUUID(),
            factoryRunId = factoryRunId,
            workspaceId = request.workspace_id,
            artifactType = request.artifact_type,
            name = request.name,
            contentRef = request.content_ref,
            checksum = request.checksum,
            createdAt = OffsetDateTime.now(),
            createdBy = request.created_by,
        )
    }

    suspend fun listByFactoryRunId(factoryRunId: String): List<FactoryArtifact> {
        factoryRunService.get(factoryRunId)
        return factoryArtifactRepository.listByFactoryRunId(factoryRunId)
    }

    suspend fun get(factoryArtifactId: String): FactoryArtifact =
        factoryArtifactRepository.findById(factoryArtifactId) ?: notFound("Factory artifact", factoryArtifactId)
}
