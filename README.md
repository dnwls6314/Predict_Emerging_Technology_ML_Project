# Predict_Emerging_Technology_ML_Project

## 졸업연구
1. Data source: Crawled patents about healthcare from PatentsView by api
2. Data preprocessing: Using patent information, made it to my own variables
3. Using machine learning, try to predict promising patent which can be proxy for emerging technology

  ### Data Source - raw patents
  1. By 'Crawling.py', I crawled USPTO patents about health care
  2. the crawling process was made by PatentsView API query
  3. base url: https://api.patentsview.org/patents/query
  4. I concatenated the base url and crawling elements I defined

  ### Additional data crawling
  1. Since there are no Family Patent info on PatentsView, I had to crawl additionally
    1-1. Family Patent number: number of countries where a patent was granted
  2. In this case, I used Chrome Webdriver and Selenium to crawl patents info on Google patent website
  3. Base url: https://patents.google.com/patent/
  4. Add to base url, I parsed html source by BeautifulSoup and crawled number of Family Patent
