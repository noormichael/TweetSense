from flask import render_template, flash, redirect, request, session
from app import app
from .forms import LoginForm, RandomForm
from Twitter import Twitter
from Analysis import analyze
from RandomTopic import get_random_topic

def listtups_to_listlists(lt):
  return [[x, y] for (x, y) in lt]

def setGraphs(form, q, q2):
  query = q
  query2 = q2

  t = Twitter()

  if not t.checkTerm(query):
    if not query2 == "" and not t.checkTerm(query2):
      return (True, True)
    return (True, False)

  if not query2 == "":
    if not t.checkTerm(query2):
      return (False, True)

  if not query2 == "":
    if not t.checkTerm(query2):
      return (False, True)

  return (False, False)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  q1Invalid = False
  q2Invalid = False
  session['qu'] = ""
  session['qu2'] = ""
  form = LoginForm()
  if form.validate_on_submit():
    session['qu'] = str(form.query.data.replace('#','').strip())
    session['qu2'] = str(form.opQuery.data.replace('#','').strip())
    q1Invalid, q2Invalid = setGraphs(form, session['qu'], session['qu2'])
    
    # print q1Invalid, q2Invalid
    if not q1Invalid and not q2Invalid:
      return redirect('/results')
  return render_template('index.html',
                         title='Home',
                         q1Invalid=q1Invalid,
                         q2Invalid=q2Invalid,
                         form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
  d = [[]]
  d2 = [[]]

  # print ""
  # print "/results:"
  # print "Query 1: %s" % query
  # print "Query 2: %s" % query2
  # print "d: ",d
  # print "d2: ",d2
    
  # return result = "\n".join("\t".join(map(str,l)) for l in d)
  count = 30
  t = Twitter()
  a = t.getTweets(session['qu'], count)
  d = analyze(a, [float(i)/24.0 for i in range(-10*24, +3*24)])
  
  if not session['qu2'] == "":
    a = t.getTweets(session['qu2'], count)
    d2 = analyze(a, [float(i)/24.0 for i in range(-10*24, +3*24)])
  
  form = LoginForm()
  if form.validate_on_submit():
    session['qu'] = str(form.query.data.replace('#','').strip())
    session['qu2'] = str(form.opQuery.data.replace('#','').strip())
    if session['qu'] == "":
      return redirect('/index')
    # q1Invalid, q2Invalid = setGraphs(form, query, query2)
    t = Twitter()
    
    if not t.checkTerm(session['qu']):
      if not session['qu2'] == "" and not t.checkTerm(session['q2']):
        return render_template('results.html',
                           title='Results',
                           q=query,
                           q2=query2,
                           data=dataList,
                           data2=dataList2,
                           q1Invalid=True,
                           q2Invalid=True,
                           form=form)
      return render_template('results.html',
                           title='Results',
                           q=query,
                           data=dataList,
                           q1Invalid=True,
                           q2Invalid=False,
                           form=form)

    if not session['qu2'] == "":
      if not t.checkTerm(session['qu2']):
        return render_template('results.html',
                           title='Results',
                           q=query,
                           q2=query2,
                           data=dataList,
                           data2=dataList2,
                           q1Invalid=False,
                           q2Invalid=True,
                           form=form)
    
    return redirect('/results')

  dataList = listtups_to_listlists(d)
  if not session['qu2'] == "":
    
    dataList2 = listtups_to_listlists(d2)

    return render_template('results.html',
                           title='Results',
                           q=session['qu'],
                           q2=session['qu2'],
                           data=dataList,
                           data2=dataList2,
                           form=form)
  
  return render_template('results.html',
                           title='Results',
                           q=session['qu'],
                           data=dataList,
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
        q1Invalid, q2Invaled = setGraphs(form, t1, t2)
        
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
  return "500 error"
