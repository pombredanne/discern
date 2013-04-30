This is an example project for the ml service api.

If you are running the ml api at 127.0.0.1:7999 and you have performed all setup instructions, do the following to run the example.

1. cd /examples/problem_grader (this directory)
2. pip install -r requirements.txt
3. python manage.py syncdb --noinput
4. python manage.py migrate --noinput
5. python manage.py runserver 127.0.0.1:7998

You should now be able to navigate to 127.0.0.1:7998 and use the frontend.  You will be able to create a course.  After creation, clicking on the course will let you view the problems.  You can then add problems to the course.  You will then be able to use the write essays and grade essays actions.