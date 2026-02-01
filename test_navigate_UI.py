from seleniumbase import BaseCase

class TestNavigationUI(BaseCase):
    
    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Professor's Style: Wait for page stability
        self.wait_for_element_present("body")
        
        # Handle the common interruption immediately
        if self.is_element_visible('button[alt="Continue shopping"]'):
            self.click('button[alt="Continue shopping"]')
        
        # Ensure the header is interactive before starting any TC
        self.wait_for_element_visible("#nav-logo-sprites", timeout=15)

    def tearDown(self):        
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC17(self):
        """Verify the logo returns the user to the Home Page"""
        # Navigation away
        self.type('input[name="field-keywords"]', "laptop\n") 
        self.wait_for_element_visible('div[data-component-type="s-search-result"]', timeout=15)
        self.sleep(5)

        # Professor's Verification Strategy
        logo_selector = "#nav-logo-sprites"
        if self.is_element_visible(logo_selector):
            self.js_click(logo_selector)
        else:
            self.fail("Amazon logo not found")

        # Gateway check
        home_indicator = "#gw-layout"
        self.wait_for_element_visible(home_indicator, timeout=15)
        
        if self.is_element_visible(home_indicator):
            print("Confirmed: Return to Home (Gateway) successful.")
        else:
            self.fail("Failed to reach Home Gateway after clicking logo")
        
        self.save_screenshot("TC17_back_home.png", "Test Case Screenshots")

    def test_case_TC18(self):
        """Verify the header search bar is visible and enabled"""
        # Professor's Style: Using the specific ID and manual verification logic
        search_bar = "#twotabsearchtextbox"
        
        # 1. Wait for element to ensure page stability
        self.wait_for_element_present(search_bar, timeout=15)

        # 2. Verification of Visibility and State (Professor's if/else pattern)
        if self.is_element_visible(search_bar):
            print("Search bar is visible on the header")
        else:
            self.fail("Search bar should be visible but it is hidden")

        # 3. Check if enabled and verify placeholder (Professor's attribute logic)
        if self.is_element_enabled(search_bar):
            placeholder = self.get_attribute(search_bar, "placeholder")
            if placeholder and len(placeholder) > 0:
                print(f"Search bar is enabled with placeholder: '{placeholder}'")
            else:
                print("Search bar is enabled but placeholder is empty")
        else:
            self.fail("Search bar found but is not enabled for typing")

        # 4. Final Screenshot and Console Handshake
        self.save_screenshot("TC18_search_bar_status.png", "Test Case Screenshots")
        print("Successfully validated header search bar state.")

    def test_case_TC19(self):
        """Verify the cart icon is clickable and leads to the Cart Page"""
        # Professor's Style: Explicit ID targeting and state verification
        cart_icon = "#nav-cart"
        
        # 1. Wait for element presence to ensure stability
        self.wait_for_element_present(cart_icon, timeout=15)

        # 2. Execution: Verify visibility before interaction (Professor's pattern)
        if self.is_element_visible(cart_icon):
            print("Cart icon is visible on the header")
            self.js_click(cart_icon) # Using robust click to avoid potential overlays
        else:
            self.fail("Cart icon should be visible but it is hidden")

        # 3. Verification: Wait for Cart-specific container first
        # This prevents logic from proceeding before the page has rendered
        cart_container = "#sc-active-cart, .sc-your-amazon-cart-is-empty"
        self.wait_for_element_visible(cart_container, timeout=15)

        if self.is_element_visible(cart_container):
            print("Successfully reached the Cart container")
        else:
            self.fail("Cart page container was not found after clicking icon")

        # 4. Final URL and Text Verification (Professor's if/else check)
        current_url = self.get_current_url()
        if "/cart" in current_url or "/gp/cart" in current_url:
            print(f"URL verified: {current_url}")
        else:
            self.fail(f"URL does not contain '/cart'. Current URL: {current_url}")

        # Final state check for Shopping Cart header
        if self.is_text_visible("Shopping Cart") or self.is_text_visible("Your Amazon Cart is empty"):
            print("Cart page header/content is visible")
        else:
            self.fail("Cart page title text not found")
        
        self.save_screenshot("TC19_cart_page_status.png", "Test Case Screenshots")
        print("Successfully validated Shopping Cart navigation.")