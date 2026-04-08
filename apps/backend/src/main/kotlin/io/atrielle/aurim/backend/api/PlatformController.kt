package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.HealthResponse
import io.atrielle.aurim.backend.model.PlatformContractResponse
import java.time.OffsetDateTime
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class PlatformController {

    @GetMapping("/health")
    fun health(): HealthResponse =
        HealthResponse(
            status = "ok",
            service = "aurim-backend",
            timestamp = OffsetDateTime.now(),
        )

    @GetMapping("/platform-contract")
    fun platformContract(): PlatformContractResponse =
        PlatformContractResponse(
            systemOfRecord = "PostgreSQL",
            workspaceBoundary = "Every domain resource is scoped by workspace_id.",
            workItemModel = "Calendar, kanban, WBS, and gantt project from one Work Item model.",
            storagePolicy = "File metadata is platform-owned; file body storage is provider-driven.",
        )
}
