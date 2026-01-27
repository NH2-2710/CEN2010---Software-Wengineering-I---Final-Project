from seleniumbase import BaseCase

class FirstTest(BaseCase):
    def test_keiser(self):
        self.open("https://kuv.edu.vn/vi/")
        self.maximize_window()
        self.assert_text("Sinh viên là ưu tiên hàng đầu tại Keiser University, Vietnam", "h4")
        self.sleep(2)
        self.scroll_to_element("/html/body/div[1]/footer/section[2]/div[2]/div[2]")
        self.sleep(2)
        self.assert_text("View Keiser University's EASE Grant Performance Measures", "/html/body/div[1]/footer/section[2]/div[2]/div[2]")

    def test_menu_links(self):
        self.open("https://tiki.vn/")
        print(self.find_elements("//*[starts-with(@data-view-id, 'header_quicklinks_item')]"))