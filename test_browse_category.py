from seleniumbase import BaseCase

class TestBrowseCategory(BaseCase):
    """
    Tests for category navigation and side-menu behavior.
    Checks if we can scroll the menu properly, navigate deep into sub-categories,
    and return to the starting point without the UI breaking.
    """
    
    def setUp(self):
        super().setUp()
        print("\n---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Standard check to make sure the page actually loaded
        self.wait_for_element_present("body")
        
        # Close the "Continue shopping" pop-up if it appears so it doesn't block clicks
        self.click_if_visible('button[alt="Continue shopping"]') 
        
        # Hamburger menu is our main anchor, need to make sure it's ready
        self.wait_for_element_visible("#nav-hamburger-menu", timeout=15)
        self.sleep(5)

    def tearDown(self):         
        # Clean out everything so the next test starts with a fresh session
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")

    def test_case_TC05(self):
        """Make sure the side menu is actually scrollable in both directions."""
        # Get the menu open
        self.click("#nav-hamburger-menu", timeout = 15)
        self.wait_for_element_visible("#hmenu-canvas", timeout = 10)

        # Target the specific active menu pane
        menu_selector = 'div.hmenu-visible[data-menu-id="1"]'
        self.wait_for_element_visible(menu_selector, timeout=10)
        
        # Need to know how far we can actually scroll
        total_height = self.execute_script(f"return document.querySelector('{menu_selector}').scrollHeight")

        if not total_height:
            self.fail("Could not calculate the scroll height of the menu.")

        print(f"Menu scroll height: {total_height}px")

        # Scroll down in chunks so we can see the movement in the logs/screenshots
        for pos in range(0, total_height, 400):
            self.execute_script(f"document.querySelector('{menu_selector}').scrollTop = {pos}")
            self.sleep(0.2)
        
        self.save_screenshot("TC05_scrolled_down.png", "Test Case Screenshots")

        # Now scroll back up to the top to make sure it doesn't get stuck
        for pos in range(total_height, -400, -400):
            self.execute_script(f"document.querySelector('{menu_selector}').scrollTop = {pos}")
            self.sleep(0.2)

        self.save_screenshot("TC05_scrolled_up.png", "Test Case Screenshots")

    def test_case_TC06(self):
        """Navigate through Electronics to Wearable Tech and verify the landing page."""
        # Using aria-label here because IDs in this menu can be a bit flaky
        menu_button = 'a[aria-label="Open All Categories Menu"]'
        self.wait_for_element_visible(menu_button, timeout=15)
        
        # js_click helps if the menu is partially covered by a transparent layer
        self.js_click(menu_button)
        
        # Wait for the DOM to update with the menu content
        self.wait_for_element_present("#hmenu-content", timeout=10)
        
        # Find and click 'Electronics'
        electronics_link = "a:contains('Electronics')"
        self.wait_for_element_visible(electronics_link, timeout=10)
        self.js_click(electronics_link)

        # Move deeper into 'Wearable Technology'
        wearable_link = "a:contains('Wearable Technology')"
        self.wait_for_element_visible(wearable_link, timeout=10)
        self.js_click(wearable_link)

        # Confirm the page actually loaded the right content
        self.wait_for_element_present("#search, .s-main-slot", timeout=15)
        self.assert_text_visible("Wearable Technology", timeout=10)
        
        # Make sure no random error boxes popped up during navigation
        self.assert_element_not_visible("#auth-error-message-box")
        
        self.save_screenshot("TC06_final_navigation.png", "Test Case Screenshots")
        print("Successfully validated 'Wearable Technology' landing page.")

    def test_case_TC07(self):
        """Check the path: See All -> Home and Kitchen -> Kids' Home Store."""
        menu_button = 'a[aria-label="Open All Categories Menu"]'
        self.wait_for_element_visible(menu_button, timeout=15)
        self.js_click(menu_button)
        
        self.wait_for_element_present("#hmenu-content", timeout=10)

        # Need to expand the menu first to see the full list
        see_all_btn = 'a[aria-label="See all"]'
        self.wait_for_element_visible(see_all_btn, timeout=10)
        self.scroll_to_element(see_all_btn)
        self.js_click(see_all_btn)

        # Home & Kitchen is under menu ID 18
        home_kitchen = 'a[data-menu-id="18"]'
        self.wait_for_element_visible(home_kitchen, timeout=10)
        self.scroll_to_element(home_kitchen)
        self.js_click(home_kitchen)

        # Using a partial href match for the Kids' Home Store link
        kids_home = 'a[href*="kids_home_store"]'
        self.wait_for_element_visible(kids_home, timeout=10)
        self.scroll_to_element(kids_home)
        self.js_click(kids_home)

        # Verification step
        self.wait_for_element_present("#search, .s-main-slot", timeout=15)
        
        # Checking for "Kids" and "Home Store" separately to avoid issues with the apostrophe in the locator
        self.assert_text_visible("Kids", timeout=10)
        self.assert_text_visible("Home Store", timeout=10)
        
        self.save_screenshot("TC07_kids_home_final.png", "Test Case Screenshots")
        print("Successfully reached and validated Kids' Home Store.")

    def test_case_TC08(self):
        """Verify the 'Back' button works and returns us to the main 'shop by department' list."""

        self.click("#nav-hamburger-menu")
        self.wait_for_element_visible('#hmenu-content', timeout=10)
        
        # Expand menu to find our target category
        see_all_btn = 'a[aria-label="See all"]'
        self.wait_for_element_visible(see_all_btn, timeout=10)
        self.js_click(see_all_btn)
        
        # Go into Home & Kitchen sub-menu
        self.wait_for_element_visible('a[data-menu-id="18"]', timeout=10)
        self.js_click('a[data-menu-id="18"]')
        self.save_screenshot("TC08_SubMenu_Entered.png", "Test Case Screenshots")
        
        # Hit the back button to return to the main list
        back_btn = 'a[aria-label="Back to main menu"]'
        self.wait_for_element_visible(back_btn, timeout=10)
        self.js_click(back_btn)
        self.sleep(5)
        
        # Reset scroll position via JS just in case the menu gets stuck in a blank spot
        self.execute_script("""
            var menu = document.querySelector('ul.hmenu-visible');
            if (menu) { menu.scrollTop = 0; }
        """)
        
        # Confirm we are back where we started
        self.wait_for_element_visible('#hmenu-content', timeout=10)
        self.assert_text_visible("shop by department", timeout=10)
        self.save_screenshot("TC08_Returned_To_Main_Menu.png", "Test Case Screenshots")