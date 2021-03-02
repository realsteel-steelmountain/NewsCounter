#!C:\Users\YANG\AppData\Local\Programs\Python\Python38-32\python.exe
print("content-type:text/html; charset=UTF-8\n")

from bs4 import BeautifulSoup
import requests, json, cgi, sys, codecs, locale, re

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
query = form["query"].value
start_date = form["ds"].value
end_date = form["de"].value

ds = start_date.replace("-", ".")
de = end_date.replace("-", ".")

sd = start_date.replace("-", "")
ed = end_date.replace("-", "")

def naver_counter(query, ds, de):
    URL = f'https://s.search.naver.com/p/newssearch/search.naver?_callback=window.__jindo_callback._news_morelist_0&rev=42&query={query}&where=mobile_more_api&spq=0&m=1&sort=1&pd=3&nx_search_query=&nx_and_query=&nx_sub_query=&nx_search_hlquery=&eid=&force_original=&query_original=&photo=0&field=0&ds={ds}&de={de}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nlu_query=&nqx_theme=&is_dts=0&start='
    result = requests.get(URL).text
    results = result[44:-3]
    res = json.loads(results) 
    numb = res['totalCount']
    return numb


def daum_counter(query, sd, ed):
      URL = f'https://search.daum.net/search?w=news&sort=accuracy&q={query}&cluster=y&DA=STC&dc=STC&pg=1&r=1&p=1&rc=1&at=more&sd={sd}000000&ed={ed}235959&period=u'
      result = requests.get(URL)
      daum_soup = BeautifulSoup(result.text, "lxml")
      daum_result = daum_soup.find("span", id = "resultCntArea")
      string_daum = daum_result.string
      if ',' in string_daum:
            daum_results = re.search('약 (.*?)건', string_daum).group(1).replace(",","")
      elif string_daum == "1-0 / 0건":
            daum_results = '0'
      else:
            daum_results = re.search('/ (.*?)건', string_daum).group(1)

      return daum_results


naver_results = int(naver_counter(query, ds, de))
daum_results = int(daum_counter(query, sd, ed))

display_source = f"""
   <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;700&display=swap');
    
            body{{
              width : 90%;
            	height : 90vh;
              background-image: url("bgi.jpg");    
              background-repeat: no-repeat;
              background-size: cover;
              background-position: center;
              color: whitesmoke;
            }}
    
            #main{{
              width: 50%;
              height: 50%;
              overflow: auto;
              margin: auto;
              position: absolute;
              top: 0; left: 0; bottom: 0; right: 0;
              text-align: center;
              font-family: 'Roboto Condensed', sans-serif;
              display : grid;
              grid-template-columns: 50% 50%;
            }}
    
    
            #counter3, #counter2 {{ 
              font-family: 'Roboto Condensed'; 
              font-size: 100px; font-weight: bold; 
              text-align: center; 
              margin-bottom: 0px; 
              margin-left:10px; 
              margin-right:10px;
            }}
            
            @media (prefers-color-scheme: light) {{
              body {{
                background-image: url("mountains.jpg");
                color: black;
            }}
        }}
       
        </style>
    </head>
    <body>
      <div id="main">

        <div id ='naver_result'>
          <p id="counter2"></p>
          <span id="n_explain">articles on Naver</span>
        </div>

        <div id ='daum_result'>
          <p id="counter3"></p>
          <span id="d_explain">articles on Daum</span>
        </div>

        </div>
    
    
      <script>
        function numberCounter(target_frame, target_number) {{
        this.count = 0; this.diff = 0;
        this.target_count = parseInt(target_number);
        this.target_frame = document.getElementById(target_frame);
        this.timer = null;
        this.counter();
    }};
        numberCounter.prototype.counter = function() {{
            var self = this;
            this.diff = this.target_count - this.count;
        
            if(this.diff > 0) {{
                self.count += Math.ceil(this.diff / 5);
            }}
        
            this.target_frame.innerHTML = this.count.toString();
        
            if(this.count < this.target_count) {{
                this.timer = setTimeout(function() {{ self.counter(); }}, 20);
            }} else {{
                clearTimeout(this.timer);
            }}
        }};

    new numberCounter("counter2", {naver_results});
    new numberCounter("counter3", {daum_results});
    
      </script>
    </body>
    </html>
    """



print(display_source)


