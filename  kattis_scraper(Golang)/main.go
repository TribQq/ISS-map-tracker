package main

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"

	"github.com/TribQq/mini_apps/tree/master/%20kattis_scraper(Golang)/utils"
)

func main() {
	r := gin.Default()
	r.MaxMultipartMemory = 8 << 20
	r.Static("/", "./public")
	r.Use(cors.New(cors.Config{
		AllowOrigins: []string{"https://djwebapp.herokuapp.com", "http://localhost:3000"},
		AllowMethods: []string{"GET", "PUT", "POST"},
	}))

	r.POST("/kattis", utils.GetProblemsHandler)

	r.Run()
}
