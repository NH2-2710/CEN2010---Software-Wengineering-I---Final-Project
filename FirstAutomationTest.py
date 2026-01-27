from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://tiki.vn/")
driver.maximize_window()
title = driver.title
print(title)
assert "Tiki - Mua hàng online giá tốt, hàng chuẩn, ship nhanh" in title
driver.find_element(*(By.XPATH,"//body"))