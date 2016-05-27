HOST = "127.0.0.1"
PORT = 8080

MONGO = {
  "host": "127.0.0.1",
  "port": 27017,
  "db": "eight_coupons"
}

SCRAPER = {
  "url_template": "http://www.giantbomb.com/api/platforms/?limit={limit}&offset={offset}&api_key={api_key}&format=json&platforms={platforms}",
  "platform_url_template": "http://www.giantbomb.com/api/platforms/?limit=100&offset=0&api_key={api_key}&format=json",
  "api_key": "a79d08980c27dde4ff8358da190b5a35af9be21f",
  "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
  "platforms": ('NES', 'SNES', 'N64'),
  "step": 100,
  "run_every": 3600, # Fetch time period in seconds
}
