package main

import (
	"fmt"
	"os"

	"definitelynotaspy/crawler-service/internal/handlers"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
)

func init() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Info("No .env file found, using environment variables")
	}

	// Configure logging
	logLevel := os.Getenv("LOG_LEVEL")
	if logLevel == "" {
		logLevel = "INFO"
	}

	level, err := log.ParseLevel(logLevel)
	if err != nil {
		level = log.InfoLevel
	}
	log.SetLevel(level)
	log.SetFormatter(&log.JSONFormatter{})
}

func main() {
	// Create Fiber app
	app := fiber.New(fiber.Config{
		AppName:      "DefinitelyNotASpy Crawler Service",
		ErrorHandler: customErrorHandler,
	})

	// Middleware
	app.Use(recover.New())
	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowHeaders: "Origin, Content-Type, Accept",
	}))

	// Health check
	app.Get("/health", handlers.HealthCheck)

	// API routes
	api := app.Group("/api/v1")
	
	// Crawler routes
	api.Post("/crawl", handlers.StartCrawl)
	api.Get("/status/:id", handlers.GetCrawlStatus)
	api.Get("/jobs", handlers.ListJobs)
	api.Delete("/job/:id", handlers.CancelJob)

	// Get port from environment
	port := os.Getenv("CRAWLER_PORT")
	if port == "" {
		port = "8080"
	}

	// Start server
	log.WithField("port", port).Info("🚀 Crawler service starting")
	if err := app.Listen(fmt.Sprintf(":%s", port)); err != nil {
		log.Fatal(err)
	}
}

func customErrorHandler(c *fiber.Ctx, err error) error {
	code := fiber.StatusInternalServerError
	if e, ok := err.(*fiber.Error); ok {
		code = e.Code
	}

	log.WithFields(log.Fields{
		"error": err.Error(),
		"path":  c.Path(),
		"code":  code,
	}).Error("Request error")

	return c.Status(code).JSON(fiber.Map{
		"error":   err.Error(),
		"code":    code,
		"path":    c.Path(),
		"success": false,
	})
}
