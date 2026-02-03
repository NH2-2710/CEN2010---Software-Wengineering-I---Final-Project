from seleniumbase import BaseCase

class TestSearchProduct(BaseCase):
    """
    Automated search functionality tests.
    Covers valid, invalid, and special character inputs, 
    plus the auto-suggestion logic.
    """

    def setUp(self):
        super().setUp()
        print("\n--- Initializing Test Environment ---")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Make sure the DOM is fully ready
        self.wait_for_element_present("body")
        
        # Clear the "Continue shopping" splash screen if it blocks the UI
        if self.is_element_visible('button[alt="Continue shopping"]'):
            self.click('button[alt="Continue shopping"]')
        
        # Wait until the search input is interactable
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):        
        # Cleanup cookies and storage to keep tests isolated
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("--- Test Session Finished ---")

    def test_case_TC01(self):
        """Standard search: Verify that a valid keyword returns products."""
        search_bar = 'input[name="field-keywords"]'
        
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "laptop\n") 

        # Look for the specific search result container
        product_selector = 'div[data-component-type="s-search-result"]'
        self.wait_for_element_visible(product_selector, timeout=15)
        
        # Verify we actually got items back
        results = self.find_elements(product_selector)
        if len(results) > 0:
            print(f"Verified: Found {len(results)} items in results.")
        else:
            self.fail("The search container loaded, but the list is empty.")
            
        self.save_screenshot("TC01_valid_search.png", "Test Case Screenshots")

    def test_case_TC02(self):
        """Negative testing: Verify 'No results' state for gibberish input."""
        search_bar = 'input[name="field-keywords"]'
        invalid_key = "wfhhr2h3iuh32ih23iuwdhfi"
        
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, invalid_key + "\n") 
        
        # Wait for the results section to update
        self.wait_for_element_present(".s-main-slot", timeout=15)
        
        try:
            # Check for the expected error messaging
            self.wait_for_text("No results for", "body", timeout=10)
            print("UI correctly identified 0 results.")
            
            # Double check if the UI actually mentions our invalid string
            if self.is_text_visible(invalid_key):
                print(f"Confirmed: The input string '{invalid_key}' is visible in the error message.")
            else:
                print("Warning: No results found, but the input string isn't printed on screen.")
                
        except Exception:
            # Fallback check: Sometimes Amazon shows 'Try these' or 'Suggested' items instead
            if self.is_element_visible(".a-section.a-spacing-base.a-spacing-top-medium"):
                 print("Zero direct matches found, but suggestions were displayed.")
            else:
                self.fail("Test failed: The search didn't land on a 'No Results' state.")

        self.save_screenshot("TC02_invalid_search.png", "Test Case Screenshots")

    def test_case_TC03(self):
        """Special characters: Handle cases where symbols might return results or errors."""
        search_bar = 'input[name="field-keywords"]'
        special_key = "@!#$"
        
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, special_key + "\n") 
        
        # Standard wait for the search container to be present in the DOM
        self.wait_for_element_present("#search", timeout=15)
        
        # Define identifiers for success vs. empty states
        results_selector = 'div[data-component-type="s-search-result"]'
        no_results_selector = '.s-no-results-info-bar'

        # Determine which page state we landed on
        if self.is_element_visible(results_selector):
            # Branch A: Results exist
            print(f"Note: Amazon found matches for the special characters '{special_key}'")
            self.assert_element(results_selector)
            self.assert_element_visible('span.a-section.a-spacing-small.a-spacing-top-small')
            
        elif self.is_element_visible(no_results_selector) or self.is_text_visible("No results for"):
            # Branch B: No results (this is also an acceptable pass)
            print(f"Note: No results found for '{special_key}', as expected.")
            self.assert_element(no_results_selector)
            self.assert_text(special_key, "body")

        else:
            # Branch C: Neither state found (could be a captcha or unexpected UI change)
            self.fail("Landed on an unknown page state after special character search.")

        self.save_screenshot("TC03_special_chars_final.png", "Test Case Screenshots")

    def test_case_TC04(self):
        """Flyout Menu: Verify the search suggestions appear after partial typing."""
        search_bar = 'input[name="field-keywords"]'
        
        self.wait_for_element_visible(search_bar)
        self.click(search_bar) 
        self.send_keys(search_bar, "lapto") 
        
        # Wait for the suggestion dropdown to appear
        suggestion_pane = ".left-pane-results-container"
        self.wait_for_element_visible(suggestion_pane, timeout=10)
        
        # Confirm that the pane actually contains suggestion rows
        suggestions = self.find_elements(f"{suggestion_pane} .s-suggestion-container")
        if len(suggestions) > 0:
            print(f"Verified: Suggestion flyout contains {len(suggestions)} options.")
        else:
            self.fail("The suggestion pane opened, but no keywords were found inside.")
        
        self.save_screenshot("TC04_suggestions.png", "Test Case Screenshots")