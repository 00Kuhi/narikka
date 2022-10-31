import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from robobrowser import RoboBrowser
from scrapepage import scrape_events
from scrapepage import count_students
import time

def scrape_narikka(searches,host,username,password):
    """
    ret = list()
    for s in searches:
        ret.append(s['user'] + ' ' + s['month'])
    return ret
    """

    browser = RoboBrowser(parser='html.parser')
    browser.open(host+'?page=login')

    form = browser.get_form(action='login.php')
    form['username'].value = username
    form['password'].value = password
    browser.submit_form(form)

    students = list()

    for s in searches:
        month = s['month'].strip()
        user = s['user'].strip()
        browser.open(host+'?page=listaus&selector='+month)
        event_urls = scrape_events(browser.parsed)
        for href in event_urls:
            browser.open(host+href)
            students.extend(count_students(browser.parsed,user))
            time.sleep(1)

    return students

def print_students(students):
    from collections import Counter
    cnt = Counter(students)
    sorted_cnt = sorted(cnt.items())
    print("lkm,varaus")
    for s in sorted_cnt:
        print(str(s[1]) + "," + s[0])    

if __name__ == "__main__":
    from settings import months, host, username, password
    students = scrape_narikka(months,host,username,password)
    print_students(students)

