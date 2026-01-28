from seleniumbase import BaseCase

class LoginTest(BaseCase):

    def setUp(self): 
    # to run the program before every test begins
        super().setUp()
        """This procedures opens the windows of "TIKI" website and close ad windows and open
        login window to prepare inputting information for logging"""
        print("RUNNING BEFORE THE TEST")

        self.open("https://tiki.vn/") # open the website "TIKI"
        self.maximize_window() # make the window open at maximum size
        self.sleep(5)
        self.assert_element(".tiki-logo", timeout = 3)
        # verify if the TIKI's logo appears on the webpage
        self.click_if_visible("img[alt='close-icon']", timeout = 3) 
        # click the close button of the first advertisement window appears on the webpage

        self.sleep(5)

        self.click_if_visible("[data-view-id='header_header_account_container']", timeout = 3)
        # click the "Tài khoản" if it is visible on the webpage
        self.assert_element('button:contains("Tiếp Tục")')
        # to verify if the "Tiếp tục" button is available on the Login window

    def tearDown(self):
        # Clear all cookies so the next test starts with a fresh login screen
        self.clear_local_storage()
        self.clear_session_storage()
        self.delete_all_cookies()
        super().tearDown()

    def test_case_TC01(self):
        """TC01: Verify the login procedure is executed correctly
        and allow when the user to log in if they enter the correct 
        telephone and password"""
        self.wait_for_element_visible('input[name="tel"]')
        # wait for the text field "Số điện thoại" to be visible
        self.click('input[name="tel"]')
        # click the text field "Số điện thoại" if visible
        # and verify whether the user can click the text field before typing information

        self.send_keys('input[name="tel"]', "0337998047")
        # send the telephone number which exists in the system to the text field
        self.save_screenshot("filled_telephone.png", "TC01_screenshots")
        # save the screenshot after filling the telephone number text field
        self.click_if_visible('button:contains("Tiếp Tục")')
        # click "Tiếp Tục" button
        self.wait_for_element_visible('input[type="password"]')

        self.send_keys('input[type="password"]', "Huyhoang@2710")
        # send the correct password associated to the telephone number
        self.save_screenshot("filled_password.png", "TC01_screenshots")
        # save the screenshot after filling the telephone number text field

        self.click('button:contains("Đăng Nhập")')
        # click the "Đăng Nhập" button to log in
        self.save_screenshot("login_successfully.png", "TC01_screenshots")
        # save the screenshot after logging in successfully
        self.click_if_visible("img[alt='close-icon']")
        # click the close button in the ad window appears logging in if the ad appears

        self.hover_on_element("[data-view-id='header_header_account_container']")
        # hover the mouse on the Tài khoản button
        self.save_screenshot("sub-options in Tài khoản.png", "TC01_Screenshots")
        # save the screenshot showing sub options in Tài khoản button
        self.wait_for_element_visible('p:contains("Thông tin tài khoản")')
        # hover to the "Tài khoản" section to make more options in this section appears
        self.assert_elements("div[data-view-id='header_header_account_container'] p")
        # to verify if options in "Tài khoản" section including "Thông tin tài khoản",
        # "Hạng TikiVIP của bạn", "Đơn hàng của tôi", "Trung tâm hỗ trợ", "Đăng xuất" are present

        print("The test case TC01 has been verified successfully")
        # This statement will be printed if the compiler can reach to the end of the program
        # else, the compiler is stuck somewhere in the progra indicating an error pops up

    def test_case_TC02(self):
        """This test verifies whether the system allow the user to enter a number that
        is more than 10 digits"""
        invalid_number = "03373412325" # assign a number with 11 digits to the variable
        self.send_keys('input[name="tel"]', invalid_number) # input the 11-digits number to the text field
        self.save_screenshot("filled_telephone.png", "TC02_screenshots")
        try: 
            self.assert_text(invalid_number[0:len(invalid_number)], 'input[name="tel"]')
            # verify whether the invalid number is typed completely in the text field
            # or any extra number is excluded
        except Exception:
            print("The system doesn't allow user to enter more than 10 digits in the field")
            # print the statement if there is an error
        print("The test case TC02 has been verified successfully")
            # print the statement indicating that the test has been completed successfully

    def test_case_TC03(self):
        """This test verifies whether the system allow the user to enter a number that
        is less than 10 digits"""
        invalid_number = "033799804" # assign a number with 9 digits to the variable
        self.send_keys('input[name="tel"]', invalid_number)
        # type the invalid number to the text field
        self.save_screenshot("filled_telephone.png", "TC03_screenshots")
        # save the screenshot of filling invalid number to the text field
        self.click('button:contains("Tiếp Tục")')
        self.sleep(3)
        self.assert_text("Số điện thoại không đúng định dạng.", ".error-mess")
        # verify if the system notifies the error to the user showing that the number is not correctly formatted
        self.save_screenshot("error_notified.png", "TC03_screenshots")
        # save the screenshot notifying the phone number is not formatted correctly
        print("The test case TC03 has been verified successfully")

