from seleniumbase import BaseCase

class TestBrowseCategory(BaseCase):
    """These test cases verify whether users can search products by browsing to 
        various categories and can scroll up and down"""
    
    def setUp(self):
        # Open the Amazon website at the maximum window size and wait
        # for the website to be stable
        super().setUp()
        print()
        print("---- RUNNING BEFORE THE TEST ----")
        self.open("https://www.amazon.com/") 
        self.maximize_window()
        
        # Wait for the body to ensure page load
        self.wait_for_element_present("body")
        
        self.click_if_visible('button[alt="Continue shopping"]') 
        # click "Continue Shopping" to continue, avoiding the program to terminate suddenly
        self.wait_for_element_visible('input[name="field-keywords"]', timeout=10)
        

    def tearDown(self):        
        # Clear all cookies so the next test starts with a fresh login screen
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()
        print("---- END OF TEST ----")


    def test_case_TC17(self):
        search_bar = 'input[name="field-keywords"]'
        self.wait_for_element_visible(search_bar)
        self.type(search_bar, "mac laptop\n") 

        # 1. Wait for ANY product results to load
        product_selector = '//div[@data-component-type="s-search-result"]'
        self.wait_for_element_visible(product_selector, timeout=15)

        # 2. Click the first product title link
        target = '(//div[@data-component-type="s-search-result"]//a[contains(@href,"/dp/")])[1]'

        # 3 Execution
        if self.is_element_present(target):
            self.scroll_to_element(target)
            self.wait_for_element_present(target, timeout=15)
            href = self.get_attribute(target, "href")
            if href and len(href) > 0:
                self.open(href)
            else:
                self.fail("Product link found but href is empty")
        else:
            self.fail("No /dp/ product links found in search results")

        # 4. Verification
        # The product detail page always has an ID "productTitle"
        self.wait_for_element_visible("#productTitle", timeout=15)
        print("Successfully navigated to product details.")

        if self.is_element_visible("#productTitle"):
            print("Product title is visible")
        else:
            self.fail("Product title should be visible but it is hidden")

        title = self.get_text("#productTitle").strip()
        if len(title) > 0:
            print("Product title is not empty")
        else:
            self.fail("Product title is empty")

        # 5. Verify thumbnails exist
        self.wait_for_element_present("#altImages", timeout=15)

        thumb_selector = '#altImages li.imageThumbnail'
        if self.is_element_present(thumb_selector):
            thumbs = self.find_elements(thumb_selector)
            if len(thumbs) < 2:
                self.fail("Not enough thumbnails to verify switching")
            else:
                print(f"{len(thumbs)} thumbnails found")
        else:
            self.fail("Thumbnail section (#altImages) not found")

        # Assert thumbnail 1 visible
        first_thumb = '(//div[@id="altImages"]//li[contains(@class,"imageThumbnail")])[1]'
        if self.is_element_visible(first_thumb):
            print("Thumbnail 1 is visible")
            self.scroll_to_element(first_thumb)
            self.save_screenshot("TC17_thumbnail_1.png", "Test Case Screenshots")
        else:
            self.fail("Thumbnail 1 is not visible")

        # Assert thumbnail 2 visible
        second_thumb = '(//div[@id="altImages"]//li[contains(@class,"imageThumbnail")])[2]'
        if self.is_element_visible(second_thumb):
            print("Thumbnail 2 is visible")
            self.scroll_to_element(second_thumb)
            self.js_click(second_thumb)
            self.save_screenshot("TC17_thumbnail_2.png", "Test Case Screenshots")
        else:
            self.fail("Thumbnail 2 is not visible")

        # 6. Verify changing SKU options (Capacity / Style) if available
        if self.is_element_present("#twister-plus-inline-twister-card"):
            print("Inline twister card found")

            # SKU 1
            sku1 = '(//ul[contains(@data-a-button-group,"size_name")]//li)[1]//input'
            if self.is_element_present(sku1):
                print("SKU option 1 is present")
                self.scroll_to_element("#twister-plus-inline-twister-card")
                self.js_click(sku1)
                self.sleep(2)
                self.save_screenshot("TC17_sku_1.png", "Test Case Screenshots")
            else:
                self.fail("SKU option 1 not found")

            # SKU 2
            sku2 = '(//ul[contains(@data-a-button-group,"size_name")]//li)[2]//input'
            if self.is_element_present(sku2):
                print("SKU option 2 is present")
                self.scroll_to_element("#twister-plus-inline-twister-card")
                self.js_click(sku2)
                self.sleep(2)
                self.save_screenshot("TC17_sku_2.png", "Test Case Screenshots")
            else:
                self.fail("SKU option 2 not found")

        else:
            self.fail("SKU (twister) section not found")

        self.save_screenshot("TC17_screenshot.png", "Test Case Screenshots")
        print("Successfully validated product details page, thumbnails, and SKU options.")
