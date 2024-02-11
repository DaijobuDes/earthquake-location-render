from selenium import webdriver

GRID_URL = "http://selenium:4444/wd/hub"

class Driver:

    # Headless browser setup
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.binary_location = '/usr/bin/google-chrome'
        self.browser = webdriver.Remote(command_executor=GRID_URL, options=self.options)

    # Set resolution to 1080p
    def window_size(self):
        self.browser.set_window_size(1920, 1080)

    # Fetch webpage
    def fetch_page(self, url):
        self.browser.get(url)

    # Save screenshot
    def save_screenshot(self, output):
        self.browser.save_screenshot(output)

    # Quit browser
    def quit(self):
        self.browser.quit()