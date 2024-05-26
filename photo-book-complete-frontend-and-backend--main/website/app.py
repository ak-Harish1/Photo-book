from flask import Flask, render_template, request, redirect, session,flash
import supabase
import os
import boto3
from PIL import Image,ImageDraw,ImageFont
from datetime import timedelta
import gotrue
import secrets

# token = secrets.token_urlsafe(32)
s3 = boto3.client('s3')
app = Flask(__name__)
app.secret_key = 'key'
supabase_url = 'https://ifrfizobgwcmvvivvsiv.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmcmZpem9iZ3djbXZ2aXZ2c2l2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgwOTU5MjcsImV4cCI6MTk5MzY3MTkyN30.o9xnPJkaj381ZIY6oftDekEz1yevCWM81cFxt-UdZ6g'
supabase_client = supabase.create_client(supabase_url, supabase_key)
# Set session lifetime to 60 minutes
app.permanent_session_lifetime = timedelta(minutes=60)

@app.route('/',methods=['GET'])
def home():
            user_id=session.get('user_id')
            if user_id:
                    photos1 = supabase_client.table("UserPhotos").select("*").eq("display_home_page","true").execute()
                    photos=[]
                    for phot in photos1.data:
                        a=phot.get("user_id")
                        b=phot.get('photoname')
                        url = s3.generate_presigned_url("get_object",Params={"Bucket":"bucker-name-123","Key":f"{a}/{b}"},)
                        photos.append(url)
                    return render_template('home.html',photos=photos)
            else:
                photos1 = supabase_client.table("UserPhotos").select("*").eq("display_home_page","true").execute()
                photos=[]
                for phot in photos1.data:
                    a=phot.get("user_id")
                    b=phot.get('photoname')
                    url = s3.generate_presigned_url("get_object",Params={"Bucket":"bucker-name-123","Key":f"{a}/{b}"},)
                    photos.append(url)
                return render_template('home.html',photos=photos)
            
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
        try:
            if request.method == 'POST':
                name = request.form['name']                                          
                email = request.form['email']                                                         
                password = request.form['password']
                # Sign up the user with Supabase
                # Store the user's name, email, and password in session
                session['name'] = name
                session['email'] = email
                session['password'] = password
                name = session.get('name')
                email = session.get('email')
                password = session.get('password')
                user_exists=supabase_client.table('Users').select('id').eq('email',email).execute()
                if user_exists.data != []:
                    flash('Email address already exists')
                    return render_template('signup.html')
                else:
                    res = supabase_client.auth.sign_up({'name':name,'email': email, 'password': password})
                    User_id = res.user.id
                    session['User_id']=User_id
                    session.get(User_id)
                    user_data = {'name': session['name'], 'email':session[ 'email'], 'password':session['password'],'User_id':User_id}
                    supabase_client.table('Users').insert([user_data]).execute()
                    return render_template('login.html')
        except gotrue.errors.AuthApiError as e:
            flash(str(e))
            return render_template('signup.html')
        else:
            return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            res = supabase_client.auth.sign_in_with_password({"email":email, "password":password})
            user_id=res.user.id
            session['user_id']=user_id
            session['email']=email
            return redirect('/')
        except gotrue.errors.AuthApiError as e:
            flash(str(e))
            return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/myposts',methods=['GET','POST'])
def myposts():
    if request.method == 'POST':
        try:
                user = supabase_client.auth.get_user()
                user_id=user.user.id 
                file = request.files['photo']
                photoname = file.filename
                file_path = os.path.join('stat', photoname)  # path to save the uploaded file
                file.save(file_path)
                text='PB'
                with open(file_path,'rb') as f:
                    image = Image.open(f)
                    draw=ImageDraw.Draw(image)
                    font = ImageFont.truetype('arial.ttf', size=36)
                    textwidth, textheight = draw.textsize(text, font)
                    width, height =image.size 
                    x=width/2-textwidth/2
                    y=height-textheight-300
                    draw.text((x,y), text, font=font) 
                image.save(file_path,format='JPEG')
                with open(file_path,'rb') as f:
                    bucket_name = 'bucker-name-123'
                    key = f'{user_id}/{photoname}'     # creating a folder in the name of user_id in s3 bucket
                    #water marking
                    # upload the photos in the bucket
                    s3.upload_fileobj(f,bucket_name,key)
                os.remove(file_path)
                # Generate pre-signed URLs for each photo object in the bucket
                permission=request.form.get('permission')
                if permission =='yes':
                        bucket_name = 'bucker-name-123'
                        display_home_page=True
                        photo_data = {'user_id': user_id, 'photoname': photoname,'display_home_page':display_home_page}
                        photo_objects = s3.list_objects(Bucket=bucket_name, Prefix=user_id)['Contents']
                        photo_urls = []
                        #generate urls for permssion =yes
                        for photo_obj in photo_objects:
                            photo_url = s3.generate_presigned_url('get_object',    # for sharing photos in home page
                            Params={
                                'Bucket': bucket_name,
                                'Key': photo_obj['Key'] 
                                # key- location of the photo 
                                },# ExpiresIn=3600
                            )
                            photo_urls.append(photo_url) 
                        photo_data = {'user_id': user_id, 'photoname': photoname,'display_home_page':display_home_page}
                        supabase_client.table('UserPhotos').insert(photo_data).execute()
                        message='Photo uploaded sucessfully'
                        return render_template('myposts.html',photo_urls=photo_urls,message=message)
                else:
                        bucket_name = 'bucker-name-123'
                        user = supabase_client.auth.get_user()
                        user_id=user.user.id 
                        photo_urls = []
                        photo_objects = s3.list_objects(Bucket=bucket_name, Prefix=user_id)['Contents']

                        for photo_obj in photo_objects:
                            photo_url = s3.generate_presigned_url(
                                'get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': photo_obj['Key']  # key- location of the photo 
                                },   # ExpiresIn=3600
                            )
                            photo_urls.append(photo_url)       
                        display_home_page=False
                        photo_data = {'user_id': user_id, 'photoname': photoname,'display_home_page':display_home_page}
                        supabase_client.from_('UserPhotos').insert(photo_data).execute()
                        message = "Uploaded successfully"
                        return render_template('myposts.html' , photo_urls = photo_urls , message = message)
        except gotrue.errors.AuthApiError as e:
                flash(str(e))
                return render_template('myposts.html')
        except Exception as e:
            flash(str(e))
            return render_template('myposts.html')
    user = supabase_client.auth.get_user()
    user_id=user.user.id 
    bucket_name = 'bucker-name-123'
    photo_urls = []
    photo_objects = s3.list_objects(Bucket=bucket_name, Prefix=user_id)['Contents']
    for photo_obj in photo_objects:
        photo_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': photo_obj['Key']  # key- location of the photo 
            },   # ExpiresIn=3600
        )
        photo_urls.append(photo_url)  
    return render_template('myposts.html',photo_urls=photo_urls) 
   
@app.route('/signout')
def signout():
    session.clear()
    supabase_client.auth.sign_out()
    flash('You logged out, login again to access photo-book')
    return render_template('index.html')   

@app.route('/delete_user', methods=['POST'])
def delete_user():
    # # Get the current user's information
    user = supabase_client.auth.get_user()
    user_id =user.user.id
    # auth=supabase_client.auth
    # supabase_client.auth.api.deleteUser(user_id)
    # email = session.get('email')
    # # Delete the user from the users table
    # # photos = supabase_client.table("UserPhotos").select("*").eq("display_home_page","true").execute()
    # supabase_client.table('Users').delete().eq('User_id', User_id).execute()
    # # Delete the user's photos from the userphotos table
    # supabase_client.table('UserPhotos').delete().eq('User_id', User_id).eq('permission', 'no').execute()
    # # Log the user out
    # supabase_client.auth.sign_out()
    # # Redirect the user to the home page
    # flash(f"Your account has been deleted.", "success")
    return render_template('home.html')

@app.route('/password_reset', methods=['GET','POST'])
def reset_password():
        if request.method == 'POST':
            email=request.form['email']
            session['email']=email
            email=session.get('email')
            #generate magic link for the user
            try:
                #generate unique token for each user
                magic_link_request_result = supabase_client.auth.reset_password_email(email)
                if magic_link_request_result is None:
                    flash('check your mail')
                    token = secrets.token_urlsafe(32)
                    session['token'] = token
                    print("token is ",token)
                    return render_template('password_reset.html')
            except Exception as e:
                print(e)
        return render_template('password_reset.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    # token=session.get(token)
    # print('token 1 is this ',token)
    # if token:
    if request.method == 'POST':
        try:
            session.get('token')
            email = request.form['email']
            new_password = request.form['new_password']
            # Update new password in the supabase in table name Users
            supabase_client.auth.update_user({"email": email, "password": new_password})
            supabase_client.from_('Users').update({'password': new_password}).eq('email', email).execute()
            flash('Password is updated')
            return redirect('/login')
        except gotrue.errors.AuthApiError as e:
            flash(str(e))
            return render_template('reset.html')
    return render_template('reset.html')


