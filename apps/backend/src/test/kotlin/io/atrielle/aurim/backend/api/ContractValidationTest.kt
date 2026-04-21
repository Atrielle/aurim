package io.atrielle.aurim.backend.api

import io.atrielle.aurim.backend.model.CloseFactoryRunRequest
import io.atrielle.aurim.backend.model.CreateGitWorkspaceRequest
import io.atrielle.aurim.backend.model.CreateWorkspaceRequest
import io.atrielle.aurim.backend.model.UpdateWorkspaceRequest
import jakarta.validation.Validation
import jakarta.validation.Validator
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class ContractValidationTest {

    private val validator: Validator = Validation.buildDefaultValidatorFactory().validator

    @Test
    fun `create workspace rejects invalid slug`() {
        val violations = validator.validate(
            CreateWorkspaceRequest(
                slug = "Invalid Slug",
                name = "Aurim",
                created_by = "tester",
            ),
        )

        assertHasViolation(violations.map { it.propertyPath.toString() }, "slug")
    }

    @Test
    fun `update workspace rejects empty payload`() {
        val violations = validator.validate(UpdateWorkspaceRequest())

        assertHasViolation(violations.map { it.message }, "At least one workspace field must be provided.")
    }

    @Test
    fun `create git workspace rejects invalid repository url`() {
        val violations = validator.validate(
            CreateGitWorkspaceRequest(
                provider = "github",
                repository_url = "not-a-uri",
                default_branch = "main",
                created_by = "tester",
            ),
        )

        assertHasViolation(violations.map { it.propertyPath.toString() }, "repository_url")
    }

    @Test
    fun `close factory run rejects non contract evaluation result`() {
        val violations = validator.validate(
            CloseFactoryRunRequest(
                evaluation_result = "MAYBE",
                closed_by = "tester",
            ),
        )

        assertHasViolation(violations.map { it.propertyPath.toString() }, "evaluation_result")
    }

    private fun assertHasViolation(values: List<String>, expected: String) {
        assertTrue(
            values.any { it == expected },
            "Expected violation <$expected> but got $values",
        )
    }
}
