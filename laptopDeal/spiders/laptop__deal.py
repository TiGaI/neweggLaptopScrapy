from scrapy import Spider
from laptopDeal.items import LaptopdealItem
import re
from scrapy.http.request import Request
from scrapy_splash import SplashRequest
import pandas as pd
# import csv

# import lxml.html
# from lxml import etree
# from selenium import webdriver 
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 
# from selenium.common.exceptions import TimeoutException
# scrapy crawl laptop

# csv_file = open('laptop2.csv', 'w+', encoding='utf-8', newline='')
# writer = csv.writer(csv_file)


class laptopAll(Spider):
	name = 'laptop'
	allowed_urls = ['https://www.newegg.com/']
	start_urls = ['https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32?Tid=6740&PageSize=96']
#                  https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32/Page-100?Tid=6740&PageSize=96
	def parse(self, response):
		for index in range(1,25):
			url ='https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32/''Page-' + str(index) + '?Tid=6740&PageSize=96'
			print("********* ")
			print(url)
			print("********* ")
			yield Request(url=url, callback=self.parse_laptop_page)


	def parse_laptop_page(self, response):
		data = pd.DataFrame()
		rows = response.xpath("//div[contains(@class, 'item-container')]/div")

		for selector in rows:
			#a[1]/@href
			url = selector.xpath("./a[1]/@href").extract()[0]
			#print(url)
			priceCurrent1 = selector.css('li[class=price-current] strong::text').extract()[0].replace(",", "")
			priceCurrent2 = selector.css('li[class=price-current] sup::text').extract()[0]
			#print("************: ", priceCurrent1)
			#print("************: ", priceCurrent2)
			priceCurrent = float(priceCurrent1 + priceCurrent2)
			print(url)
			try:
				pricePrevious = float(re.sub('[^0-9.]+', '', selector.css('li[class=price-was]::text').extract()[0]))
			except:
		 		pricePrevious = priceCurrent
			
			yield Request(url=url, callback=self.parse_detail_page, meta={'priceCurrent': priceCurrent, 'pricePrevious': pricePrevious})

	def parse_detail_page(self, response):
		specsDict = {}
		#get the price and the save price if it exist
		specsDict["Price_Current"] = response.meta['priceCurrent']
		specsDict["Price_Previous"] = response.meta['pricePrevious']
		specsDict["Saving"] = response.meta['pricePrevious'] - response.meta['priceCurrent']
		#print(50*"*", specsDict)

		detail_url = response.xpath('//*[@id="Specs"]/fieldset')
		
		# print("detail_url", detail_url)

		for specs in detail_url:
			fieldset = specs.xpath('.//h3/text()').extract()
			# print("this is fieldset", fieldset)
			try:
				dltags = specs.xpath(".//dl")
			except:
				dltags = ""

			# print("this is dltags", dltags)

			if fieldset[0] == "Model":
				# print("I AM HERE", dltags)
				for dl in dltags:
					# print("I AM HERE", dltags)
					dt = dl.xpath(".//dt/text()").extract()[0]
					# print("THIS IS NOT DT: ", dt)
					if dt == "Brand":
						specsDict['Brand'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Series":
						specsDict['Series'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Model":
						specsDict['Model'] = dl.xpath(".//dd/text()").extract()[0]
					else:
						continue
			elif fieldset[0] == "Quick Info":
				for dl in dltags:
					try:
						dt = dl.xpath(".//dt/text()").extract()[0]
					except:
						dt = dl.xpath(".//dt/a/text()").extract()[0]

					if dt == "Operating System":
						specsDict['Operating_System'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Screen":
						specsDict['Screen'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="CPU":
						specsDict['CPU'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Memory":
						specsDict['Memory'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Storage":
						specsDict['Storage'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Graphics Card":
						specsDict['GPU'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Video Memory":
						specsDict['GPU_Spec'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Dimensions (W x D x H)":
						specsDict['DimensionWxDxH'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Weight":
						specsDict['Weight'] = dl.xpath(".//dd/text()").extract()[0]
					else:
						continue
			elif fieldset[0] == "CPU":
				for dl in dltags:
					try:
						dt = dl.xpath(".//dt/text()").extract()[0]
					except:
						dt = dl.xpath(".//dt/a/text()").extract()[0]

					if dt == "CPU Type":
						specsDict['CPU_Type'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="CPU Speed":
						specsDict['CPU_Speed'] = dl.xpath(".//dd/text()").extract()[0]
					else:
						continue
			elif fieldset[0] == "Display":
				for dl in dltags:
					try:
						dt = dl.xpath(".//dt/text()").extract()[0]
					except:
						dt = dl.xpath(".//dt/a/text()").extract()[0]
					
					if dt == "Screen_Size":
						specsDict['Screen_Size'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt == "Touchscreen":
						specsDict['Touchscreen'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Resolution":
						specsDict['Resolution'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Refresh Rate":
						specsDict['Refresh_Rate'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="LCD Features":
						specsDict['LCD_Features'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Wide Screen Support":
						specsDict['Wide_Screen_Support'] = dl.xpath(".//dd/text()").extract()[0]				
					else:
						continue
			elif fieldset[0] == "Storage":
				for dl in dltags:

					dt = dl.xpath(".//dt/text()").extract()[0]

					if dt == "SSD":
						specsDict['SSD'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="HDD":
						specsDict['HDD'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Storage Spec":
						specsDict['Storage_Spec'] = dl.xpath(".//dd/text()").extract()[0]
					else:
						continue
			elif fieldset[0] == "Optical Drive":
				for dl in dltags:

					dt = dl.xpath(".//dt/text()").extract()[0]

					if dt == "Optical Drive":
						specsDict['Optical_Drive'] = dl.xpath(".//dd/text()").extract()[0]
					else:
						continue						
			elif fieldset[0] == "Communications":
				for dl in dltags:

					try:
						dt = dl.xpath(".//dt/text()").extract()[0]
					except:
						dt = dl.xpath(".//dt/a/text()").extract()[0]

					if dt == "WLAN":
						specsDict['WLAN'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Bluetooth":
						specsDict['Bluetooth'] = dl.xpath(".//dd/text()").extract()[0]
					else:
						continue
			elif fieldset[0] == "Ports":
				for dl in dltags:

					try:
						dt = dl.xpath(".//dt/text()").extract()[0]
					except:
						dt = dl.xpath(".//dt/a/text()").extract()[0]

					if dt == "USB":
						specsDict['USB'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Video Port":
						specsDict['Video_Port'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="HDMI":
						specsDict['HDMI'] = dl.xpath(".//dd/text()").extract()[0]					
					else:
						continue
			elif fieldset[0] == "Input Device":
				for dl in dltags:
					try:
						dt = dl.xpath(".//dt/text()").extract()[0]
					except:
						dt = dl.xpath(".//dt/a/text()").extract()[0]

					if dt == "Backlit Keyboard":
						specsDict['Backlit'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Webcam":
						specsDict['Webcam'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Card Reader":
						specsDict['Card_Reader'] = dl.xpath(".//dd/text()").extract()[0]					
					else:
						continue
			elif fieldset[0] == "General":
				for dl in dltags:
					dt = dl.xpath(".//dt/text()").extract()[0]

					if dt == "Style":
						specsDict['Style'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Type":
						specsDict['Type'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Usage":
						specsDict['Usage'] = dl.xpath(".//dd/text()").extract()[0]					
					else:
						continue
			elif fieldset[0] == "Power":
				for dl in dltags:
					dt = dl.xpath(".//dt/text()").extract()[0]

					if dt == "AC Adapter":
						specsDict['AC_Adapter'] = dl.xpath(".//dd/text()").extract()[0]
					elif dt =="Battery":
						specsDict['Battery'] = dl.xpath(".//dd/text()").extract()[0]				
					else:
						continue

		# print("this is specsDict", specsDict)
		item = LaptopdealItem()
		# item = specsDict
		for key, value in specsDict.items():
			# print(key, value)
			item[key] = value
		# print("Item: ", item)
		yield item
