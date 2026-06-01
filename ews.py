import logging
import time
import requests
from PIL import Image
from inky import InkyPHAT

class WebsiteChecker:
    """Manages website checks, image display, and logging."""

    def __init__(self):
        # Display dimensions
        self.width = InkyPHAT.WIDTH
        self.height = InkyPHAT.HEIGHT

        # Initialize display
        self.inky_display = InkyPHAT("red")  # Initialize with "red" color for InkyPhat Red

        # Configure logging
        logging.basicConfig(filename="website_checker.log", level=logging.INFO)

        # Define image paths
        self.image_paths = {
            "startup": "/home/pi/inky/ews/images/ews.png",
            "stratcom_on": "/home/pi/inky/ews/images/stratcom_on.png",
            "stratcom_off": "/home/pi/inky/ews/images/stratcom_off.png",
            "norad_on": "/home/pi/inky/ews/images/norad_on.png",
            "norad_off": "/home/pi/inky/ews/images/norad_off.png",
            "vanguard_on": "/home/pi/inky/ews/images/vanguard_on.png",
            "vanguard_off": "/home/pi/inky/ews/images/vanguard_off.png",
            "success_snv": "/home/pi/inky/ews/images/success_snv.png",
            "fail_snv": "/home/pi/inky/ews/images/fail_snv.png",
        }

        # Define website URLs
        self.website_urls = {
            "stratcom": "https://www.gov.uk/government/organisations/strategic-command",
            "norad": "https://www.norad.mil",
            "vanguard": "https://www.bbc.co.uk/sounds/play/live:bbc_radio_fourfm",
        }

    def display_image(self, path, delay=5):
        """Displays an image on the Inky Phat screen."""
        try:
            print("Displaying image:", path)
            img = Image.open(path)
            self.inky_display.set_image(img)
            self.inky_display.show()
            time.sleep(min(delay, 10))  # Delay after displaying the image, maximum of 10 seconds
        except FileNotFoundError:
            logging.error(f"Error: Image not found: {path}")
            print("Error: Image not found:", path)
        except Exception as e:  # Catch other potential display errors
            logging.error(f"Error displaying image: {e}")
            print("Error displaying image:", e)

    def check_website(self, url):
        """Checks if a website is online and returns True/False."""
        try:
            print("Checking website:", url)
            response = requests.get(url, timeout=10)  # Set timeout to 10 seconds
            print("Response code for", url + ":", response.status_code)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Error checking website {url}: {e}")
            print("Error checking website:", e)
            return False

    def display_final_image(self):
        """Displays the final image based on website statuses."""
        # Check website statuses
        stratcom_status = self.check_website(self.website_urls["stratcom"])
        norad_status = self.check_website(self.website_urls["norad"])
        vanguard_status = self.check_website(self.website_urls["vanguard"])

        # Display the images while checking the websites
        self.display_image(self.image_paths["startup"], delay=5)
        self.display_image(self.image_paths["stratcom_on"] if stratcom_status else self.image_paths["stratcom_off"], delay=10)
        self.display_image(self.image_paths["norad_on"] if norad_status else self.image_paths["norad_off"], delay=10)
        self.display_image(self.image_paths["vanguard_on"] if vanguard_status else self.image_paths["vanguard_off"], delay=10)

        # Construct final image key based on website statuses
        final_image_key = ""
        if not stratcom_status:
            final_image_key += "s"
        if not norad_status:
            final_image_key += "n"
        if not vanguard_status:
            final_image_key += "v"

        # Add "fail_" prefix to the final image key if it's not empty
        if final_image_key:
            final_image_key = "fail_" + final_image_key

        print("Final image key:", final_image_key)

        # Select final image path based on final image key
        final_image_path = self.image_paths.get(final_image_key, self.image_paths["success_snv"])

        # Print final image path for debugging
        print("Final image path:", final_image_path)

        self.display_image(final_image_path)

    def run(self):
        """Main loop for website checks and image updates."""
        while True:
            # Check website statuses and display corresponding images
            self.display_final_image()
            time.sleep(300)  # Wait for 5 minutes (adjust as needed)


if __name__ == "__main__":
    website_checker = WebsiteChecker()
    website_checker.run()