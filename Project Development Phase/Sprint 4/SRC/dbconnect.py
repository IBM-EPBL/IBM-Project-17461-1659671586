from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import bcrypt
from sendmail import *

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zvl42723;PWD=hXf4RGalRBp2sQU6",'','')


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=['GET'])
def home():
    if 'email' not in session:
      return redirect(url_for('index'))
    return render_template('index.html',name='Home')
@app.route("/index")
def index():
  return render_template('index.html')

@app.route("/products")
def products():
  return render_template('products.html')

@app.route("/product1")
def product1():
  return render_template('product1.html')

@app.route("/product2")
def products2():
  return render_template('product2.html')

@app.route("/blog")
def blog():
  return render_template('blog.html')

@app.route("/blog1")
def blog1():
  return render_template('blog1.html')

@app.route("/blog2")
def blog2():
  return render_template('blog2.html')

@app.route("/blog3")
def blog3():
  return render_template('blog3.html')

@app.route("/blog4")
def blog4():
  return render_template('blog4.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/contact")
def contact():
  return render_template('contact.html')

@app.route("/cart")
def cart():
  return render_template('cart.html')

@app.route("/cart1")
def cart1():
  return render_template('cart1.html')

@app.route("/cart2")
def cart2():
  return render_template('cart2.html')

@app.route("/sproduct")
def sproducts():
  return render_template('sproduct.html')

@app.route("/register")
def registerhome():
  return render_template('register.html')

@app.route("/adminpage")
def adminpage():
    return render_template('adminpage.html')

@app.route("/shoppingcart")
def shoppingcart():
    return render_template('shoppingcart.html')

@app.route("/payment")
def payment():
    return render_template('payment.html')


@app.route("/registerUser",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    name = request.form['name']
    phn = request.form['phn']
    email = request.form['email']
    psw = request.form['psw']

    if not name or not email or not phn or not psw:
      return render_template('registerUser.html',error='Please fill all fields')
    hash=bcrypt.hashpw(psw.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM user_detail WHERE email=? OR phn=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,phn)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO user_detail(name, email, phn, psw) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phn)
      ibm_db.bind_param(prep_stmt, 4, hash)
      ibm_db.execute(prep_stmt)
      sendMailUsingSendGrid(API,from_email,email,subject,html_content)
      return render_template('registerUser.html',success="You can login")
      
  
    else:
      return render_template('registerUser.html',error='Invalid Credentials')

  return render_template('registerUser.html',name='Home')



@app.route("/loginUser",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      psw = request.form['psw']

      if not email or not psw:
        return render_template('loginUser.html',error='Please fill all fields')
      query = "SELECT * FROM user_detail WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,psw)

      if not isUser:
        return render_template('loginUser.html',error='Invalid Credentials')
      
      isPasswordMatch = bcrypt.checkpw(psw.encode('utf-8'),isUser['PSW'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('loginUser.html',error='Invalid Credentials')

      session['email'] = isUser['EMAIL']
      return redirect(url_for('home'))

    return render_template('loginUser.html',name='Home')

@app.route("/registerAdmin",methods=['GET','POST'])
def adregister():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    phn = request.form['phn']
    psw = request.form['psw']

    if not name or not email or not phn or not psw:
      return render_template('registerAdmin.html',error='Please fill all fields')
    hash=bcrypt.hashpw(psw.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM admin_detail WHERE email=? OR phn=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,phn)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO admin_detail(name, email, phn, psw) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phn)
      ibm_db.bind_param(prep_stmt, 4, hash)
      ibm_db.execute(prep_stmt)
      sendMailUsingSendGrid(API,from_email,email,subject,html_content)
      return render_template('registerAdmin.html',success="You can login")
    else:
      return render_template('registerAdmin.html',error='Invalid Credentials')

  return render_template('registerAdmin.html',name='Home')

@app.route("/loginAdmin",methods=['GET','POST'])
def adlogin():
    if request.method == 'POST':
      email = request.form['email']
      psw = request.form['psw']

      if not email or not psw:
        return render_template('loginAdmin.html',error='Please fill all fields')
      query = "SELECT * FROM admin_detail WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,psw)

      if not isUser:
        return render_template('loginAdmin.html',error='Invalid Credentials')
      
      isPasswordMatch = bcrypt.checkpw(psw.encode('utf-8'),isUser['PSW'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('loginAdmin.html',error='Invalid Credentials')

      session['email'] = isUser['EMAIL']
      return redirect(url_for('adminpage'))

    return render_template('loginAdmin.html',name='Home')


@app.route("/addproduct",methods=['GET','POST'])
def addproduct():
  if request.method == 'POST':
    types=request.form['cc']
    name = request.form['name']
    image = request.form['image']
    rate = request.form['rate']
    categorie = request.form['categorie']
    if types =='col1':
      insert_sql = "INSERT INTO COL1(name, image, categorie,rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)
    if types =='col2':
      insert_sql = "INSERT INTO  COL2(name, image, categorie,rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)
    if types =='col3':
      insert_sql = "INSERT INTO  COL3(name, image, categorie,rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)
    if types =='col4':
      insert_sql = "INSERT INTO  COL4(name, image, categorie,rate) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 4, rate)
      ibm_db.execute(prep_stmt)
        
  return render_template('addproduct.html',success="You have entered the details")

@app.route("/data")
def display():
  col1_list=[]
  col2_list=[]
  col3_list=[]
  col4_list=[]

  #selecting_col1
  sql = "SELECT * FROM COL1"
  stmt = ibm_db.exec_immediate(conn, sql)
  col1 = ibm_db.fetch_both(stmt)
  while col1 != False :
      col1_list.append(col1)
      col1 = ibm_db.fetch_both(stmt)
  print(col1_list)
  
 #selecting_col2
  
  sql1="SELECT * FROM COL2"
  stmt1 = ibm_db.exec_immediate(conn, sql1)
  col2=ibm_db.fetch_both(stmt1)
  while col2 != False :
      col2_list.append(col2)
      col2 = ibm_db.fetch_both(stmt1)
  print(col2_list) 

#selecting_col3
  sql2="SELECT * FROM COL3"
  stmt2 = ibm_db.exec_immediate(conn, sql2)
  col3=ibm_db.fetch_both(stmt2)
  while col3 != False :
      col3_list.append(col3)
      col3 = ibm_db.fetch_both(stmt2)
  print(col3_list)

  #selecting_col4
  sql3="SELECT * FROM COL4"
  stmt3 = ibm_db.exec_immediate(conn, sql3)
  col4=ibm_db.fetch_both(stmt3)
  while col4 != False :
      col4_list.append(col4)
      col4 = ibm_db.fetch_both(stmt3)
  print(col4_list)  
  #returning to HTML
  return render_template('pro.html',col1= col1_list,col2=col2_list,col3=col3_list,col4=col4_list)

@app.route('/add', methods=['POST'])
def add_product_to_cart():
	try:
		_quantity = int(request.form['quantity'])
		_code = request.form['code']
		# validate the received values
		if _quantity and _code and request.method == 'POST':
			query = "SELECT * FROM user_detail WHERE email=? OR phn=?"
			stmt = ibm_db.prepare(conn, query)
			ibm_db.bind_param(stmt,1,_code)
			ibm_db.execute(stmt)
            
			row = ibm_db.fetch_assoc(stmt)
			itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price': _quantity * row['price']}}
			
			all_total_price = 0
			all_total_quantity = 0
			
			session.modified = True
			if 'cart_item' in session:
				if row['code'] in session['cart_item']:
					for key, value in session['cart_item'].items():
						if row['code'] == key:
							#session.modified = True
							#if session['cart_item'][key]['quantity'] is not None:
							#	session['cart_item'][key]['quantity'] = 0
							old_quantity = session['cart_item'][key]['quantity']
							total_quantity = old_quantity + _quantity
							session['cart_item'][key]['quantity'] = total_quantity
							session['cart_item'][key]['total_price'] = total_quantity * row['price']
				else:
					session['cart_item'] = array_merge(session['cart_item'], itemArray)

				for key, value in session['cart_item'].items():
					individual_quantity = int(session['cart_item'][key]['quantity'])
					individual_price = float(session['cart_item'][key]['total_price'])
					all_total_quantity = all_total_quantity + individual_quantity
					all_total_price = all_total_price + individual_price
			else:
				session['cart_item'] = itemArray
				all_total_quantity = all_total_quantity + _quantity
				all_total_price = all_total_price + _quantity * row['price']
			
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
			
			return redirect(url_for('.products'))
		else:			
			return 'Error while adding item to cart'
	except Exception as e:
		print(e)
        
@app.route('/empty')
def empty_cart():
	try:
		session.clear()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		
		if all_total_quantity == 0:
			session.clear()
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		
		#return redirect('/')
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False
  
    
@app.route("/home")
def dis():
  col3_list=[]
  sql2="SELECT * FROM COL3"
  stmt2 = ibm_db.exec_immediate(conn, sql2)
  col3=ibm_db.fetch_both(stmt2)
  while col3 != False :
      col3_list.append(col3)
      col3 = ibm_db.fetch_both(col3)
  print(col3_list) 
  return render_template('pro.html',col3=col3_list)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

