from seleniumbase import BaseCase

class TestPaginate(BaseCase):
    """
    Tests for pagination behavior.
    Checks if we can hop between pages using direct numbers and 
    the 'Next'/'Previous' arrow buttons.
    """

    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Standard check to make sure the site isn't hanging on a blank screen
        self.wait_for_element_present("body")
        
        # Clear the "Continue shopping" overlay if it's blocking the search bar
        if self.is_element_visible('button[alt="Continue shopping"]'):
            self.click('button[alt="Continue shopping"]')
        
        # Don't proceed until the search bar is ready for input
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):         
        # Cleanup cookies so each test starts with a fresh session
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def perform_search(self, keyword="Bag"):
        """Search helper to keep the test cases focused on pagination rather than typing"""
        search_bar = 'input[name="field-keywords"]'
        self.type(search_bar, f"{keyword}\n")
        # Need to see at least one product before we try to scroll to the bottom
        self.wait_for_element_visible('div[data-component-type="s-search-result"]', timeout=15)

    def test_case_TC13(self):
        """Verify we can jump straight to page 3 using the number link."""
        self.perform_search("Bag")

        # Scroll all the way down to find the pagination strip
        pagination_bar = 'span.s-pagination-strip'
        self.wait_for_element_visible(pagination_bar, timeout=10)
        self.scroll_to_element(pagination_bar)
        
        # Give it a moment to load any lazy elements at the footer
        self.sleep(5)
        self.save_screenshot("TC13_page1_pagination.png", "Test Case Screenshots")

        # Click the link for Page 3
        page_3_selector = 'a[aria-label="Go to page 3"]'
        self.wait_for_element_clickable(page_3_selector)
        self.click(page_3_selector)
        
        # Wait for the page refresh to complete
        self.sleep(5)

        # Confirm the '3' is now the selected/active page in the UI
        self.scroll_to_element(pagination_bar)
        current_page_selector = 'span.s-pagination-selected[aria-label="Page 3"]'
        self.wait_for_element_visible(current_page_selector, timeout=10)
        
        self.save_screenshot("TC13_page3_verified.png", "Test Case Screenshots")
        print("Successfully navigated to Page 3.")

    def test_case_TC14(self):
        """Verify we can navigate from page 3 back to page 1."""
        self.perform_search("Bag")

        # Head to page 3 first to set up the 'Back' test
        self.scroll_to_element('span.s-pagination-strip')
        self.click('a[aria-label="Go to page 3"]')
        self.wait_for_element_visible('span[aria-label="Page 3"]')

        # Click back to Page 1
        page_1_selector = 'a[aria-label="Go to page 1"]'
        self.scroll_to_element(page_1_selector)
        self.click(page_1_selector)

        # Verify page 1 is active again
        self.wait_for_element_visible('span[aria-label="Page 1"]', timeout=10)
        self.scroll_to_element(page_1_selector)
        self.save_screenshot("TC14_back_to_page1.png", "Test Case Screenshots")
        print("Successfully came back to Page 1.")

    def test_case_TC15(self):
        """Verify the 'Next' arrow advances the results to the next page."""
        self.perform_search("Bag")

        # Find the Next button at the bottom
        next_arrow = 'a.s-pagination-next'
        self.scroll_to_element(next_arrow)
        self.wait_for_element_clickable(next_arrow)
        self.click(next_arrow)

        # After clicking Next, we should see the Page 2 indicator active
        self.wait_for_element_visible('span[aria-label="Page 2"]', timeout=10)
        self.scroll_to_element(next_arrow)
        self.save_screenshot("TC15_next_page_arrow.png", "Test Case Screenshots")

    def test_case_TC16(self):
        """Verify the 'Previous' arrow returns the user to the preceding page."""
        self.perform_search("Bag")

        # Need to move to Page 2 first so the 'Previous' arrow actually exists in the DOM
        self.scroll_to_element('a.s-pagination-next')
        self.click('a.s-pagination-next')
        self.wait_for_element_visible('span[aria-label="Page 2"]')
        self.sleep(5)

        # Hit the Previous button
        prev_arrow ='[class*="s-pagination-prev"]'
        self.scroll_to_element(prev_arrow)
        self.click(prev_arrow)

        # Confirm we landed back on Page 1
        self.wait_for_element_visible('span[aria-label="Page 1"]', timeout=10)
        self.scroll_to_element(prev_arrow)
        self.save_screenshot("TC16_prev_page_arrow.png", "Test Case Screenshots")