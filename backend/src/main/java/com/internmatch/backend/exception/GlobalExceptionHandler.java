package com.internmatch.backend.exception;

import com.internmatch.backend.dto.ApiResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Object>> handleException(Exception ex) {

        ApiResponse<Object> response =
                new ApiResponse<>(
                        false,
                        ex.getMessage(),
                        null
                );

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(response);
    }

    @ExceptionHandler(org.springframework.web.server.ResponseStatusException.class)
    public ResponseEntity<ApiResponse<Object>> handleResponseStatusException(org.springframework.web.server.ResponseStatusException ex) {
        ApiResponse<Object> response = new ApiResponse<>(
                false,
                ex.getReason() != null ? ex.getReason() : ex.getMessage(),
                null
        );
        return ResponseEntity
                .status(ex.getStatusCode())
                .body(response);
    }

    @ExceptionHandler(org.springframework.web.bind.MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Object>> handleValidationException(org.springframework.web.bind.MethodArgumentNotValidException ex) {
        String errorMsg = ex.getBindingResult().getFieldErrors().stream()
                .map(org.springframework.validation.FieldError::getDefaultMessage)
                .collect(java.util.stream.Collectors.joining(", "));
        ApiResponse<Object> response = new ApiResponse<>(
                false,
                "Validation failed: " + errorMsg,
                null
        );
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(response);
    }

    @ExceptionHandler(org.springframework.http.converter.HttpMessageNotReadableException.class)
    public ResponseEntity<ApiResponse<Object>> handleMalformedJson(org.springframework.http.converter.HttpMessageNotReadableException ex) {
        ApiResponse<Object> response = new ApiResponse<>(
                false,
                "Malformed request payload",
                null
        );
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(response);
    }
}