# Data Engineering System Final Project: Album
#### This is the repository for an independent project built by Zheng Zhang(zz211) at Duke University. 
## Demo Video
#### You can click on the image below to watch the video demonstration.
[![demo video](https://github.com/zzpsy/IDS_Final_Project_Public/blob/master/resource/youtube%20screenshot.png)](https://www.youtube.com/watch?v=3Xht7LwqyMQ "demo video")
## Description
#### This project is an album web app created for the course IDS 706 Data Engineering Systems.
#### Tools/framwork: 
1. Flask
2. AWS(EC2, S3, RDS, Rekognition, CodeBuild)
3. Docker
4. Bootstrap
#### Main functionalities: 
1. Each user can create multiple albums/set different permissions for different albums/upload & delete photos to the albums.
2. The website will do image classification for the uploaded photos(the album will automatically "tag" the photos)
3. The user can search a photo of the same kind in other albums that he/she has permission to access.
## Architecture:
![alt text](https://github.com/zzpsy/IDS_Final_Project_Public/blob/master/resource/architecture.png?raw=true)
## Example webpages:
#### 1. An user creating a new album
![alt text](https://github.com/zzpsy/IDS_Final_Project_Public/blob/master/resource/screenshot3.png?raw=true)
#### 2. An user visting one of his/her own albums
![alt text](https://github.com/zzpsy/IDS_Final_Project_Public/blob/master/resource/screenshot1.png?raw=true)
#### 3. An user uploading a new photo(the backend will automatically classify the tags that the photo belongs to after it is uploaded. The result will be stored and displayed in frontend).
![alt text](https://github.com/zzpsy/IDS_Final_Project_Public/blob/master/resource/screenshot4.png?raw=true)
#### 4. An user searching for photos with food in all of the albums he/she has permission to.
![alt text](https://github.com/zzpsy/IDS_Final_Project_Public/blob/master/resource/screenshot2.png?raw=true)
