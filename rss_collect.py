# Timezones abbreviations:
# http://stackoverflow.com/questions/1703546/parsing-date-time-string-with-timezone-abbreviated-name-in-python

import datetime
import re
import requests
from lxml import etree

import html_pattern
from constants import *


# Transform date-time to unix-format:
# Example: "Sat, 14 Feb 2015 09:48:17 -0500" --> 1423896497.0
def time_to_unix(t_str):

    date = list(re.findall("(\d\d) (\w{3}) (\d{4})", t_str)[0])
    date[0], date[1], date[2] = int(date[0]), MONTHS[date[1]], int(date[2])
    tmp = list(re.findall("(\d\d):(\d\d):(\d\d)", t_str)[0])
    time = list(map(int, tmp))
    time_zone = (re.findall("([+-])(\d\d)(\d\d)", t_str))  # tz format: -0500
    if not time_zone:
        time_zone = (re.findall("\d\s([A-Z]{3,5})", t_str))[0]
        t_z = TIME_ZONES[time_zone]
    else:
        time_zone = list(time_zone[0])
        t_z = int(time_zone[0]+"1")*int(time_zone[1])+int(time_zone[2])/60

    # print (time_zone, len(time_zone))

    # print("time_zone: " + str(t_z))
    return datetime.datetime(date[2], date[1], date[0], time[0], time[1],
                             time[2]).timestamp() + t_z*3600


# Search all entries of tag template in the input string.
# Return list of finded substrings:
def find_all_tag_data(string, tag):

    string = re.sub("\\n", "", string)
    list_of_messages = re.findall("<%s>(.+?)</%s>" % (tag, tag), string)
    return list_of_messages


# Function parses rss file, returns 2-dimention dictionary of messages.
# 1st dimention: key - message id, value - message dict
# 2nd dimention: key - tags of message, value - text data of tag fields
def parse_rss(rss_string):
    mess_list = find_all_tag_data(rss_string, "item")
    mess_dict = {}
    url = find_all_tag_data(rss_string, "link")
    if url:
        url = url[0]
    else:
        url = "-"
    print("url: ", url)

    for m in mess_list:
        fields_of_mess = {}
        for tag in TAGS_LIST:
            try:
                fields_of_mess[tag] = find_all_tag_data(m, tag)[0]
            except:
                fields_of_mess[tag] = "-"

        fields_of_mess["url"] = url
        # Make id of message dict (float) as a connection of time in unix
        # format (integer part) and a part of hash of message text (fractional
        # part):
        fields_of_mess["id"] = (time_to_unix(fields_of_mess["pubDate"]) +
                                0.0001*(hash(m) % 10000))
        mess_dict[fields_of_mess["id"]] = fields_of_mess

    return mess_dict


def print_mess_dict(mess_dict):
    i = 1
    for k_mess in mess_dict.keys():
        print("\n" + str(i) + ": " + "="*35)
        i += 1
        for k_tag in mess_dict[k_mess].keys():
            print(str(k_tag) + ":\n " + str(mess_dict[k_mess][k_tag]))


def make_html(header_inf, md):

    line = ("<tr><td>%s<br><a href='%s'>rss</a></td>" +
            "<td><a href='%s'>%s</a></td><td>%s</td>" +
            "<td>%s (GMT)</td></tr>")
    html_file = open("rss.html", "w+")

    # Write info about our RSS collection:
    tmp = "<ul><li>" + ("</li> <li>").join(header_inf) + "</li></ul>"

    html_file.write(html_pattern.html_start + tmp +
                    html_pattern.html_table_start)

    displayed_keys = reversed(sorted(list(md.keys())))
    # Limits number of rss messages (50) :
    displayed_keys = list(displayed_keys)[:50]
    str_number = 0

    for dk in displayed_keys:
        str_number += 1

        # Removes CDATA tags:
        if re.findall("CDATA", md[dk]['description']):
            md[dk]['description'] = etree.fromstring("<ab>" +
                                                     md[dk]['description'] +
                                                     "</ab>").text
        # Change &lt and &gt on < , > :
        description = re.sub("&lt;", "<", md[dk]['description'])
        description = re.sub("&gt;", ">", description)
        description = re.sub("<(|/)pre>", "", description)
        html_file.write(line % (str(str_number), md[dk]['url'], md[dk]['link'],
                        md[dk]['title'], description,
                        datetime.datetime.fromtimestamp(
                        int(md[dk]['id'])).strftime("%d-%m-%Y %H:%M:%S")))

    html_file.write(html_pattern.html_finish)
    html_file.close()


if __name__ == "__main__":

    header_inf = []
    header_inf.append("Time of production:" +
                      datetime.datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S") +
                      " (GMT)")
    all_mess_dict = {}
    for url in URLS:
        r = requests.get(url)
        print("\n\n" + 35*"-" + "\n" + url + " - " + str(r.status_code))
        header_inf.append(url + " - " + str(r.status_code))
        mess_dict = parse_rss(str(r._content))
        print("number of messages: " + str(len(mess_dict.keys())))
        all_mess_dict.update(mess_dict)

    print("total messages: " + str(len(all_mess_dict.keys())))

    make_html(header_inf, all_mess_dict)
