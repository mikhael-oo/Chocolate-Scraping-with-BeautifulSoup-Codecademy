from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html')
soup = BeautifulSoup(url.content, 'html.parser')
#print(soup)
tags = soup.find_all(attrs = {'class': 'Rating'})
ratings = []

# get the ratings after skipping the first thing in the rating class
for tag in tags[1:]:
  rat = tag.get_text()
  ratings.append(float(rat))

plt.hist(ratings)
plt.show()
plt.clf()
# find the company tags
comp_tag = soup.select('.Company')
comp = []
# loop after the first to skip through the title
for el in comp_tag[1:]:
  comp.append(el.get_text())
df = pd.DataFrame({'Company': comp,
                   'Ratings': ratings})
#print(df.head())

# group by company and average the ratings
mean_val = df.groupby('Company').Ratings.mean()

# this command take the 10 highest rated companies
top_ten = mean_val.nlargest(10)
print(top_ten)

# do the same processes to get cocoa percent in integer form
cocoa_tags = soup.select('.CocoaPercent')
cocoa = []

for td in cocoa_tags[1:]:
  coc = td.get_text().strip('%')
  cocoa.append(float(coc))

# add the percentage to the df dataframe
df['CocoaPercent'] = cocoa
print(df.head())

# make a scatterplot pf ratings vs cocoapercentage

plt.scatter(df.CocoaPercent, df.Ratings)
plt.xlabel('Cocoa Percent')
plt.ylabel('Ratings')
plt.title('Scatterplot of Ratings vs Cocoa Percentage')

z = np.polyfit(df.CocoaPercent, df.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercent, line_function(df.CocoaPercent), "r--")

plt.show()