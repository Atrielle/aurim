package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.CreateWorkspaceRequest
import io.atrielle.aurim.backend.model.ItemsResponse
import io.atrielle.aurim.backend.model.UpdateWorkspaceRequest
import io.atrielle.aurim.backend.model.Workspace
import io.atrielle.aurim.backend.service.WorkspaceService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PatchMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class WorkspaceController(
    private val workspaceService: WorkspaceService,
) {

    @PostMapping("/workspaces")
    suspend fun createWorkspace(@RequestBody request: CreateWorkspaceRequest): ResponseEntity<Workspace> =
        ResponseEntity
            .status(HttpStatus.CREATED)
            .body(workspaceService.create(request))

    @GetMapping("/workspaces")
    suspend fun listWorkspaces(): ItemsResponse<Workspace> =
        ItemsResponse(
            items = workspaceService.list(),
        )

    @GetMapping("/workspaces/{workspace_id}")
    suspend fun getWorkspace(@PathVariable("workspace_id") workspaceId: String): Workspace =
        workspaceService.get(workspaceId)

    @PatchMapping("/workspaces/{workspace_id}")
    suspend fun updateWorkspace(
        @PathVariable("workspace_id") workspaceId: String,
        @RequestBody request: UpdateWorkspaceRequest,
    ): Workspace = workspaceService.update(workspaceId, request)
}
