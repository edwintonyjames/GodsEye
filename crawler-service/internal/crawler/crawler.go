package crawler

import (
	"bytes"
	"definitelynotaspy/crawler-service/internal/models"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/gocolly/colly/v2"
	"github.com/gocolly/colly/v2/extensions"
	log "github.com/sirupsen/logrus"
)

type CrawlerService struct {
	mu sync.Mutex
}

func NewCrawlerService() *CrawlerService {
	return &CrawlerService{}
}

// StartCrawl initiates a web crawl based on the provided job and request
func (cs *CrawlerService) StartCrawl(job *models.CrawlJob, req models.CrawlRequest) error {
	cs.mu.Lock()
	job.Status = "running"
	cs.mu.Unlock()

	// Create collector
	c := colly.NewCollector(
		colly.MaxDepth(req.MaxDepth),
		colly.Async(true),
	)

	// Set user agent
	userAgent := req.UserAgent
	if userAgent == "" {
		userAgent = os.Getenv("USER_AGENT")
		if userAgent == "" {
			userAgent = "DefinitelyNotASpy/1.0"
		}
	}
	c.UserAgent = userAgent

	// Add random user agent extension
	extensions.RandomUserAgent(c)

	// Set rate limiting
	c.Limit(&colly.LimitRule{
		DomainGlob:  "*",
		Parallelism: 2,
		Delay:       1 * time.Second,
	})

	// Track crawled pages
	pageCount := 0
	var results []models.CrawlResult
	var resultsMu sync.Mutex

	// Set timeout
	c.SetRequestTimeout(30 * time.Second)

	// On HTML response
	c.OnHTML("html", func(e *colly.HTMLElement) {
		resultsMu.Lock()
		defer resultsMu.Unlock()

		if pageCount >= req.MaxPages {
			return
		}

		pageCount++
		job.PagesCrawled = pageCount

		// Extract title
		title := e.ChildText("title")

		// Extract main content
		content := extractContent(e)

		// Extract links
		var links []string
		e.ForEach("a[href]", func(_ int, el *colly.HTMLElement) {
			link := el.Attr("href")
			if link != "" {
				links = append(links, link)
			}
		})

		result := models.CrawlResult{
			URL:        e.Request.URL.String(),
			Title:      title,
			Content:    content,
			Links:      links,
			CrawledAt:  time.Now().UTC(),
			StatusCode: e.Response.StatusCode,
		}

		results = append(results, result)
		job.URLsFound = len(links)

		log.WithFields(log.Fields{
			"job_id": job.ID,
			"url":    result.URL,
			"title":  result.Title,
		}).Info("Page crawled")
	})

	// Follow links
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		if pageCount >= req.MaxPages {
			return
		}
		
		link := e.Attr("href")
		if link != "" {
			e.Request.Visit(link)
		}
	})

	// On request
	c.OnRequest(func(r *colly.Request) {
		log.WithFields(log.Fields{
			"job_id": job.ID,
			"url":    r.URL.String(),
		}).Debug("Visiting")
	})

	// On error
	c.OnError(func(r *colly.Response, err error) {
		log.WithFields(log.Fields{
			"job_id": job.ID,
			"url":    r.Request.URL.String(),
			"error":  err.Error(),
		}).Error("Crawl error")
	})

	// Start crawling from search results
	searchURLs := performSearch(req.Query, 10)
	
	for _, url := range searchURLs {
		c.Visit(url)
	}

	// Wait for completion
	c.Wait()

	// Update job
	cs.mu.Lock()
	job.Status = "completed"
	job.Results = results
	job.CompletedAt = time.Now().UTC()
	cs.mu.Unlock()

	// Send results to intel service
	go cs.sendToIntelService(job)

	log.WithFields(log.Fields{
		"job_id":        job.ID,
		"pages_crawled": job.PagesCrawled,
	}).Info("Crawl completed")

	return nil
}

// extractContent extracts meaningful text content from HTML
func extractContent(e *colly.HTMLElement) string {
	var content strings.Builder

	// Try to extract from common content areas
	selectors := []string{
		"article",
		"main",
		".content",
		"#content",
		".post-content",
		".entry-content",
		"p",
	}

	for _, selector := range selectors {
		e.ForEach(selector, func(_ int, el *colly.HTMLElement) {
			text := strings.TrimSpace(el.Text)
			if len(text) > 50 {
				content.WriteString(text)
				content.WriteString("\n\n")
			}
		})

		if content.Len() > 500 {
			break
		}
	}

	// Limit content size
	result := content.String()
	if len(result) > 5000 {
		result = result[:5000]
	}

	return result
}

// performSearch simulates a search and returns URLs (in production, integrate with Google Custom Search API)
func performSearch(query string, maxResults int) []string {
	// For now, return some placeholder URLs
	// In production, integrate with Google Custom Search API or similar
	log.WithField("query", query).Info("Performing search")
	
	// This is a placeholder. In production, you would:
	// 1. Use Google Custom Search API
	// 2. Use SerpAPI
	// 3. Use Bing Search API
	// 4. Or implement your own search scraper
	
	return []string{
		fmt.Sprintf("https://en.wikipedia.org/wiki/%s", strings.ReplaceAll(query, " ", "_")),
	}
}

// sendToIntelService sends crawl results to the intel service for processing
func (cs *CrawlerService) sendToIntelService(job *models.CrawlJob) error {
	intelURL := os.Getenv("PYTHON_SERVICE_URL")
	if intelURL == "" {
		log.Warn("PYTHON_SERVICE_URL not set, skipping intel service")
		return nil
	}

	payload := models.IntelServiceRequest{
		JobID:   job.ID,
		Results: job.Results,
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal payload: %w", err)
	}

	resp, err := http.Post(
		fmt.Sprintf("%s/api/v1/process", intelURL),
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		log.WithError(err).Error("Failed to send to intel service")
		return err
	}
	defer resp.Body.Close()

	log.WithFields(log.Fields{
		"job_id": job.ID,
		"status": resp.StatusCode,
	}).Info("Sent to intel service")

	return nil
}
