from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm, RandomForm
from Twitter import Twitter
from Analysis import analyze
from RandomTopic import get_random_topic


d = [[]]
d2 = [[]]
query = ""
query2 = ""

def listtups_to_listlists(lt):
  return [[x, y] for (x, y) in lt]

def setGraphs(form):
  global query
  global query2
  global d
  global d2

  count = 30
  query = str(form.query.data.replace('#','').strip())
  query2 = str(form.opQuery.data.replace('#','').strip())

  t = Twitter()

  if not t.checkTerm(query):
    if not query2 == "" and not t.checkTerm(query2):
      return (True, True)
    return (True, False)

  if not query2 == "":
    if not t.checkTerm(query2):
      return (False, True)

  a = t.getTweets(query, count)
  d = analyze(a, [float(i)/24.0 for i in range(-10*24, +3*24)])

  if not query2 == "":
    if not t.checkTerm(query2):
      return (False, True)
    a = t.getTweets(query2, count)
    d2 = analyze(a, [float(i)/24.0 for i in range(-10*24, +3*24)])

  return (False, False)


query = ""
query2 = ""

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  q1Invalid = False
  q2Invaled = False
  form = LoginForm()
  if form.validate_on_submit():
      q1Invalid, q2Invaled = setGraphs(form)
      # print q1Invalid, q2Invaled
      if not q1Invalid and not q2Invaled:
        return redirect('/results')
  return render_template('index.html',
                         title='Home',
                         q1Invalid=q1Invalid,
                         q2Invalid=q2Invaled,
                         form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
  global query
  global query2
  global d
  global d2

  # print ""
  # print "/results:"
  # print "Query 1: %s" % query
  # print "Query 2: %s" % query2
  # print "d: ",d
  # print "d2: ",d2
  
  if query ==  "" or query is None or request.referrer is None:
    return redirect('/index')
  
  q1Invalid = False
  q2Invalid = False
  form = LoginForm()
  if form.validate_on_submit():
      q1Invalid, q2Invalid = setGraphs(form)

      return redirect('/results')

  dataList = listtups_to_listlists(d)
  if not query2 == "":
    
    dataList2 = listtups_to_listlists(d2)

    d2 = None
    d = None
    return render_template('results.html',
                           title='Results',
                           q=query,
                           q2=query2,
                           data=dataList,
                           data2=dataList2,
                           q1Invalid=q1Invalid,
                           q2Invalid=q2Invalid,
                           form=form)
  d = None
  return render_template('results.html',
                           title='Results',
                           q=query,
                           data=dataList,
                           q1Invalid=q1Invalid,
                           q2Invalid=q2Invalid,
                           form=form)

@app.route('/about')
def about():
  return render_template('about.html',
                          title='Results')

@app.route('/random', methods=['GET', 'POST'])
def random():

  q1Invalid = False
  q2Invaled = False
  form = RandomForm()
  if form.validate_on_submit():
    if request.form['btn'] == 'Randomize':
      t1=get_random_topic().split(' ', 1)[0]
      while not Twitter().checkTerm(t1):
        t1=get_random_topic().split(' ', 1)[0]

      t2=get_random_topic().split(' ', 1)[0]
      while not Twitter().checkTerm(t2):
        t2=get_random_topic().split(' ', 1)[0]
      # print "t1: %s\nt2: %s" % (t1, t2)
      form.query.data=t1
      form.opQuery.data=t2
    else:
      if form.query != "" or form.opQuery != "":
        q1Invalid, q2Invaled = setGraphs(form)
        
        if not q1Invalid and not q2Invaled:
          return redirect('/results')

  return render_template('random.html',
                         q1Invalid=q1Invalid,
                         q2Invalid=q2Invaled,
                         form=form)

@app.route('/hof')
def hof():
  return render_template('hof.html')
  
@app.errorhandler(500)
def internal_error(error):
    if app.debug is not True:   
      import logging
      from logging.handlers import RotatingFileHandler
      file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
      file_handler.setLevel(logging.ERROR)
      formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
      file_handler.setFormatter(formatter)
      app.logger.addHandler(file_handler)
