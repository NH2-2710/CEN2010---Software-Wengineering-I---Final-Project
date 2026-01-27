from seleniumbase import BaseCase

class HomeTest(BaseCase):
    def test_home_page(self):
        # open home page
        self.open("https://tiki.vn/")
        self.maximize_window()
        # assert title page
        self.assert_title("Tiki - Mua hàng online giá tốt, hàng chuẩn, ship nhanh")

        # assert logo

        self.assert_element(".tiki-logo")

        # click button
        self.click("#VIP_BUNDLE > div.sc-cbd12f50-2.gLMejz > div > picture:nth-child(1) > img")
        self.sleep(3)
        self.click("#main-header > div > div > div.sc-b1e0edd7-0.ljZvVE > div.sc-ee984840-0.gypTeU > div.sc-7d80e456-15.dCdTIg > div:nth-child(2)")
        self.sleep(3)
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, "https://tiki.vn/")
        self.assert_true("tiki.vn" in get_started_url)
        self.assert_text("Freeship đơn từ 45k, giảm nhiều hơn cùng", "#__next > div:nth-child(1) > a > div > div")
        self.sleep(2)
        self.scroll_to_bottom()
        self.assert_text("Danh Mục Sản Phẩm", "#main-footer > div:nth-child(5) > div > div.sc-8ba33404-0.hrWWOH > div.sc-4ce82f3c-4.aMfcf")