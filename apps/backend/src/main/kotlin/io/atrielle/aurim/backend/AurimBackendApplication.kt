package io.atrielle.aurim.backend

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class AurimBackendApplication

fun main(args: Array<String>) {
    runApplication<AurimBackendApplication>(*args)
}
