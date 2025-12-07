from faker import Faker
def main():
    fake = Faker()
    for _ in range(80):
        comment = Comment.objects.create(
            text = fake.text()
        )
    comments = Comment.objects.all()
    print(f"Comments in DB {comments.count()}")
if __name__ == '__main__':
    import os
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','mystore.settings')
    aplication = get_wsgi_application()
    from comments.models import Comment
    main()