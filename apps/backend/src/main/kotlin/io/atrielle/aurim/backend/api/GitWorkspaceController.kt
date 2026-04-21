package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.CreateGitWorkspaceRequest
import io.atrielle.aurim.backend.model.GitWorkspace
import io.atrielle.aurim.backend.model.ItemsResponse
import io.atrielle.aurim.backend.model.UpdateGitWorkspaceRequest
import io.atrielle.aurim.backend.service.GitWorkspaceService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PatchMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class GitWorkspaceController(
    private val gitWorkspaceService: GitWorkspaceService,
) {

    @PostMapping("/workspaces/{workspace_id}/git-workspaces")
    suspend fun createGitWorkspace(
        @PathVariable("workspace_id") workspaceId: String,
        @RequestBody request: CreateGitWorkspaceRequest,
    ): ResponseEntity<GitWorkspace> =
        ResponseEntity
            .status(HttpStatus.CREATED)
            .body(gitWorkspaceService.create(workspaceId, request))

    @GetMapping("/workspaces/{workspace_id}/git-workspaces")
    suspend fun listGitWorkspaces(@PathVariable("workspace_id") workspaceId: String): ItemsResponse<GitWorkspace> =
        ItemsResponse(
            items = gitWorkspaceService.listByWorkspaceId(workspaceId),
        )

    @GetMapping("/git-workspaces/{git_workspace_id}")
    suspend fun getGitWorkspace(@PathVariable("git_workspace_id") gitWorkspaceId: String): GitWorkspace =
        gitWorkspaceService.get(gitWorkspaceId)

    @PatchMapping("/git-workspaces/{git_workspace_id}")
    suspend fun updateGitWorkspace(
        @PathVariable("git_workspace_id") gitWorkspaceId: String,
        @RequestBody request: UpdateGitWorkspaceRequest,
    ): GitWorkspace = gitWorkspaceService.update(gitWorkspaceId, request)

    @DeleteMapping("/git-workspaces/{git_workspace_id}")
    suspend fun archiveGitWorkspace(@PathVariable("git_workspace_id") gitWorkspaceId: String): ResponseEntity<GitWorkspace> =
        ResponseEntity
            .status(HttpStatus.ACCEPTED)
            .body(gitWorkspaceService.archive(gitWorkspaceId))
}
