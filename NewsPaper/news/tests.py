import unittest
from news.models import *


class TestUpdateR(unittest, TestCase):
    def test_store(self, id=1):
        a1 = Author.objects.get(id)
        pR1 = a1.ratingAuthor
        ps = Post
        Post.objects.get(id).like()
