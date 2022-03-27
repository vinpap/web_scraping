from googleimagesscraper import Google_images_scraper

scraper = Google_images_scraper()
scraper.download_images("cat", 600, size=(300,300))
scraper.download_images("dog", 600, size=(300,300))
