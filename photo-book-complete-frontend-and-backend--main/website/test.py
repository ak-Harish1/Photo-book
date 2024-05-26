from supabase import create_client,Client


supabase_url = 'https://ifrfizobgwcmvvivvsiv.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmcmZpem9iZ3djbXZ2aXZ2c2l2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgwOTU5MjcsImV4cCI6MTk5MzY3MTkyN30.o9xnPJkaj381ZIY6oftDekEz1yevCWM81cFxt-UdZ6g'
supabase_client = create_client(supabase_url, supabase_key)
# res1 = supabase_client.table("UserPhotos").select("*").eq("display_home_page","true").execute()

# import boto3

# s3 = boto3.client('s3')



# magic_link_request_result = supabase_client.auth.reset_password_email('viratkohli16072004@gmail.com')
# print(magic_link_request_result)
# if magic_link_request_result:
#     print('confirmation  will send to your mail clck that and set new password')
# else:
#     print("not sent")
# # res = supabase_client.auth.get_user()
# # id=res.user.id
# bucket_name='bucker-name-123'
# user_id='public_photos/'
# objects = s3.list_objects(Bucket=bucket_name, Prefix=user_id)['Contents']
# # print('objs ',objects)
# urls=[]
# # urls1=[]
# for obj in objects:
#     urls.append(url)
# print(' all link is ',urls)
# photos = supabase_client.table("UserPhotos").select("*").eq("display_home_page","true").execute()
# for phot in photos.data:
#     a=phot.get("user_id")
#     b=phot.get("photoname")
# url = s3.generate_presigned_url("get_object",Params={"Bucket":"bucker-name-123","Key":f"{a}/{b}"},)
# print(url)
# bucket_name = 'bucker-name-123'
# res = supabase_client.auth.get_user()
# user_id=res.user.id
#         # s3.upload_fileobj(buf,bucket_name,key)
# photo_objects = s3.list_objects(Bucket=bucket_name, Prefix=user_id)['Contents']
# photo_urls = []
# for photo_obj in photo_objects:
#     photo_url = s3.generate_presigned_url('get_object',
#     Params={
#         'Bucket': bucket_name,
#         'Key': photo_obj['Key'] 
#         # key- location of the photo 
#         },
#         # ExpiresIn=3600
#     )
#     # print(photo_url)
#     photo_urls.append(photo_url) 
#     # if permission =='yes':
#     #     photo_data = {'user_id': user_id, 'photoname': photoname,'display_home_page':display_home_page,'photo_url':photo_url}
#     # supabase_client.from_('UserPhotos').insert(photo_data).execute()
# <form action="{{ url_for('delete_user') }}" method="post">
#     <button type="submit" class="my-btn">Delete Account</button>
# </form>
# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     # Get the current user's information
#     user = supabase_client.auth.get_user()
#     user_id = user.user.id
#     email = user.user.email
#     # Delete the user from the users table
#     supabase_client.table('Users').delete().eq('id', id).execute()
#     # Delete the user's photos from the userphotos table
#     supabase_client.table('UserPhotos').delete().eq('user_id', user_id).eq('permission', 'no').execute()
#     # Log the user out
#     supabase_client.auth.sign_out()
#     # Redirect the user to the home page
#     flash(f"Your account ({email}) has been deleted.", "success")
#     return render_template('home.html')
# if __name__ == "__main__":
#     # app = create_app()
#     app.run(debug=True)
 # new_password = request.form.get('new_password')
# new_password=session.get('new_password')
# if new_password:
#  password=new_password
# email='ragnorlothbrok2004@gmail.com'
# new_password='654321'           
# user=supabase_client.auth.get_user()
# supabase_client.auth.update_user({"id": user['id'],"password": new_password })
# Get the access token from the authentication response
# auth_res = supabase_client.auth.sign_in(email=email, password=new_password)
# access_token = auth_res["access_token"]
# Update the user's password using the access token
# new_password = "newpassword123"
# supabase_client.auth.update_user({"password": new_password}, access_token=access_token)
# result = supabase_client._get_auth_headers(
#     email="ragnorlothbrok2004@gmail.com",
#     password="123456")
# Access session details
# print(result['session'])
# from flask import Flask 
# app = Flask(__name__)
# @app.route('/upload-image', methods=['POST'])
# import supabase
import os 
# with open("login.jpeg", 'rb+') as file:
#     # res = supabase.storage().from_("photobook").upload("dest.jpeg",os.path.abspath("login.jpeg"))
#     res = supabase_client.storage.from_("photobook").upload("dest.jpeg",os.path.abspath("login.jpeg"))



# email=''
# password='123456'
# try:

#     res=supabase_client.auth.sign_in_with_password({"email":'ragnorlothbrok2004@gmail.com',"password":'123456'})
#     with open('login.jpeg','rb+') as f:
#         supabase_client.storage.from_('photobook').upload('sam.jpeg',os.path.abspath('login.jpeg'))
# except Exception as e:
#     print(str(e))

# a=supabase_client.auth.get_user({'email':'viratkohli16072004@gmail.com'})
# print(a)



import secrets

# generate a random token
token = secrets.token_urlsafe(32)

# alternatively, generate a token with a specific length
token_length = 64
toke = secrets.token_urlsafe(token_length)[:token_length]
print(toke)
print(token)
