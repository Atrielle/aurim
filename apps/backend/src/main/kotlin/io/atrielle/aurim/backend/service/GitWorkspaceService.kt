package io.atrielle.aurim.backend.service

import io.atrielle.aurim.backend.model.CreateGitWorkspaceRequest
import io.atrielle.aurim.backend.model.GitWorkspace
import io.atrielle.aurim.backend.model.UpdateGitWorkspaceRequest
import io.atrielle.aurim.backend.persistence.GitWorkspaceRepository
import java.time.OffsetDateTime
import java.util.UUID
import org.springframework.stereotype.Service

@Service
class GitWorkspaceService(
    private val workspaceService: WorkspaceService,
    private val gitWorkspaceRepository: GitWorkspaceRepository,
) {

    suspend fun create(
        workspaceId: String,
        request: CreateGitWorkspaceRequest,
    ): GitWorkspace {
        workspaceService.get(workspaceId)
        return gitWorkspaceRepository.create(
            gitWorkspaceId = UUID.randomUUID(),
            workspaceId = workspaceId,
            provider = request.provider,
            repositoryUrl = request.repository_url,
            defaultBranch = request.default_branch,
            connectionStatus = "connected",
            createdAt = OffsetDateTime.now(),
            createdBy = request.created_by,
        )
    }

    suspend fun listByWorkspaceId(workspaceId: String): List<GitWorkspace> {
        workspaceService.get(workspaceId)
        return gitWorkspaceRepository.listByWorkspaceId(workspaceId)
    }

    suspend fun get(gitWorkspaceId: String): GitWorkspace =
        gitWorkspaceRepository.findById(gitWorkspaceId) ?: notFound("Git workspace", gitWorkspaceId)

    suspend fun update(
        gitWorkspaceId: String,
        request: UpdateGitWorkspaceRequest,
    ): GitWorkspace {
        val current = get(gitWorkspaceId)
        return gitWorkspaceRepository.update(
            current.copy(
                default_branch = request.default_branch ?: current.default_branch,
                connection_status = request.connection_status ?: current.connection_status,
            ),
        )
    }

    suspend fun archive(gitWorkspaceId: String): GitWorkspace {
        val current = get(gitWorkspaceId)
        return gitWorkspaceRepository.update(
            current.copy(
                connection_status = "archived",
            ),
        )
    }
}
