This is a very simple scraper for Google Images. It will also resize the images it downloads automatically.

How to use:

```
scraper = Google_images_scraper()
scraper.download_images("my query", count=100, size=(600, 600))

# Use the function below instead if you only want one image (the first showing up on Google Images)
scraper.download_image("my query", size=(1024, 768)) 
```


Note: you need to download the web driver matching your web browser and move it in your working directory, or this scraper won't work. See Selenium's documentation for further details
