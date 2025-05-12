"""
This module contain the code for backend,
that will handle scraping process
"""

from time import sleep
from scraper.base import Base
from scraper.scroller import Scroller
import undetected_chromedriver as uc
from settings import DRIVER_EXECUTABLE_PATH
from scraper.communicator import Communicator


class Backend(Base):

    def __init__(self, searchquery, outputformat, latitude, longitude, healdessmode):
        self.searchquery = searchquery  # search query that user will enter
        self.latitude = latitude
        self.longitude = longitude
        self.headlessMode = healdessmode

        self.init_driver()
        self.scroller = Scroller(driver=self.driver)
        self.init_communicator()

    def init_communicator(self):
        Communicator.set_backend_object(self)

    def init_driver(self):
        options = uc.ChromeOptions()
        if self.headlessMode == 1:
            options.headless = True

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        Communicator.show_message(
            "Wait checking for driver...\nIf you don't have webdriver in your machine it will install it")

        try:
            if DRIVER_EXECUTABLE_PATH is not None:
                self.driver = uc.Chrome(
                    driver_executable_path=DRIVER_EXECUTABLE_PATH, options=options)

            else:
                self.driver = uc.Chrome(options=options)

        except NameError:
            self.driver = uc.Chrome(options=options)

        Communicator.show_message("Opening browser...")
        self.driver.maximize_window()
        self.driver.implicitly_wait(self.timeout)

    def mainscraping(self):
        try:
            # Prepare the search query
            querywithplus = "+".join(self.searchquery.split())

            # Use the latitude and longitude for a location-based search
            if self.latitude and self.longitude:
                link_of_page = (
                    f"https://www.google.com/maps/search/{querywithplus}/"
                    f"@{self.latitude},{self.longitude},15z/"
                )
            else:
                link_of_page = f"https://www.google.com/maps/search/{querywithplus}/"

            Communicator.show_message(
                f"Searching for '{self.searchquery}' at {self.latitude}, {self.longitude}")

            # Open the URL
            self.openingurl(url=link_of_page)

            Communicator.show_message("Working start...")

            sleep(1)

            # Start scrolling and scraping
            self.scroller.scroll()

        except Exception as e:
            Communicator.show_message(
                f"Error occurred while scraping. Error: {str(e)}")

        finally:
            try:
                Communicator.show_message("Closing the driver")
                self.driver.close()
                self.driver.quit()
            except:
                pass

            Communicator.end_processing()
            Communicator.show_message("Now you can start another session")
