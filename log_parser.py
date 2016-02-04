import re
import string
import os


from util import hook


def db_init(db):
    db.execute("create table if not exists memory(chan, word, data, nick,"
               " primary key(chan, word))")
    db.commit()

def get_memory(db, chan, word):
    row = db.execute("select data from memory where chan=? and word=lower(?)",
                     (chan, word)).fetchone()
    if row:
        return row[0]
    else:
        return None

regex = re.compile(">\t\.r\s")
cwd = os.getcwd()
with open(cwd + '/QuakeNet-#tlponies.log', 'r') as f:
    text = f.read()
    lst = text.split('\n')
    lst2 = []
    for line in lst:
        if regex.search(line):
            data = line.split(".r ")
            try:
                lst2.append(unicode(data[1], encoding="UTF-8"))
            except IndexError:
                pass
            
            
with open(cwd + '/tlponieslog.txt', 'r') as f:
    text = f.read()
    lst = text.split('\n')
    lst2 = []
    for line in lst:
        if regex.search(line):
            data = line.split(".r ")
            try:
                lst2.append(unicode(data[1], encoding="UTF-8"))
            except IndexError:
                pass

            
THE_LIST = lst2





@hook.command
def restoration(inp, nick='', chan='', db=None, lst=THE_LIST):
    if nick != 'camail':
        return 'no'
    db_init(db)
    for line in lst:
        try:
            head,tail = line.split(' ', 1)
        except ValueError:
            continue
        try:
            if tail[0] =='+':
                tail = tail[1:]
        except IndexError:
            continue

        db.execute("replace into memory(chan, word, data, nick) values"
                   " (?,lower(?),?,?)", (chan, head, head + ' ' + tail, nick))
        db.commit()
    return "complete"
