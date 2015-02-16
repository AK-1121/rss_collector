URLS = ["http://www.reddit.com/r/Python/new/.rss",
        "http://www.ksl.com/xml/148.rss",
        "http://www.npr.org/rss/rss.php?id=1013",
        "http://news.yahoo.com/rss/",
        "http://www.economist.com/sections/business-finance/rss.xml"
        ]

TAGS_LIST = ["title", "description", "link", "pubDate", "url"]
#Possible tags: "content:encoded", "giude", 

MONTHS = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr': 4, 'May': 5, 'Jun': 6, 
          'Jul': 7, 'Aug': 8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

TIME_ZONES = {
              # Timezone abbreviations
              # Std     Summer

              # Standards
              'UT':0,
              'UTC':0,
              'GMT':0,

              # A few common timezone abbreviations
              'CET':1,  'CEST':2, 'CETDST':2, # Central European
              'MET':1,  'MEST':2, 'METDST':2, # Mean European
              'MEZ':1,  'MESZ':2,             # Mitteleuropäische Zeit
              'EET':2,  'EEST':3, 'EETDST':3, # Eastern Europe
              'WET':0,  'WEST':1, 'WETDST':1, # Western Europe
              'MSK':3,  'MSD':4,  # Moscow
              'IST':5.5,          # India
              'JST':9,            # Japan
              'KST':9,            # Korea
              'HKT':8,            # Hong Kong

              # US time zones
              'AST':-4, 'ADT':-3, # Atlantic
              'EST':-5, 'EDT':-4, # Eastern
              'CST':-6, 'CDT':-5, # Central
              'MST':-7, 'MDT':-6, # Midwestern
              'PST':-8, 'PDT':-7, # Pacific

              # Australian time zones
              'CAST':9.5, 'CADT':10.5, # Central
              'EAST':10,  'EADT':11,   # Eastern
              'WAST':8,   'WADT':9,    # Western
              'SAST':9.5, 'SADT':10.5, # Southern

              # US military time zones
              'Z': 0,
              'A': 1,
              'B': 2,
              'C': 3,
              'D': 4,
              'E': 5,
              'F': 6,
              'G': 7,
              'H': 8,
              'I': 9,
              'K': 10,
              'L': 11,
              'M': 12,
              'N':-1,
              'O':-2,
              'P':-3,
              'Q':-4,
              'R':-5,
              'S':-6,
              'T':-7,
              'U':-8,
              'V':-9,
              'W':-10,
              'X':-11,
              'Y':-12
              }
