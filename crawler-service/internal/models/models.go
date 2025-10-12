package models

import "time"

// CrawlRequest represents a request to start a crawl
type CrawlRequest struct {
	Query         string   `json:"query"`
	MaxPages      int      `json:"max_pages"`
	MaxDepth      int      `json:"max_depth"`
	AllowedDomains []string `json:"allowed_domains,omitempty"`
	UserAgent     string   `json:"user_agent,omitempty"`
}

// CrawlJob represents a crawl job
type CrawlJob struct {
	ID            string    `json:"id"`
	Query         string    `json:"query"`
	Status        string    `json:"status"` // pending, running, completed, failed
	MaxPages      int       `json:"max_pages"`
	MaxDepth      int       `json:"max_depth"`
	PagesCrawled  int       `json:"pages_crawled"`
	URLsFound     int       `json:"urls_found"`
	StartedAt     time.Time `json:"started_at,omitempty"`
	CompletedAt   time.Time `json:"completed_at,omitempty"`
	Error         string    `json:"error,omitempty"`
	Results       []CrawlResult `json:"results,omitempty"`
}

// CrawlResult represents a single crawled page
type CrawlResult struct {
	URL         string    `json:"url"`
	Title       string    `json:"title"`
	Content     string    `json:"content"`
	Links       []string  `json:"links"`
	CrawledAt   time.Time `json:"crawled_at"`
	StatusCode  int       `json:"status_code"`
	Error       string    `json:"error,omitempty"`
}

// JobStatus represents the current status of a job
type JobStatus struct {
	JobID        string    `json:"job_id"`
	Status       string    `json:"status"`
	PagesCrawled int       `json:"pages_crawled"`
	URLsFound    int       `json:"urls_found"`
	Progress     float64   `json:"progress"`
	StartedAt    time.Time `json:"started_at,omitempty"`
	UpdatedAt    time.Time `json:"updated_at"`
}

// IntelServiceRequest represents data sent to the intel service
type IntelServiceRequest struct {
	JobID   string        `json:"job_id"`
	Results []CrawlResult `json:"results"`
}
