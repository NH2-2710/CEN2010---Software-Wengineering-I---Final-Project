# Từng thứ mình nhìn thấy trên web được gọi là Web Element, khi người dùng tương tác với web như khi nhấn đăng nhập, hoặc nhấn sản phẩm để xem hàng, họ sẽ
# tương tác với web element. Việc tương tác với web element đòi hỏi việc họ phải tương tác với locators (thường là id, css selector, tag, class name) 
# của web element đó. Có thể hiểu các locators là các giá trị đại diện cho web element (được ghi trong dấu " " giống string), và có thể được truyền vào method như là  
# tham số để thực hiện hoặc kiểm tra một hành động hay phương thức nào đó. Ví dụ: self.click() sẽ nhận tham số là css selector của web element và 
# sẽ tự động nhấn chuột vào đúng web element chứa css selector đó
# Để tìm được locators của web element, mở web -> nhấn chuột phải chọn inspect, ở góc trên bên trái của cửa sổ mới, nhấn nút ngoài cùng để di chuột đến các web element
# khi đó sẽ tìm được code html tương ứng với web element đó, sau đó nhấn chuột trái vào đoạn code của web element chọn copy, chọn coppy as full xpath 
# để lấy locators rồi truyền vào hàm
# Để hiểu thêm các phương thức có trong Seleniumbase, truy cập https://seleniumbase.io/help_docs/method_summary/
from seleniumbase import BaseCase

class HomeTest(BaseCase):
    def test_home_page(self):
        # open home page
        self.open("https://tiki.vn/") # mở trang web, tham số truyền vào là link URL
        self.maximize_window() # phóng to cửa sổ ên full màn hình
        # assert title page
        self.assert_title("Tiki - Mua hàng online giá tốt, hàng chuẩn, ship nhanh") 
# kiểm tra xem dòng chữ có xuất hiện trên web chưa --> dùng để kiểm tra xem khi người dùng tương tác với web như nhập mật khẩu hay click vào đường dẫn thì có nhìn thấy dòng chữ cụ thể không
        # assert logo

        self.assert_element(".tiki-logo") # kiểm tra xem logo của tiki đã xuất hiện trên web chưa, tham số truyền vào là css selector

        # click button
        self.click("#VIP_BUNDLE > div.sc-cbd12f50-2.gLMejz > div > picture:nth-child(1) > img")
        # nhấn nút đóng vào cửa sổ xuất hiện khi khởi động web, tham số truyền vào là css selector
        self.sleep(3)# stop the program temporarily for 3 seconds
        self.click("#main-header > div > div > div.sc-b1e0edd7-0.ljZvVE > div.sc-ee984840-0.gypTeU > div.sc-7d80e456-15.dCdTIg > div:nth-child(2)")
        # click the web element of the 
        self.sleep(3)# stop the program temporarily for 3 seconds
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, "https://tiki.vn/")
        self.assert_true("tiki.vn" in get_started_url)
        self.assert_text("Freeship đơn từ 45k, giảm nhiều hơn cùng", "#__next > div:nth-child(1) > a > div > div")
        self.sleep(2) # stop the program temporarily for 2 seconds
        self.scroll_to_bottom() #scroll the web page to bottom
        self.assert_text("Danh Mục Sản Phẩm", "#main-footer > div:nth-child(5) > div > div.sc-8ba33404-0.hrWWOH > div.sc-4ce82f3c-4.aMfcf")
