from seleniumbase import BaseCase

class TestSearchFilter(BaseCase):
    """These test cases verify whether the website returns the result of products
        satisfying the criteria mentioned in the filters."""

    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Stability: Wait for body and handle potential pop-ups
        self.wait_for_element_present("body")
        self.click_if_visible('button[alt="Continue shopping"]') 
        
        # Wait for search bar to ensure navigation is ready
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):        
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC09(self):
        """Verify multi-filter application: Unisex, Black Color, and Size M"""
        
        # 1. Search for 'clothes'
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "clothes\n") 

        # Professor's Strategy: Define a list of static selectors
        # This makes the code cleaner and easier to extend for more filters
        filters = [
            'a[aria-label="Apply Unisex filter to narrow results"]',
            'a[aria-label="Apply Black filter to narrow results"]',
            'button[value="M"]'
        ]

        # 2. Iterate through filters with high-stability logic
        for i, filter_selector in enumerate(filters, 1):
            # Wait for the specific filter to appear in the DOM after the previous refresh
            self.wait_for_element_visible(filter_selector, timeout=15)
            
            # Professional 'Nudge': Scroll and move slightly up to avoid fixed headers
            self.scroll_to_element(filter_selector)
            self.execute_script("window.scrollBy(0, -150);") 
            
            # JavaScript Click: Ensures the click registers even if a loading overlay exists
            self.js_click(filter_selector)
            
            # Descriptive Screenshot for each filter state
            self.save_screenshot(f"TC09_0{i}_Filter_Applied.png", "Test Case Screenshots")
            
            # Smart Wait: Wait for the AJAX 'spinning' or loading to settle
            self.wait_for_element_present("body")
            self.sleep(2) 

        # 3. Final Verification
        # Ensure the results container is visible after all filters are active
        self.wait_for_element_visible('div[data-component-type="s-search-result"]', timeout=10)
        
        self.save_screenshot("TC09_04_Final_Filtered_Results.png", "Test Case Screenshots")
        print("Successfully validated multi-filter application for clothes.")

    def test_case_TC10(self):
        """Verify that a user can successfully clear all applied filters"""
        
        # 1. Search for 'clothes'
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "clothes\n") 

        # 2. Apply a filter to make the "Clear" option appear
        # We use the same selector that we know works from TC09
        unisex_filter = 'a[aria-label="Apply Unisex filter to narrow results"]'
        self.wait_for_element_visible(unisex_filter, timeout=10)
        self.js_click(unisex_filter)
        
        # Professional Wait: Ensure the page refreshes before looking for "Clear"
        self.wait_for_element_present("body")
        self.save_screenshot("TC10_01_Filter_Applied.png", "Test Case Screenshots")
        
        # 3. Locate and click the "Clear" link
        # Professor's Tip: Use a specific selector for the "Clear" link in the filter sidebar
        clear_link = 'a:contains("Clear")'
        
        if self.is_element_visible(clear_link):
            self.wait_for_element_visible(clear_link, timeout=10)
            self.js_click(clear_link)
            
            # 4. Final Verification: Ensure the "Clear" button is gone after clicking
            # This proves the filters were actually reset
            self.wait_for_element_not_visible(clear_link, timeout=10)
            print("Successfully cleared applied filters.")
        else:
            # If the link isn't there, we take a debug screenshot
            self.save_screenshot("TC10_Error_Clear_Not_Found.png", "Test Case Screenshots")
            self.fail("Clear link was not found after applying filter.")

        # Final state check
        self.save_screenshot("TC10_02_Filters_Cleared_Final.png", "Test Case Screenshots")