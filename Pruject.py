from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome()

driver.get("https://www.jobinfo.co.il/%D7%93%D7%A8%D7%95%D7%A9%D7%99%D7%9D-%D7%94%D7%99%D7%99%D7%98%D7%A7/%D7%93%D7%A8%D7%95%D7%A9%D7%99%D7%9D-%D7%AA%D7%95%D7%9B%D7%A0%D7%94")

categories = driver.find_elements(By.CSS_SELECTOR, "a.Normal")
category_links = []
for obj in categories[:10]:
    href = obj.get_attribute("href")
    category_links.append(href)

with open("./jobs.csv", "w", newline="", encoding="utf-8-sig") as file:
    fieldnames = ["Title", "Description", "Requirements", "Company Size", "Category"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for category in category_links:
        driver.get(category)
        time.sleep(1)
        jobs = driver.find_elements(By.CSS_SELECTOR, "a.value.tooltip-activator")
        vacancy_links = []
        for obj1 in jobs:
            href = obj1.get_attribute("href")
            vacancy_links.append(href)
        for vacancy_link in vacancy_links:
            driver.get(vacancy_link)
            time.sleep(1)
            vacancy_details = {} 
            vacancy_ditails = driver.find_element(By.ID, "dnn_ctr505_OfferDetails_pnlOfferDetails")
            vacancy_details["Title"] = vacancy_ditails.find_element(By.ID, "dnn_ctr505_OfferDetails_hTitle").text
            vacancy_details["Description"] = vacancy_ditails.find_element(By.ID, "dnn_ctr505_OfferDetails_lblODesc").text
            vacancy_details["Requirements"] = vacancy_ditails.find_element(By.ID, "dnn_ctr505_OfferDetails_lblONeedsValue").text
            vacancy_details["Category"] = vacancy_ditails.find_element(By.ID, "dnn_ctr505_OfferDetails_lblOField").text
            try:
                vacancy_details["Company Size"] = vacancy_ditails.find_element(By.ID, "dnn_ctr505_OfferDetails_lblCoSize").text
            except:
                vacancy_details["Company Size"] = "לא צוין"
            writer.writerow(vacancy_details)
            time.sleep(1)

print('finish')

driver.quit()
