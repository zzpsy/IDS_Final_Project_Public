# This connection code references the MySQL tutorial:
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
import mysql.connector
from mysql import connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from mysql.connector import Error

from enum import Enum, auto
class SigninStatus(Enum):
    CREATEUSER = auto()
    FAIL = auto()
    SUCCEED = auto()

class MyConnection:
    def __init__(self, database):
        self.user = 'admin'
        self.password = 'zhengzhangaws'
        self.host = 'database-1.c4tjsdr1vyb4.us-east-1.rds.amazonaws.com'
        self.database = database
        self.cnx = connector.connect(user=self.user, password= self.password,
                                          host=self.host,
                                          database=self.database)

    
    # if a new user, will create a user for it
    # if an old user, will check
    def signin(self, username, password):
        try:
            cursor = self.cnx.cursor()
            query = ("SELECT * FROM user WHERE username = \'{}\'".format(username))
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append(row)
            if len(result) == 0:
                cursor = self.cnx.cursor()
                print("query is:")
                print("INSERT INTO user VALUES(\'{}\', \'{}\')".format(username, password))
                query = ("INSERT INTO user VALUES(\'{}\', \'{}\')".format(username, password))
                cursor.execute(query)
                
                # we will give each user a default protected album initially
                query =  ("INSERT INTO album(albumname, username, permission) VALUES(\'Default_Album\', \'{}\', \'protected\')".format(username))
                cursor.execute(query)
                self.cnx.commit()
                return SigninStatus.CREATEUSER
            elif len(result) == 1:
                if password != result[0][1]:
                    return SigninStatus.FAIL
                else:
                    return SigninStatus.SUCCEED
            else:
                print("strange errors in signin")
                return SigninStatus.FAIL
        
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                
        # else:
        #     cnx.close()
    
    def get_default_album(self,username):
        cursor = self.cnx.cursor()
        query = ("SELECT albumid FROM album WHERE albumname = \'Default_Album\' AND username = \'{}\'".format(username))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return str(result[0][0])
    
    
    def insert_photo(self, photoname, albumid, image_path, labels):
        cursor = self.cnx.cursor()
        query =  ("INSERT INTO photo(photoname, albumid, photopath) VALUES(\'{}\', {}, \'{}\')".format(photoname, albumid, image_path))
        cursor.execute(query)
        query = ("SELECT LAST_INSERT_ID()")
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        print(result)
        photoid = result[0][0]
        
        for label in labels:
            query =  ("INSERT INTO photo_tag(photoid, tag) VALUES( {}, \'{}\')".format(photoid, label))
            cursor.execute(query)
        self.cnx.commit()
        
    
    # example return result (for album 4 that has two photos, whose photoid are 7 & 11):
    # {7 : [4/IMG_0578.jpg, ["beach","person","sea","fish","ice cream"]] , 
    # 11:  [4/IMG_1234.jpg, ["computer","keyboard","food","music","phone"]]}
    def get_photo_and_tag_by_album(self, albumid):
        cursor = self.cnx.cursor()
        query =  ("SELECT photoid, photopath FROM photo WHERE albumid = {}".format(albumid))
        cursor.execute(query)
        photos = dict()
        for row in cursor:
            # key: photoid
            # value: a tuple
            # the first element is the path to that photo
            # the second element is a list of all tags 
            # for example, a key value pair can be: 
            # 7 : [4/IMG_0578.jpg, ["beach","person","sea","fish","ice cream"]]
            # here, 7 is the photoid, 4 is the albumid
            photos[row[0]] = [row[1],[]]
        
        for photoid in photos:
            query = ("SELECT tag FROM photo_tag WHERE photoid = {}".format(photoid))
            cursor.execute(query)
            for row in cursor:
                photos[photoid][1].append(row[0])
        
        return photos
    
    def get_user_by_album(self, albumid):
        cursor = self.cnx.cursor()
        query =  ("SELECT username FROM album WHERE albumid = {}".format(albumid))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        
        return result[0][0]
        
    
    # search photos in this user's album and in any other nonprivate albums of other users.
    # albumid is where the user clicked on the "search tag"
    def get_photos_by_tag(self, username, tag):
        cursor = self.cnx.cursor()
       
        
        query =  ('''
        SELECT photo.photoid, photo.photopath, album.username 
        FROM photo
        INNER JOIN photo_tag
        ON photo.photoid = photo_tag.photoid
        INNER JOIN album 
        ON photo.albumid = album.albumid
        WHERE 
        (album.username = \'{}\' OR album.permission != \'private\') AND photo_tag.tag = \'{}\'
        '''.format(username, tag))

        cursor.execute(query)
        
        photos = dict()
        for row in cursor:
            # key: photoid
            # value: a tuple
            # the first element is the path to that photo
            # the second element is a list of all tags 
            # the third element is the username
            # for example, a key value pair can be: 
            # 7 : [4/IMG_0578.jpg, ["beach","person","sea","fish","ice cream"], "test_user"]
            # here, 7 is the photoid, 4 is the albumid
            photos[row[0]] = [row[1], [], row[2]]
        
        for photoid in photos:
            query = ("SELECT tag FROM photo_tag WHERE photoid = {}".format(photoid))
            cursor.execute(query)
            for row in cursor:
                photos[photoid][1].append(row[0])
        
        return photos
    
    # insert a new album and return the albumid of this new album
    def insert_album(self, albumname, username, permission):
        cursor = self.cnx.cursor()
        query = ("INSERT INTO album(albumname, username, permission) VALUES(\'{}\', \'{}\', \'{}\')".format(albumname, username, permission))
        cursor.execute(query)
        query = ("SELECT LAST_INSERT_ID()")
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        albumid = result[0][0]
        

        self.cnx.commit()
        return albumid
    
    def get_albumname_by_albumid(self, albumid):
        cursor = self.cnx.cursor()
        query = ("SELECT albumname FROM album WHERE albumid = \'{}\'".format(albumid))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        
        return result[0][0]
    
    def get_album_by_user(self, username):
        cursor = self.cnx.cursor()
        query = ("SELECT albumid, albumname FROM album WHERE username = \'{}\'".format(username))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)

        return result
        
if __name__ == "__main__":
    cnx = MyConnection("album")
    flag = cnx.signin("test_user", "abc123")
    print(flag)
    
    albumid = cnx.get_default_album("test_user")
    print(albumid)
    
    username = cnx.get_user_by_album(7)
    print(username)
    username = cnx.get_user_by_album(2)
    print(username)
    
    print("AAA")
    photos = cnx.get_photos_by_tag("zzabc","water")
    print(photos)
    print("BBB")
    photos = cnx.get_photos_by_tag("test_user","water")
    print(photos)
    
    albumid = cnx.insert_album("just_a_test", "zzabc", "private")
    print(albumid)
    
    albums = cnx.get_album_by_user("test_user")
    print(albums)
    
    albumname = cnx.get_albumname_by_albumid(2)
    print(albumname)
    albumname = cnx.get_albumname_by_albumid(13)
    print(albumname)