package database

import (
	"context"
	"os"
	"time"

	"github.com/go-redis/redis/v8"
	log "github.com/sirupsen/logrus"
)

var (
	ctx = context.Background()
	rdb *redis.Client
)

// InitRedis initializes Redis connection
func InitRedis() error {
	redisHost := os.Getenv("REDIS_HOST")
	if redisHost == "" {
		redisHost = "localhost:6379"
	}

	rdb = redis.NewClient(&redis.Options{
		Addr:         redisHost,
		Password:     os.Getenv("REDIS_PASSWORD"),
		DB:           0,
		DialTimeout:  10 * time.Second,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
	})

	// Test connection
	_, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.WithError(err).Error("Failed to connect to Redis")
		return err
	}

	log.Info("Redis connection established")
	return nil
}

// GetRedisClient returns the Redis client
func GetRedisClient() *redis.Client {
	return rdb
}

// CloseRedis closes the Redis connection
func CloseRedis() error {
	if rdb != nil {
		return rdb.Close()
	}
	return nil
}
