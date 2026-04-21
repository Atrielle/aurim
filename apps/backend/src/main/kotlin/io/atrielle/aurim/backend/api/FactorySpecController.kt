package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.CreateFactorySpecRequest
import io.atrielle.aurim.backend.model.FactorySpec
import io.atrielle.aurim.backend.model.ItemsResponse
import io.atrielle.aurim.backend.model.UpdateFactorySpecRequest
import io.atrielle.aurim.backend.service.FactorySpecService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PatchMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class FactorySpecController(
    private val factorySpecService: FactorySpecService,
) {

    @PostMapping("/workspaces/{workspace_id}/factory-specs")
    suspend fun createFactorySpec(
        @PathVariable("workspace_id") workspaceId: String,
        @RequestBody request: CreateFactorySpecRequest,
    ): ResponseEntity<FactorySpec> =
        ResponseEntity
            .status(HttpStatus.CREATED)
            .body(factorySpecService.create(workspaceId, request))

    @GetMapping("/workspaces/{workspace_id}/factory-specs")
    suspend fun listFactorySpecs(@PathVariable("workspace_id") workspaceId: String): ItemsResponse<FactorySpec> =
        ItemsResponse(
            items = factorySpecService.listByWorkspaceId(workspaceId),
        )

    @GetMapping("/factory-specs/{factory_spec_id}")
    suspend fun getFactorySpec(@PathVariable("factory_spec_id") factorySpecId: String): FactorySpec =
        factorySpecService.get(factorySpecId)

    @PatchMapping("/factory-specs/{factory_spec_id}")
    suspend fun updateFactorySpec(
        @PathVariable("factory_spec_id") factorySpecId: String,
        @RequestBody request: UpdateFactorySpecRequest,
    ): FactorySpec = factorySpecService.update(factorySpecId, request)

    @PostMapping("/factory-specs/{factory_spec_id}/approve")
    suspend fun approveFactorySpec(@PathVariable("factory_spec_id") factorySpecId: String): FactorySpec =
        factorySpecService.approve(factorySpecId)
}
