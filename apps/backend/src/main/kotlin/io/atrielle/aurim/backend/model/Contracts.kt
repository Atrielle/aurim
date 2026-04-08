package io.atrielle.aurim.backend.model

import java.time.OffsetDateTime

data class HealthResponse(
    val status: String,
    val service: String,
    val timestamp: OffsetDateTime,
)

data class PlatformContractResponse(
    val systemOfRecord: String,
    val workspaceBoundary: String,
    val workItemModel: String,
    val storagePolicy: String,
)
