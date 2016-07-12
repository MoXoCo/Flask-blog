import requests
import bs4


class One_Index_Spider(object):
    def __init__(self):
        self.url = 'http://www.wufazhuce.com/'
        self.title = []
        self.img = []
        self.one = {}
        self.article = {}
        self.question = {}

    def output(self, dic):
        for i in dic:
            print(i, dic[i])

    def get_post(self, post):
        if post.small:
            try:
                num = post.a.get('href')[-4:]
                author = post.small.string
                title = post.a.strings.__next__().strip()
                return num, author, title
            except:
                num = post.get('href')[-4:]
                author = post.small.string
                title = post.strings.__next__().strip()
            return num, author, title
        else:
            try:
                num = post.a.get('href')[-4:]
                title = post.a.strings.__next__().strip()
                return num, title
            except:
                num = post.get('href')[-4:]
                title = post.strings.__next__().strip()
            return num, title

    def get_soup(self):
        response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(response.text, 'html.parser')

    def get_title(self):
        title = self.soup.find_all('p', class_='titulo')
        for t in title:
            self.title.append(t.string)

    def get_one(self):
        i = 0
        ones = self.soup.find_all('div', class_='fp-one-cita')
        for one in ones:
            num = one.a.get('href')[-4:]
            post = ''.join(one.strings)
            self.one[num] = self.title[i], post.strip(), self.img[i]
            i += 1

    def get_img(self):
        img_class = self.soup.find_all('img', class_='fp-one-imagen')
        for i in img_class:
            self.img.append(i['src'])

    def get_article(self):
        i = 1
        for today_article in self.soup.find_all(
                'p', class_='one-articulo-titulo'):
            num, author, title = self.get_post(today_article)
            self.article[num] = self.title[0], title + ' ' + author

        for early_article in self.soup.find_all(
                'ul', class_='list-unstyled pasado')[0].select('a'):
            num, author, title = self.get_post(early_article)
            self.article[num] = self.title[i], title + ' ' + author
            i += 1

    def get_question(self):
        i = 1
        for today_question in self.soup.find_all(
                'p', class_='one-cuestion-titulo'):
            num, title = self.get_post(today_question)
            self.question[num] = self.title[0], title

        for early_question in self.soup.find_all(
                'ul', class_='list-unstyled pasado')[1].select('a'):
            num, title = self.get_post(early_question)
            self.question[num] = self.title[i], title
            i += 1

    @property
    def run(self):
        self.get_soup()
        self.get_title()
        self.get_img()
        self.get_one()
        return self.one





