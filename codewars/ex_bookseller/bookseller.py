
# https://www.codewars.com/kata/54dc6f5a224c26032800005c/train/python 
# 26 categories a-z
# books have ids of 3/4/5 chars long
# 1st character of id defines the category
# quantity of books follows the id with a space inbetween

import re

# Create stocklist of the quantity of books in each category
# ** 1. This is created outside of the function because in a real-world setting the categories would want to be preserved **
# ** 2. Also, if we were to add books or update quantities, this keeps the data of the stock list being reset and books that are not being updated or added from being lost **
# ** 3. However, in this example we want the stocklist to reset so we can test different entries - so a function to reset stock list is made
stock = dict()
# Enter all categories
def reset_stock_list():
    for i in range(65,91):
        cat = chr(i)
        stock[cat] = {
            'books': dict(),
            'count': 0
        }

def stock_list(list_of_art, list_of_cat):   
    # The following line of code resolves the problems i discuss in 3.3 and 4.2. The problem was with understanding the description of the kata.
    if len(list_of_art) == 0 or len(list_of_cat) == 0: return ''

    reset_stock_list() # comment this in production

    # 1. Enter the book and its quantity into stock according to its category
    for book_info in list_of_art:
        l = book_info.split(' ')
        c = l[0]
        cat = c[0]
        stock[cat]['books'][c[1:]] = int(l[1])
    
    # 2. Find the total of books in each category
    for cat,d in stock.items():
        for v in d['books'].values():
            stock[cat]['count'] += v

    # 3.1. Create a list of tuples which has the total book count for each category
    l = list()
    # 3.2. Loop through list of categories so the str can be created in the desired order
    for cat in list_of_cat:
        # # 3.3 (Unclear instruction, however:) If there are no books in one of the specified categories then i must return an empty string, so continue
        # # 3.3.1 if there are no books in a category, do not return it
        # Problem with kata...
        # if len(stock[cat]['books']) == 0: continue

        l.append((cat,stock[cat]['count']))

    # 4.1 Format the list of tuples into the desired format
    form = '({} : {})'
    sep = ' - '
    s = ''
    # format
    for t in l:
        # 4.2 (The following line of code continues the logical of 3.3): Do not add category to return string if it has no books
        #if t == '' : continue

        s += form
        if t is not l[len(l)-1]:
            s += sep
        s = s.format(t[0],t[1])

    # # 5.1 - To meet the awkward demands of the test which ask for counts of 0 to be and empty string but seemingly only when only all of the categories are empty
    # # Problem with random test?
    # list_of_art = []
    # list_of_cat = ['B', 'R', 'D', 'X']
    # Error: '(B : 0) - (R : 0) - (D : 0) - (X : 0)' should equal ''
    # I can fix this however doing so means that i don't meet the demands of other tests that require e.g., (A : 0) - (B : 1290)
    if re.search('[1-9]',s) == None:
        s = ''

    return s

