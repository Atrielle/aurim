package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.HealthResponse
import java.time.OffsetDateTime
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class PlatformController {

    @GetMapping("/health")
    suspend fun health(): HealthResponse =
        HealthResponse(
            status = "ok",
            service = "aurim-backend",
            timestamp = OffsetDateTime.now(),
        )
}
