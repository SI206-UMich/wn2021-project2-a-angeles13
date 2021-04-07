from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    fileContent = open(filename)
    soup = BeautifulSoup(fileContent, 'html.parser')
    fileContent.close()
    bookLst = []
    for book in soup.find_all('tr', itemtype='http://schema.org/Book'):
        titleContainer = book.find('a', class_='bookTitle')
        title = titleContainer.find('span', itemprop='name').text.strip('\n')
        authorContainer = book.find('a', class_='authorName')
        author = authorContainer.find('span', itemprop='name').text.strip('\n')
        bookLst.append((title,author))

    return bookLst

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    links =[]
    for book in soup.find_all('a', class_='bookTitle', itemprop='url', limit = 10):
        links.append('https://www.goodreads.com'+book.get('href'))
    return links


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    resp = requests.get(book_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    container = soup.find('div', id='metacol', class_='last col')
    #Obtaining Book Title and Author Name
    title = container.find('h1', id='bookTitle').text.strip('\n')
    authorContainer = container.find('a', class_='authorName')
    author = authorContainer.find('span', itemprop='name').text.strip('\n')
    #Obtaining Page Count
    pageText =soup.find('span', itemprop = 'numberOfPages').text
    expression = '([0-9])+'
    page =int(re.search(expression, pageText).group())
    return((title,author,page))

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    fileContent = open(filepath)
    soup = BeautifulSoup(fileContent, 'html.parser')
    fileContent.close()
    bestBooks = []
    for book in soup.find_all('div', class_='category clearFix'): 
        url = book.find('a').get('href')
        category = book.find('h4').text.strip('\n')
        title = book.find('img').get('alt')
        bestBooks.append((category,title,url))
    return bestBooks

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """ 
    with open(filename, 'w') as outFile:
        writer = csv.writer(outFile)
        writer.writerow(['Book title', 'Author Name'])
        for tup in data:
            writer.writerow([tup[0],tup[1]])


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        bookLst = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(bookLst),20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(bookLst), list)
        # check that each item in the list is a tuple
        for item in bookLst: 
            self.assertEqual(type(item), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(bookLst[0],("Harry Potter and the Deathly Hallows (Harry Potter, #7)","J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(bookLst[-1],("Harry Potter: The Prequel (Harry Potter, #0.5)","J.K. Rowling")) 

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(self.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for entry in self.search_urls: 
            self.assertEqual(type(entry), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        self.assertEqual(self.search_urls, 
        ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1',
        'https://www.goodreads.com/book/show/6542645-fantasy-in-death?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=2',
        'https://www.goodreads.com/book/show/35082746-fantasy-of-frost?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=3',
        'https://www.goodreads.com/book/show/2081.The_Mind_s_I?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=4',
        'https://www.goodreads.com/book/show/13600356-epic?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=5',
        'https://www.goodreads.com/book/show/25255723-gods-and-mortals?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=6',
        'https://www.goodreads.com/book/show/6931452-the-kingdom-of-fantasy?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=7',
        'https://www.goodreads.com/book/show/31363.How_to_Write_Science_Fiction_Fantasy?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=8',
        'https://www.goodreads.com/book/show/47530.Mapping_the_World_of_Harry_Potter?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=9',
        'https://www.goodreads.com/book/show/42667807-die-vol-1?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=10'])

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for link in self.search_urls: 
            summaries.append(get_book_summary(link))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            
        for summary in summaries: 
            # check that each item in the list is a tuple
            self.assertEqual(type(summary), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(summary[0]), str)
            self.assertEqual(type(summary[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(summary[2]), int)
        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2],337)    
    
    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        bestBooks = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(bestBooks), 20)
        for summary in bestBooks:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(summary), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(summary), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(bestBooks[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(bestBooks[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles,'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r') as file: 
            csv_lines = []
            reader  = csv.reader(file)
            for row in reader: 
                csv_lines.append(row)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0][0], 'Book title')
        self.assertEqual(csv_lines[0][1], 'Author Name')
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1][0],'Harry Potter and the Deathly Hallows (Harry Potter, #7)') 
        self.assertEqual(csv_lines[1][1],'J.K. Rowling')
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')
        self.assertEqual(csv_lines[-1][1], 'J.K. Rowling')
        
        

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



