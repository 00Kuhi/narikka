def scrape_events(page):
    a_list = page.find_all("a",{ "class" : "kalenteritapahtuma" })
    links = list()
    while a_list:
        a = a_list.pop()
        links.append(a['href'])
    return links

def count_students(page,user):
    pretty = page.prettify()
    import re
    shifts = re.findall(f".*\({user}\)",pretty)

    students = list()
    while shifts:
        shift = shifts.pop().strip()
        match = re.search(f".*\({user}\)",shift)
        if match:
            student = match.group(0)
            student = trim_line(student,user)
            students.append(student)
        else:
            students.append(shift)
    return students

def trim_line(s,user):
    r = s.replace(user,'')
    r = r.replace('(','')
    r = r.replace(')','')
    r = r.strip()
    return r
