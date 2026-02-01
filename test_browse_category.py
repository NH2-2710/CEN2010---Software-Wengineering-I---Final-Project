from seleniumbase import BaseCase

class TestBrowseCategory(BaseCase):
    """These test cases verify whether users can search products by browsing to 
        various categories and can scroll up and down"""
    
    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Stability: Wait for page load and handle potential interruptions
        self.wait_for_element_present("body")
        self.click_if_visible('button[alt="Continue shopping"]') 
        
        # Ensure the hamburger menu is visible before starting
        self.wait_for_element_visible("#nav-hamburger-menu", timeout=15)
        self.sleep(5)

    def tearDown(self):        
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC05(self):
        """Verify visibility and scrollability of the category side-menu"""
        # Open Menu
        self.click("#nav-hamburger-menu", timeout = 15)
        # Wait for the main menu container first
        self.wait_for_element_visible("#hmenu-canvas", timeout = 10)

        menu_selector = 'div.hmenu-visible[data-menu-id="1"]'
        self.wait_for_element_visible(menu_selector, timeout=10)
        
        # Professor's Style: Get scroll height dynamically
        total_height = self.execute_script(f"return document.querySelector('{menu_selector}').scrollHeight")

        if not total_height:
            self.fail("Could not calculate the scroll height of the menu.")

        print(f"Menu scroll height: {total_height}px")

        # Systematic Scroll Down
        for pos in range(0, total_height, 400):
            self.execute_script(f"document.querySelector('{menu_selector}').scrollTop = {pos}")
            self.sleep(0.2)
        
        self.save_screenshot("TC05_scrolled_down.png", "Test Case Screenshots")

        # Systematic Scroll Up
        for pos in range(total_height, -400, -400):
            self.execute_script(f"document.querySelector('{menu_selector}').scrollTop = {pos}")
            self.sleep(0.2)

        self.save_screenshot("TC05_scrolled_up.png", "Test Case Screenshots")

    def test_case_TC06(self):
        """Verify navigation: Electronics --> Wearable Technology"""
        # 1. Open the side menu using the ARIA label
        # This is more robust than an ID because labels are for accessibility and rarely change
        menu_button = 'a[aria-label="Open All Categories Menu"]'
        self.wait_for_element_visible(menu_button, timeout=15)
        
        # We use js_click to ensure the 'flex' layout doesn't block the click event
        self.js_click(menu_button)
        
        # 2. Wait for the menu container to be 'present' in the DOM
        # Instead of waiting for visibility (which fails during animations), 
        # we wait for the content to exist.
        self.wait_for_element_present("#hmenu-content", timeout=10)
        
        # 3. Navigate to Electronics
        # Using a partial text match for maximum stability
        electronics_link = "a:contains('Electronics')"
        self.wait_for_element_visible(electronics_link, timeout=10)
        self.js_click(electronics_link)

        # 4. Navigate to Wearable Technology
        # We wait for the sub-menu animation to settle
        wearable_link = "a:contains('Wearable Technology')"
        self.wait_for_element_visible(wearable_link, timeout=10)
        self.js_click(wearable_link)

        # 5. Final Verification
        # Check that we landed on the correct category page
        self.wait_for_element_present("#search, .s-main-slot", timeout=15)
        self.assert_text_visible("Wearable Technology", timeout=10)
        self.assert_element_not_visible("#auth-error-message-box")
        
        self.save_screenshot("TC06_final_navigation.png", "Test Case Screenshots")
        print("Successfully validated 'Wearable Technology' landing page.")

    def test_case_TC07(self):
        """Verify navigation: See All --> Home and Kitchen --> Kids' Home Store"""
        # 1. Open the side menu using the ARIA label
        menu_button = 'a[aria-label="Open All Categories Menu"]'
        self.wait_for_element_visible(menu_button, timeout=15)
        self.js_click(menu_button)
        
        # 2. Wait for the menu container (Professional Wait)
        self.wait_for_element_present("#hmenu-content", timeout=10)

        # 3. Expand "See All" (Using your verified original attribute)
        see_all_btn = 'a[aria-label="See all"]'
        self.wait_for_element_visible(see_all_btn, timeout=10)
        self.scroll_to_element(see_all_btn)
        self.js_click(see_all_btn)

        # 4. Select 'Home and Kitchen' (Using your verified static ID)
        home_kitchen = 'a[data-menu-id="18"]'
        self.wait_for_element_visible(home_kitchen, timeout=10)
        self.scroll_to_element(home_kitchen)
        self.js_click(home_kitchen)

        # 5. Select 'Kids' Home Store' (Using your verified static href)
        kids_home = 'a[href*="kids_home_store"]'
        self.wait_for_element_visible(kids_home, timeout=10)
        self.scroll_to_element(kids_home)
        self.js_click(kids_home)

        # 6. Final Verification (Fixing the CSS SyntaxError)
        # We wait for the results container so we don't rely on a missing <h1>
        self.wait_for_element_present("#search, .s-main-slot", timeout=15)
        
        # IMPORTANT: We split the text to avoid the "Unclosed string" apostrophe bug
        self.assert_text_visible("Kids", timeout=10)
        self.assert_text_visible("Home Store", timeout=10)
        
        self.save_screenshot("TC07_kids_home_final.png", "Test Case Screenshots")
        print("Successfully reached and validated Kids' Home Store.")

    def test_case_TC08(self):
        """The test verifies if users can go back to the main menu 
        after browsing to sub categories"""

        # 1. Open Menu
        self.click("#nav-hamburger-menu")
        self.wait_for_element_visible('#hmenu-content', timeout=10)
        
        # 2. Expand 'See all'
        see_all_btn = 'a[aria-label="See all"]'
        self.wait_for_element_visible(see_all_btn, timeout=10)
        self.js_click(see_all_btn)
        
        # 3. Navigate into sub-menu (ID 18)
        self.wait_for_element_visible('a[data-menu-id="18"]', timeout=10)
        self.js_click('a[data-menu-id="18"]')
        self.save_screenshot("TC08_SubMenu_Entered.png", "Test Case Screenshots")
        
        # 4. Click Back
        back_btn = 'a[aria-label="Back to main menu"]'
        self.wait_for_element_visible(back_btn, timeout=10)
        self.js_click(back_btn)
        self.sleep(5)
        self.save_screenshot("TC08_MainMenu_BlankError.png", "Test Case Screenshots")
        
        # 5. Safe Scroll Reset
        self.execute_script("""
            var menu = document.querySelector('ul.hmenu-visible');
            if (menu) { menu.scrollTop = 0; }
        """)
        
        # 6. Final Verification
        self.wait_for_element_visible('#hmenu-content', timeout=10)
        self.assert_text_visible("shop by department", timeout=10)
        self.save_screenshot("TC08_Returned_To_Main_Menu.png", "Test Case Screenshots")