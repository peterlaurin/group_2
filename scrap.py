import sqlite3
i
conn = sqlite3.connect('journals.db')
c = conn.cursor()


def get_top_k(field, k):
    c = conn.cursor()
    
    tops_query = 'SELECT ' + field + ' FROM authors GROUP BY ' \
                 + field + ' ORDER BY COUNT(*) DESC LIMIT ' + str(k)
    tops = [i[0].split() for i in c.execute(tops_query).fetchall()]
    tops.insert(0, ['all_' + field + 's'])
    finals = ['_'.join(i) for i in tops]
    return finals

top_countries = get_top_k('country', 100)
top_institutions = get_top_k('institution', 100)





valid_configs = [
[True, True, True, True, True],
[True, True, True, True, False],
[True, True, True, False, True],
[True, True, False, True, True],
[True, True, False, False, True],
[True, False, True, True, True],
[True, False, True, False, True],
[True, False, False, True, True],
[True, False, False, False, True],
[False, True, True, True, True],
[False, True, False, True, True],
[False, False, True, True, True],
[False, False, False, True, True]]

config_boos = [np.array(i) for i in valid_configs]

select = np.array(['countries', 'field', 'rank', 'institution', 'author_size'])

for_selector = []

for boo in config_boos:
    for_selector.append(select[~boo])



for config in for_selector: 



