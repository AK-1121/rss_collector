#import urllib3
#from lxml import html
#from grab import Grab

import re, requests

TAGS_LIST = ["title", "description", "link", "pubDate"]
#Possible tags: "content:encoded", "giude", 

# Search all entries of tag template in the input string.
# Return list of finded substrings:
def find_all_tag_data(string, tag):
    string = re.sub("\\n", "", string)
    list_of_messages = re.findall("<%s>(.+?)</%s>" % (tag, tag), string)
    return list_of_messages

def parse_rss(rss_string):
    mess_list = find_all_tag_data(rss_string, "item")
    mess_dict = {}

    for m in mess_list:
        fields_of_mess={}
        for tag in TAGS_LIST:
            try:
                fields_of_mess[tag] = find_all_tag_data(m, tag)[0]
            except:
                fields_of_mess[tag] = "-"

        fields_of_mess["id"] = str(hash(m)) + fields_of_mess["pubDate"]
        mess_dict[fields_of_mess["id"]] = fields_of_mess
           
    return mess_dict
        

# Grab: http://docs.grablib.org/index.html#document-grab/http_methods


if __name__ == "__main__":
    #url = "http://www.reddit.com/r/Python/new/.rss"
    #url = "http://www.ksl.com/xml/148.rss"
    url = "http://www.npr.org/rss/rss.php?id=1013"
    r = requests.get(url)
    print(r.status_code)

    #items = find_all_tag_data(str(r._content), "item")
    mess_dict = parse_rss(str(r._content))
    print(mess_dict)
    #print(type(mess_dict))
    for k_mess in mess_dict.keys():
        print("\n"+"="*35)
        for k_tag in mess_dict[k_mess].keys():
            print(k_tag+":\n "+mess_dict[k_mess][k_tag])
