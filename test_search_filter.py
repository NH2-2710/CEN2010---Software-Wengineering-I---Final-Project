from seleniumbase import BaseCase

class TestSearchFilter(BaseCase):
    """
    Tests for the search sidebar filters.
    Checking if we can stack multiple criteria (color, size, gender)
    and if the 'Clear' functionality actually resets the results.
    """

    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Standard check to ensure we aren't looking at a blank white page
        self.wait_for_element_present("body")
        
        # Get rid of that annoying 'Continue shopping' overlay if it pops up
        self.click_if_visible('button[alt="Continue shopping"]') 
        
        # Make sure the search bar is actually there before we try to type
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):         
        # Housekeeping: wipe the session so the next test doesn't inherit weird states
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC09(self):
        """Verify we can apply Unisex, Black, and Size M filters all at once."""
        
        # Kick off with a broad search for clothes
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "clothes\n") 

        # I'm putting these in a list so I can loop through them easily.
        # This keeps the main logic from being repetitive.
        filters = [
            'a[aria-label="Apply Unisex filter to narrow results"]',
            'a[aria-label="Apply Black filter to narrow results"]',
            'button[value="M"]'
        ]

        # Loop through each filter and click 'em one by one
        for i, filter_selector in enumerate(filters, 1):
            # Need to wait for the page to refresh and the next filter to be clickable
            self.wait_for_element_visible(filter_selector, timeout=15)
            
            # Use a little nudge: scroll to the element but move up a bit
            # so the sticky Amazon header doesn't cover the button.
            self.scroll_to_element(filter_selector)
            self.execute_script("window.scrollBy(0, -150);") 
            
            # Using JS click here as a safety net in case of loading overlays
            self.js_click(filter_selector)
            
            # Take a shot after each click so I can track the progress in the logs
            self.save_screenshot(f"TC09_0{i}_Filter_Applied.png", "Test Case Screenshots")
            
            # Give the AJAX results a second to settle before the next loop
            self.wait_for_element_present("body")
            self.sleep(2) 

        # Final check: make sure we actually see products in the results area
        self.wait_for_element_visible('div[data-component-type="s-search-result"]', timeout=10)
        
        self.save_screenshot("TC09_04_Final_Filtered_Results.png", "Test Case Screenshots")
        print("Successfully validated multi-filter application for clothes.")

    def test_case_TC10(self):
        """Make sure the 'Clear' link actually appears and resets the search."""
        
        # Start with the same base search
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "clothes\n") 

        # Apply a quick filter just to trigger the 'Clear' option in the UI
        unisex_filter = 'a[aria-label="Apply Unisex filter to narrow results"]'
        self.wait_for_element_visible(unisex_filter, timeout=10)
        self.js_click(unisex_filter)
        
        # Wait for the page to update
        self.wait_for_element_present("body")
        self.save_screenshot("TC10_01_Filter_Applied.png", "Test Case Screenshots")
        
        # Now look for that 'Clear' link in the sidebar
        clear_link = 'a:contains("Clear")'
        
        if self.is_element_visible(clear_link):
            self.wait_for_element_visible(clear_link, timeout=10)
            self.js_click(clear_link)
            
            # If clicking 'Clear' worked, the link itself should disappear
            self.wait_for_element_not_visible(clear_link, timeout=10)
            print("Successfully cleared applied filters.")
        else:
            # Troubleshooting step: if 'Clear' didn't show up, something went wrong
            self.save_screenshot("TC10_Error_Clear_Not_Found.png", "Test Case Screenshots")
            self.fail("Clear link was not found after applying filter.")

        # Final check of the clean state
        self.save_screenshot("TC10_02_Filters_Cleared_Final.png", "Test Case Screenshots")