package io.atrielle.aurim.backend.service

import io.atrielle.aurim.backend.model.CreateWorkspaceRequest
import io.atrielle.aurim.backend.model.UpdateWorkspaceRequest
import io.atrielle.aurim.backend.model.Workspace
import io.atrielle.aurim.backend.persistence.WorkspaceRepository
import java.time.OffsetDateTime
import java.util.UUID
import org.springframework.http.HttpStatus
import org.springframework.stereotype.Service
import org.springframework.web.server.ResponseStatusException

@Service
class WorkspaceService(
    private val workspaceRepository: WorkspaceRepository,
) {

    suspend fun create(request: CreateWorkspaceRequest): Workspace {
        val now = OffsetDateTime.now()
        return workspaceRepository.create(
            workspaceId = UUID.randomUUID(),
            slug = request.slug,
            name = request.name,
            status = "active",
            createdAt = now,
            createdBy = request.created_by,
            updatedAt = now,
        )
    }

    suspend fun list(): List<Workspace> = workspaceRepository.list()

    suspend fun get(workspaceId: String): Workspace =
        workspaceRepository.findById(workspaceId) ?: notFound("Workspace", workspaceId)

    suspend fun update(
        workspaceId: String,
        request: UpdateWorkspaceRequest,
    ): Workspace {
        val current = get(workspaceId)
        return workspaceRepository.update(
            current.copy(
                name = request.name ?: current.name,
                status = request.status ?: current.status,
                updated_at = OffsetDateTime.now(),
            ),
        )
    }
}

internal fun notFound(resource: String, id: String): Nothing =
    throw ResponseStatusException(HttpStatus.NOT_FOUND, "$resource not found: $id")
