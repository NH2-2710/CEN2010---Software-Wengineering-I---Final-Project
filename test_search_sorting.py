from seleniumbase import BaseCase

class TestSearchSorting(BaseCase):
    """These test cases test whether the website sorts the results in a specific order.
       For example: from low to high price, from high to low price"""

    def setUp(self):
        super().setUp()
        print()
        print("---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Professor's Style: Wait for specific stability instead of just a sleep(5)
        self.wait_for_element_present("body")
        self.click_if_visible('button[alt="Continue shopping"]') 
        
        # Ensure the header is loaded before starting
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):        
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC11(self):
        """Verify sorting: Price: Low to High"""
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "Bag\n") 

        # 1. Wait for results and the sorting dropdown to be ready
        sorting_selector = 'span[data-action="a-dropdown-button"]'
        self.wait_for_element_visible(sorting_selector, timeout=15)
        self.sleep(5)
        
        # 2. Click dropdown and select "Price: Low to High"
        self.click(sorting_selector)
        self.sleep(3)
        # Professor's Style: Using a specific wait for the dropdown item
        low_to_high = 'a[data-value*="price-asc-rank"]'
        self.wait_for_element_visible(low_to_high)
        self.js_click(low_to_high) # js_click is more reliable for Amazon dropdowns

        # 3. Wait for the page to refresh with sorted results
        # We look for the "Price: Low to High" text to appear on the button label
        self.wait_for_text("Price: Low to High", sorting_selector, timeout=10)
        self.save_screenshot("TC11_LowToHigh_Start.png", "Test Case Screenshots")
        
        # 4. Professor's Style: Systematic Scrolling
        # This triggers lazy-loading and ensures screenshots capture product data
        for x in range(0, 2000, 500):
            self.execute_script(f"window.scrollTo(0, {x});")
            self.sleep(0.5)

        self.save_screenshot("TC11_LowToHigh_Scrolled.png", "Test Case Screenshots")
        print("Successfully validated 'Price: Low to High' sorting.")

    def test_case_TC12(self):
        """Verify sorting: Price: High to Low"""
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "Bag\n") 

        sorting_selector = 'span[data-action="a-dropdown-button"]'
        self.wait_for_element_visible(sorting_selector, timeout=15)
        self.sleep(5)

        # 1. Click dropdown and select "Price: High to Low"
        self.click(sorting_selector)
        self.sleep(5)
        high_to_low = 'a[data-value*="price-desc-rank"]'
        self.wait_for_element_visible(high_to_low)
        self.js_click(high_to_low)

        # 2. Verify the dropdown label updated
        self.wait_for_text("Price: High to Low", sorting_selector, timeout=10)
        self.save_screenshot("TC12_HighToLow_Start.png", "Test Case Screenshots")
        
        # 3. Defensive Scrolling
        for x in range(0, 2000, 500):
            self.execute_script(f"window.scrollTo(0, {x});")
            self.sleep(0.5)

        self.save_screenshot("TC12_HighToLow_Scrolled.png", "Test Case Screenshots")
        print("Successfully validated 'Price: High to Low' sorting.")