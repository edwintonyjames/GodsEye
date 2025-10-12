package handlers

import (
	"definitelynotaspy/crawler-service/internal/crawler"
	"definitelynotaspy/crawler-service/internal/models"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
	log "github.com/sirupsen/logrus"
)

var (
	jobStore = make(map[string]*models.CrawlJob)
	crawlerService = crawler.NewCrawlerService()
)

// HealthCheck returns the health status of the service
func HealthCheck(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{
		"status":    "healthy",
		"service":   "crawler",
		"timestamp": time.Now().UTC(),
	})
}

// StartCrawl initiates a new crawl job
func StartCrawl(c *fiber.Ctx) error {
	var req models.CrawlRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	// Validate request
	if req.Query == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Query is required",
		})
	}

	if req.MaxPages <= 0 {
		req.MaxPages = 50
	}

	if req.MaxDepth <= 0 {
		req.MaxDepth = 2
	}

	// Create job
	jobID := uuid.New().String()
	job := &models.CrawlJob{
		ID:           jobID,
		Query:        req.Query,
		Status:       "pending",
		MaxPages:     req.MaxPages,
		MaxDepth:     req.MaxDepth,
		PagesCrawled: 0,
		URLsFound:    0,
		StartedAt:    time.Now().UTC(),
	}

	jobStore[jobID] = job

	// Start crawl asynchronously
	go func() {
		if err := crawlerService.StartCrawl(job, req); err != nil {
			log.WithError(err).WithField("job_id", jobID).Error("Crawl failed")
			job.Status = "failed"
			job.Error = err.Error()
			job.CompletedAt = time.Now().UTC()
		}
	}()

	log.WithFields(log.Fields{
		"job_id":    jobID,
		"query":     req.Query,
		"max_pages": req.MaxPages,
	}).Info("Crawl job started")

	return c.Status(fiber.StatusCreated).JSON(fiber.Map{
		"job_id":  jobID,
		"status":  "pending",
		"message": "Crawl job created successfully",
		"job":     job,
	})
}

// GetCrawlStatus returns the status of a specific crawl job
func GetCrawlStatus(c *fiber.Ctx) error {
	jobID := c.Params("id")
	
	job, exists := jobStore[jobID]
	if !exists {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Job not found",
		})
	}

	progress := 0.0
	if job.MaxPages > 0 {
		progress = float64(job.PagesCrawled) / float64(job.MaxPages) * 100
		if progress > 100 {
			progress = 100
		}
	}

	return c.JSON(fiber.Map{
		"job_id":        job.ID,
		"status":        job.Status,
		"pages_crawled": job.PagesCrawled,
		"urls_found":    job.URLsFound,
		"progress":      progress,
		"started_at":    job.StartedAt,
		"completed_at":  job.CompletedAt,
		"error":         job.Error,
	})
}

// ListJobs returns all crawl jobs
func ListJobs(c *fiber.Ctx) error {
	jobs := make([]*models.CrawlJob, 0, len(jobStore))
	for _, job := range jobStore {
		jobs = append(jobs, job)
	}

	return c.JSON(fiber.Map{
		"total": len(jobs),
		"jobs":  jobs,
	})
}

// CancelJob cancels a running crawl job
func CancelJob(c *fiber.Ctx) error {
	jobID := c.Params("id")
	
	job, exists := jobStore[jobID]
	if !exists {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Job not found",
		})
	}

	if job.Status == "completed" || job.Status == "failed" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Cannot cancel a completed or failed job",
		})
	}

	job.Status = "cancelled"
	job.CompletedAt = time.Now().UTC()

	log.WithField("job_id", jobID).Info("Crawl job cancelled")

	return c.JSON(fiber.Map{
		"message": "Job cancelled successfully",
		"job_id":  jobID,
	})
}
