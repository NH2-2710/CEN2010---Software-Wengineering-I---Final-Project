from seleniumbase import BaseCase

class TestPaginate(BaseCase):
    """These test cases verify pagination functionality: switching via page numbers and arrows."""

    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Stability: Wait for the body and handle the "Continue shopping" pop-up
        self.wait_for_element_present("body")
        if self.is_element_visible('button[alt="Continue shopping"]'):
            self.click('button[alt="Continue shopping"]')
        
        # Ensure search bar is ready to avoid "element not found" errors
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):        
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def perform_search(self, keyword="Bag"):
        """Helper method to reduce redundancy in search steps"""
        search_bar = 'input[name="field-keywords"]'
        self.type(search_bar, f"{keyword}\n")
        # Wait for the result container to ensure the first page is loaded
        self.wait_for_element_visible('div[data-component-type="s-search-result"]', timeout=15)

    def test_case_TC13(self):
        """Verify switching to page 3 via page number"""
        self.perform_search("Bag")

        # 1. Scroll to pagination
        pagination_bar = 'span.s-pagination-strip'
        self.wait_for_element_visible(pagination_bar, timeout=10)
        self.scroll_to_element(pagination_bar)
        self.sleep(5)
        self.save_screenshot("TC13_page1_pagination.png", "Test Case Screenshots")

        # 2. Click Page 3
        page_3_selector = 'a[aria-label="Go to page 3"]'
        self.wait_for_element_clickable(page_3_selector)
        self.click(page_3_selector)
        self.sleep(5)

        # 3. Verification: Check if the '3' button is now the current page (aria-current="page")
        # In Professor's style, we verify the UI state changed
        self.scroll_to_element(pagination_bar)
        current_page_selector = 'span.s-pagination-selected[aria-label="Page 3"]'
        self.wait_for_element_visible(current_page_selector, timeout=10)
        
        self.scroll_to_element(pagination_bar)
        self.save_screenshot("TC13_page3_verified.png", "Test Case Screenshots")
        print("Successfully navigated to Page 3.")

    def test_case_TC14(self):
        """Verify switching from page 3 back to page 1"""
        self.perform_search("Bag")

        # 1. Go to page 3 first
        self.scroll_to_element('span.s-pagination-strip')
        self.click('a[aria-label="Go to page 3"]')
        self.wait_for_element_visible('span[aria-label="Page 3"]')

        # 2. Return to page 1
        page_1_selector = 'a[aria-label="Go to page 1"]'
        self.scroll_to_element(page_1_selector)
        self.click(page_1_selector)

        # 3. Verify Page 1 is active
        self.wait_for_element_visible('span[aria-label="Page 1"]', timeout=10)
        self.scroll_to_element(page_1_selector)
        self.save_screenshot("TC14_back_to_page1.png", "Test Case Screenshots")
        print("Successfully came back to Page 1.")

    def test_case_TC15(self):
        """Verify switching to the next page using the 'Next' arrow"""
        self.perform_search("Bag")

        # 1. Locate and Click 'Next'
        next_arrow = 'a.s-pagination-next'
        self.scroll_to_element(next_arrow)
        self.wait_for_element_clickable(next_arrow)
        self.click(next_arrow)

        # 2. Verify we are now on Page 2
        self.wait_for_element_visible('span[aria-label="Page 2"]', timeout=10)
        self.scroll_to_element(next_arrow)
        self.save_screenshot("TC15_next_page_arrow.png", "Test Case Screenshots")

    def test_case_TC16(self):
        """Verify switching to the previous page using the 'Previous' arrow"""
        self.perform_search("Bag")

        # 1. Go to Page 2 first so the 'Previous' arrow appears
        self.scroll_to_element('a.s-pagination-next')
        self.click('a.s-pagination-next')
        self.wait_for_element_visible('span[aria-label="Page 2"]')
        self.sleep(5)

        # 2. Click 'Previous'
        prev_arrow ='[class*="s-pagination-prev"]'
        self.scroll_to_element(prev_arrow)
        self.click(prev_arrow)

        # 3. Verify return to Page 1
        self.wait_for_element_visible('span[aria-label="Page 1"]', timeout=10)
        self.scroll_to_element(prev_arrow)
        self.save_screenshot("TC16_prev_page_arrow.png", "Test Case Screenshots")