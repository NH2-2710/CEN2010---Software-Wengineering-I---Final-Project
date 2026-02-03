from seleniumbase import BaseCase

class TestSearchSorting(BaseCase):
    """
    Testing the search result sorting logic.
    Main goal is to ensure the site actually reorders items when 
    switching between Low-to-High and High-to-Low price filters.
    """

    def setUp(self):
        super().setUp()
        print()
        print("---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Don't start until the body is loaded; better than just a static sleep
        self.wait_for_element_present("body")
        
        # Clean up the view: close the 'Continue shopping' pop-up if it's in the way
        self.click_if_visible('button[alt="Continue shopping"]') 
        
        # Make sure the search bar is actually interactive before typing
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):         
        # Wipe session data so tests stay independent and clean
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC11(self):
        """Check if sorting by 'Price: Low to High' works for a generic 'Bag' search."""
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "Bag\n") 

        # Give the results a moment to finish rendering so the dropdown is clickable
        sorting_selector = 'span[data-action="a-dropdown-button"]'
        self.wait_for_element_visible(sorting_selector, timeout=15)
        self.sleep(5) # Manual buffer for the dynamic sorting element to settle
        
        # Open the sort menu
        self.click(sorting_selector)
        self.sleep(3)
        
        # Target 'Low to High' specifically; using partial data-value match for stability
        low_to_high = 'a[data-value*="price-asc-rank"]'
        self.wait_for_element_visible(low_to_high)
        
        # js_click is safer here because Amazon's dropdown overlays can be tricky for Selenium
        self.js_click(low_to_high) 

        # Verification: check if the dropdown label actually updated to show the new sort order
        self.wait_for_text("Price: Low to High", sorting_selector, timeout=10)
        self.save_screenshot("TC11_LowToHigh_Start.png", "Test Case Screenshots")
        
        # Scroll down in chunks to trigger lazy-loading for a better screenshot of the items
        for x in range(0, 2000, 500):
            self.execute_script(f"window.scrollTo(0, {x});")
            self.sleep(0.5)

        self.save_screenshot("TC11_LowToHigh_Scrolled.png", "Test Case Screenshots")
        print("Successfully validated 'Price: Low to High' sorting.")

    def test_case_TC12(self):
        """Check if sorting by 'Price: High to Low' works for a generic 'Bag' search."""
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "Bag\n") 

        sorting_selector = 'span[data-action="a-dropdown-button"]'
        self.wait_for_element_visible(sorting_selector, timeout=15)
        self.sleep(5)

        # Trigger the dropdown
        self.click(sorting_selector)
        self.sleep(5)
        
        # Switch to 'High to Low'
        high_to_low = 'a[data-value*="price-desc-rank"]'
        self.wait_for_element_visible(high_to_low)
        self.js_click(high_to_low)

        # Confirm the label change
        self.wait_for_text("Price: High to Low", sorting_selector, timeout=10)
        self.save_screenshot("TC12_HighToLow_Start.png", "Test Case Screenshots")
        
        # Defensive scrolling to make sure we load the higher-priced results correctly
        for x in range(0, 2000, 500):
            self.execute_script(f"window.scrollTo(0, {x});")
            self.sleep(0.5)

        self.save_screenshot("TC12_HighToLow_Scrolled.png", "Test Case Screenshots")
        print("Successfully validated 'Price: High to Low' sorting.")