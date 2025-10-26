# --- Build stage ---
    FROM golang:1.21-alpine AS builder

    WORKDIR /app
    
    # Install git (needed for some Go modules)
    RUN apk add --no-cache git
    
    # Copy go.mod first
    COPY go.mod ./
    
    # Copy the rest of the source code
    COPY . .
    
    # Tidy dependencies to generate/update go.sum
    RUN go mod tidy
    
    # Download dependencies
    RUN go mod download
    
    # Build the application
    RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o crawler .
    
    # --- Final stage ---
    FROM alpine:latest
    
    # Install runtime dependencies
    RUN apk --no-cache add ca-certificates tzdata
    
    WORKDIR /root/
    
    # Copy the binary from the builder
    COPY --from=builder /app/crawler .
    
    # Expose the application port
    EXPOSE 8080
    
    # Run the application
    CMD ["./crawler"]
    