import sys, os

from flask import request, g
from flask import Flask, render_template, url_for, redirect, session
from db_connect import MyConnection, SigninStatus
from image_classify import ImageClassification



import boto3


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.mysql_db = MyConnection("album")
    return g.mysql_db

@app.route('/signin', methods= ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        print(request.form)
        if "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            connection = get_db()
            flag = connection.signin(username, password)
            
            if flag == SigninStatus.SUCCEED:
                session['username'] = username
                default_albumid = connection.get_default_album(username)
                return redirect(url_for('album', albumid = default_albumid))
            elif flag ==SigninStatus.CREATEUSER:
                message = "You just created a new user. Please sign in using the username and password you entered."
            else:
                message = "The password and username doesn't match. Please try again."
    else:
        message = "Welcome to this album website, please sign in"
    
    return render_template('signin.html', message = message)

@app.route('/signout')
def signout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return '''
        <h1> You have signed out succesfully</h1>
    '''


imc = ImageClassification()




@app.route('/album/<albumid>', methods= ['GET', 'POST'])
def album(albumid):
    global imc
    
    """
    TODO:
    check if the user has signed in and owns this album!!!!
    """
    connection = get_db()
    username = connection.get_user_by_album(albumid)
    albumname = connection.get_albumname_by_albumid(albumid)
    albumlist = connection.get_album_by_user(username)
    if request.method == 'POST':
        # in frontend, the file to upload has an id "image"
        if 'image' not in request.files:
            print("Error: no images")
        else:
            image= request.files['image']
            # if user does not select file, browser will submit an empty part without filename
            if image.filename == '':
                print('Error: no selected file')
            else:
                filename = image.filename.replace(" ", "")
                s3 = boto3.resource(
                    's3',
                    aws_access_key_id="AKIAWPMPWBJM6275X4NG",
                    aws_secret_access_key="XakhSVnxhi3ZK3QrEYWCDoOjYkzHXradP/x+ixXL")
                # how will it behave if there is an existing file of the same name?
                image_path =  albumid + "/" + filename
                
                """
                now if we submit an image of the same name, it will overwirte the old image
                may need to deal with it.
                """
                s3.Bucket('imagerecognizationids').put_object(Key = image_path, Body = image, ACL='public-read')
                
                labels = imc.get_labels(image_path)
                
                connection.insert_photo(filename, albumid, image_path, labels)
                
                print("succeed!!!")
    
    photos = connection.get_photo_and_tag_by_album(albumid)
    
    s3_url = "https://imagerecognizationids.s3.amazonaws.com/"
    
    photolist = []
    for photoid in photos.keys():
        photoinfo = photos[photoid]
        # generate sth like: https://imagerecognizationids.s3.amazonaws.com/4/IMG_0578.jpg
        photoinfo[0] = s3_url + photoinfo[0]
        photolist.append(photoinfo)
    """
    TODO: print the tags of each photo in album.html 
    there is already a row to put it: line 30 of album.html: <h5><a href="#" class="badge badge-info">THIS IS THE PLACE TO PUT TAGS FOR PHOTOS!!!!!</a></h5>
    we can click on the tag to view all photos with this tag, so i have a href="#" here, which will be of real use later(jumping to the page that has all photos of this.
    """
    print("list",albumlist)
    
    return render_template('album.html', photolist = photolist, is_tag_search = False, search_tag = "", username = username, albumid = albumid, albumname = albumname, albumlist = albumlist)


# search all photos of the same tag(not only in this album, but in any other nonprivate album)
@app.route('/album/<albumid>/<tag>', methods= ['GET', 'POST'])
def album_tag_search(albumid, tag):
    connection = get_db()
    username = connection.get_user_by_album(albumid)
    albumname = connection.get_albumname_by_albumid(albumid)
    photos = connection.get_photos_by_tag(username, tag)
    albumlist = connection.get_album_by_user(username)
    s3_url = "https://imagerecognizationids.s3.amazonaws.com/"
    
    photolist = []
    for photoid in photos.keys():
        photoinfo = photos[photoid]
        # generate sth like: https://imagerecognizationids.s3.amazonaws.com/4/IMG_0578.jpg
        photoinfo[0] = s3_url + photoinfo[0]
        photolist.append(photoinfo)
    

    return render_template('album.html', photolist = photolist, is_tag_search = True, search_tag = tag, username = username, albumid = albumid, albumname = albumname, albumlist = albumlist)

# @app.route('/search/<albumid>', methods= ['GET', 'POST'])
# def searchbar_tag_search(albumid):
#     tag = request.form["tag"]
#     print(request.form)
#     return redirect(url_for('album', albumid = albumid, tag = tag))

# for the page that the user want to create a new album
@app.route('/create_album/<username>/', methods= ['GET', 'POST'])
def create_album(username):
    if request.method == 'POST':
        albumname = request.form["albumname"]
        permission = request.form["permission"]
        connection = get_db()
        created_albumid = connection.insert_album(albumname, username, permission)
        return redirect(url_for('album', albumid = created_albumid))
    else:
        return render_template('create_album.html', username = username)

@app.route('/tryrandomthings')
def trytrytry():
    return render_template('layout.html')





if __name__ == '__main__':
    
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.run(debug=False, host='0.0.0.0')