from seleniumbase import BaseCase

class TestSearchProduct(BaseCase):
    """These test cases test whether the website returns any results if users
       type valid, invalid, special keyword, and verify if the website automatically 
       recommend other searching keyword to users"""

    def setUp(self):
        super().setUp()
        print()
        print("---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Professor's Style: Ensure page stability
        self.wait_for_element_present("body")
        
        # Handle the common "Continue Shopping" interruption
        if self.is_element_visible('button[alt="Continue shopping"]'):
            self.click('button[alt="Continue shopping"]')
        
        # Verify search bar is ready before proceeding
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=15)

    def tearDown(self):        
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC01(self):
        """The test verifies if the website returns the result of products when searching valid search keyword"""
        search_bar = 'input[name="field-keywords"]'
        
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "laptop\n") # Using \n is faster/cleaner than clicking submit separately

        # Professor's Style: Check for the container specifically
        product_selector = 'div[data-component-type="s-search-result"]'
        self.wait_for_element_visible(product_selector, timeout=15)
        
        # Explicitly verify the count is at least 1
        results = self.find_elements(product_selector)
        if len(results) > 0:
            print(f"Success: {len(results)} products found.")
        else:
            self.fail("Search results container appeared but no products were found.")
            
        self.save_screenshot("TC01_valid_search.png", "Test Case Screenshots")

    def test_case_TC02(self):
        """The test verifies if the website returns the result of products when searching invalid keyword"""
        search_bar = 'input[name="field-keywords"]'
        invalid_key = "wfhhr2h3iuh32ih23iuwdhfi"
        
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, invalid_key + "\n") 
        
        # Professor's Style: Use wait_for_text to confirm the "No results" message
        self.wait_for_element_present(".s-main-slot", timeout=15)
        no_results_selector = ".s-no-results-info-bar, .s-result-list-placeholder"
        try:
            # We look for the general message first
            self.wait_for_text("No results for", "body", timeout=10)
            print("Confirmed: 'No results' message is displayed.")
            
            # 4. Defensive check for the specific keyword
            if self.is_text_visible(invalid_key):
                print(f"Success: Specific keyword '{invalid_key}' is mentioned in the error message.")
            else:
                print("Note: 'No results' found, but the UI did not echo back the exact invalid string.")
                
        except Exception:
            # Fallback: Maybe Amazon showed "Try these instead" results?
            if self.is_element_visible(".a-section.a-spacing-base.a-spacing-top-medium"):
                 print("Amazon showed zero results but suggested other categories.")
            else:
                self.fail("Search did not trigger a 'No Results' state as expected.")

        self.save_screenshot("TC02_invalid_search.png", "Test Case Screenshots")

    def test_case_TC03(self):
        """The test verifies results for special characters by handling both success and empty states"""
        search_bar = 'input[name="field-keywords"]'
        special_key = "@!#$"
        
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, special_key + "\n") 
        
        # 1. Wait for the main results area to be present (it exists in both scenarios)
        self.wait_for_element_present("#search", timeout=15)
        
        # 2. Define the "Fingerprints"
        # If there ARE results, Amazon uses this class for the product tiles
        results_selector = 'div[data-component-type="s-search-result"]'
        # If there are NO results, Amazon uses this class for the info bar
        no_results_selector = '.s-no-results-info-bar'

        # 3. Decision Logic
        if self.is_element_visible(results_selector):
            # SITUATION A: Have Results
            print(f"Outcome: Results were found for '{special_key}'")
            # Assert that at least one product is displayed
            self.assert_element(results_selector)
            # Optional: Assert that the result count text is visible
            self.assert_element_visible('span.a-section.a-spacing-small.a-spacing-top-small')
            
        elif self.is_element_visible(no_results_selector) or self.is_text_visible("No results for"):
            # SITUATION B: No Results
            print(f"Outcome: No results found for '{special_key}' (Expected for some special chars)")
            # Assert the "No results" message exists
            self.assert_element(no_results_selector)
            # Verify the specific keyword is mentioned in the failure message
            self.assert_text(special_key, "body")

        else:
            # SITUATION C: Unexpected State (e.g., Robot Check or Captcha)
            self.fail("Search did not land on a standard Results or No-Results page.")

        self.save_screenshot("TC03_special_chars_final.png", "Test Case Screenshots")

    def test_case_TC04(self):
        """The test verifies the search suggestion flyout appears when typing"""
        search_bar = 'input[name="field-keywords"]'
        
        self.wait_for_element_visible(search_bar)
        self.click(search_bar) 
        self.send_keys(search_bar, "lapto") # Typing partial word to trigger flyout
        
        # Target the suggestion container
        suggestion_pane = ".left-pane-results-container"
        self.wait_for_element_visible(suggestion_pane, timeout=10)
        
        # Professor's Style: Check for content inside the flyout
        suggestions = self.find_elements(f"{suggestion_pane} .s-suggestion-container")
        if len(suggestions) > 0:
            print(f"Suggestions flyout active with {len(suggestions)} options.")
        else:
            self.fail("Suggestion pane appeared but it was empty.")
        
        self.save_screenshot("TC04_suggestions.png", "Test Case Screenshots")