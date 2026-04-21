package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.CloseFactoryRunRequest
import io.atrielle.aurim.backend.model.CreateFactoryRunRequest
import io.atrielle.aurim.backend.model.FactoryRun
import io.atrielle.aurim.backend.model.ItemsResponse
import io.atrielle.aurim.backend.service.FactoryRunService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class FactoryRunController(
    private val factoryRunService: FactoryRunService,
) {

    @PostMapping("/factory-runs")
    suspend fun createFactoryRun(@RequestBody request: CreateFactoryRunRequest): ResponseEntity<FactoryRun> =
        ResponseEntity
            .status(HttpStatus.CREATED)
            .body(factoryRunService.create(request))

    @GetMapping("/factory-runs/{factory_run_id}")
    suspend fun getFactoryRun(@PathVariable("factory_run_id") factoryRunId: String): FactoryRun =
        factoryRunService.get(factoryRunId)

    @GetMapping("/workspaces/{workspace_id}/factory-runs")
    suspend fun listFactoryRuns(@PathVariable("workspace_id") workspaceId: String): ItemsResponse<FactoryRun> =
        ItemsResponse(
            items = factoryRunService.listByWorkspaceId(workspaceId),
        )

    @PostMapping("/factory-runs/{factory_run_id}/start")
    suspend fun startFactoryRun(@PathVariable("factory_run_id") factoryRunId: String): FactoryRun =
        factoryRunService.start(factoryRunId)

    @PostMapping("/factory-runs/{factory_run_id}/close")
    suspend fun closeFactoryRun(
        @PathVariable("factory_run_id") factoryRunId: String,
        @RequestBody request: CloseFactoryRunRequest,
    ): FactoryRun = factoryRunService.close(factoryRunId, request)
}
