package io.atrielle.aurim.backend.persistence

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import io.r2dbc.spi.Row
import java.time.OffsetDateTime
import java.util.UUID
import org.springframework.http.HttpStatus
import org.springframework.stereotype.Component
import org.springframework.web.server.ResponseStatusException

@Component
class JsonListCodec(
    private val objectMapper: ObjectMapper,
) {

    fun encode(values: List<String>): String = objectMapper.writeValueAsString(values)

    fun decode(value: String?): List<String> =
        if (value.isNullOrBlank()) {
            emptyList()
        } else {
            objectMapper.readValue(value)
        }
}

internal fun Row.requiredString(name: String): String = get(name, String::class.java)!!

internal fun Row.requiredUuid(name: String): UUID = get(name, UUID::class.java)!!

internal fun Row.requiredOffsetDateTime(name: String): OffsetDateTime = get(name, OffsetDateTime::class.java)!!

internal fun parseUuid(value: String, fieldName: String): UUID =
    try {
        UUID.fromString(value)
    } catch (_: IllegalArgumentException) {
        throw ResponseStatusException(
            HttpStatus.BAD_REQUEST,
            "Invalid UUID for $fieldName: $value",
        )
    }
