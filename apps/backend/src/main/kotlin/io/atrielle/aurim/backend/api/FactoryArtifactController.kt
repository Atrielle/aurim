package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.CreateFactoryArtifactRequest
import io.atrielle.aurim.backend.model.FactoryArtifact
import io.atrielle.aurim.backend.model.ItemsResponse
import io.atrielle.aurim.backend.service.FactoryArtifactService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class FactoryArtifactController(
    private val factoryArtifactService: FactoryArtifactService,
) {

    @PostMapping("/factory-runs/{factory_run_id}/artifacts")
    suspend fun createFactoryArtifact(
        @PathVariable("factory_run_id") factoryRunId: String,
        @RequestBody request: CreateFactoryArtifactRequest,
    ): ResponseEntity<FactoryArtifact> =
        ResponseEntity
            .status(HttpStatus.CREATED)
            .body(factoryArtifactService.create(factoryRunId, request))

    @GetMapping("/factory-runs/{factory_run_id}/artifacts")
    suspend fun listFactoryArtifacts(@PathVariable("factory_run_id") factoryRunId: String): ItemsResponse<FactoryArtifact> =
        ItemsResponse(
            items = factoryArtifactService.listByFactoryRunId(factoryRunId),
        )

    @GetMapping("/factory-artifacts/{factory_artifact_id}")
    suspend fun getFactoryArtifact(@PathVariable("factory_artifact_id") factoryArtifactId: String): FactoryArtifact =
        factoryArtifactService.get(factoryArtifactId)
}
