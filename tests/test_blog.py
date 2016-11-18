from .base import TestBase

from extensions import db
from models import Post, Tag


class TestBlogPosts(TestBase):
    def create_tags_posts_login(self):
        post1 = Post(title='title one', content='content one', author_id=1)
        post2 = Post(title='title two', content='content two', author_id=1)
        post3 = Post(title='title three', content='content three', author_id=1)
        post1.url = 'post_one'
        post2.url = 'post_two'
        post3.url = 'post_three'
        tag_a = Tag(name='tag_a')
        tag_b = Tag(name='tag_b')
        post1.tags = [tag_a, tag_b]
        post2.tags = [tag_a]
        with self.get_context():
            db.session.add(tag_a)
            db.session.add(tag_b)
            db.session.add(post1)
            db.session.add(post2)
            db.session.add(post3)
            db.session.commit()
        self.login()

    def test_can_access_blog(self):
        rv = self.app.get('/blog/')
        assert b'blog_posts_list_page' in rv.data

    def test_blog_list_with_no_posts(self):
        rv = self.app.get('/blog/')
        html = rv.data.decode()
        assert '<li>' not in html

    def test_create_new_post(self):
        self.login()
        rv = self.app.get('/blog/new', follow_redirects=True)
        html = rv.data.decode()
        assert 'blog_post_edit' in html  # redirected to blog editing page
        assert 'Untitled' in html

        with self.get_context():
            posts = Post.query.all()
            assert len(posts) == 1

    def test_blog_list_with_posts(self):
        self.create_tags_posts_login()

        rv = self.app.get('/blog/')
        html = rv.data.decode()
        assert 'Create New Post' in html
        assert html.count('<li>') == 3
        assert '/blog/edit/1' in html
        assert '/blog/edit/2' in html
        assert '/blog/edit/3' in html
        assert 'title one' in html
        assert 'title two' in html
        assert 'title three' in html

        assert '/blog/tag/tag_a' in html
        assert '/blog/tag/tag_b' in html
        assert 'tag_a' in html
        assert 'tag_b' in html
