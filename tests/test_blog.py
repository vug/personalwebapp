from .base import TestBase

from extensions import db
from models import Post, Tag


class TestBlogPosts(TestBase):
    def create_tags_posts(self):
        post1 = Post(title='title one', content='content one', author_id=1, timezone=0)
        post2 = Post(title='title two', content='content two', author_id=1, timezone=0)
        post3 = Post(title='title three', content='content three', author_id=1, timezone=0)
        post1.url = 'post_one'
        post1.state_id = 2
        post2.url = 'post_two'
        post2.state_id = 1
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

    def test_blog_list_with_posts_anonymous(self):
        """Test anonymous user does not see draft posts."""
        self.create_tags_posts()
        rv = self.app.get('/blog/')
        html = rv.data.decode()

        assert 'title one' in html
        assert 'title two' not in html

    def test_blog_list_with_posts(self):
        self.create_tags_posts()
        self.login()

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

    def test_view_post(self):
        self.create_tags_posts()
        self.login()

        rv = self.app.get('/blog/post/post_one')
        html = rv.data.decode()
        assert 'blog_view_post' in html
        assert 'title one' in html
        assert 'content one' in html

    def test_attempt_viewing_non_existing_url(self):
        rv = self.app.get('/blog/post/non_existing_url')
        assert rv.status_code == 404

    def test_edit_post_view(self):
        self.create_tags_posts()
        self.login()
        rv = self.app.get('/blog/edit/1')
        html = rv.data.decode()
        assert 'blog_post_edit' in html
        assert '/blog/post/post_one' in html  # View Post link
        assert 'value="title one"' in html  # title input text
        assert 'content one' in html  # text area for content
        assert 'tag_a' in html and 'tag_b' in html

        with self.get_context():
            post = Post.query.filter_by(id=2).first()
            assert post.state.name == 'draft'
            assert post.published_at is None
            assert post.edited_at is None

            self.app.post('/blog/edit/2', follow_redirects=True,
                          data={'title': post.title, 'url': post.url, 'content': post.content, 'state': '2'})
            assert post.state.name == 'published'
            assert post.published_at is not None
            assert post.edited_at is None

            self.app.post('/blog/edit/2', follow_redirects=True,
                          data={'title': post.title, 'url': post.url, 'content': 'edited content', 'state': '2'})
            assert post.state.name == 'published'
            assert post.published_at is not None
            assert post.edited_at is not None
            assert post.content == 'edited content'

            self.app.post('/blog/edit/2', follow_redirects=True,
                          data={'title': post.title, 'url': post.url, 'content': 'edited content', 'state': '1'})
            assert post.state.name == 'draft'
            assert post.published_at is None
            assert post.edited_at is None

    def test_delete_post(self):
        self.create_tags_posts()
        self.login()
        rv = self.app.post('/blog/delete/1', follow_redirects=True)
        html = rv.data.decode()
        assert '/blog/edit/1' not in html

    def test_preview(self):
        self.create_tags_posts()
        self.login()
        rv = self.app.post('/blog/preview', data={'markdown': '[a link](http://www.example.com)'})
        html = rv.data.decode()
        assert '<p><a href="http://www.example.com">a link</a></p>' in html

    def test_listing_post_with_a_tag(self):
        self.create_tags_posts()
        rv = self.app.get('/blog/tag/tag_a')
        html = rv.data.decode()
        assert '/blog/post/post_one' in html
        assert '/blog/post/post_two' in html
        assert '/blog/post/post_three' not in html

    def test_edit_tags(self):
        self.create_tags_posts()
        self.login()
        rv = self.app.get('/blog/edit_tags')
        html = rv.data.decode()

        assert 'blog_edit_tags' in html
        assert 'tag_a' in html
        assert 'tag_b' in html
