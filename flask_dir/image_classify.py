import boto3
"""
AWS Image Rekognition references:
https://www.youtube.com/watch?v=SZa2HfR-9Xc

S3 bucket references:
https://www.youtube.com/watch?v=7gqvV4tUxmY

boto3 references:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

"""
class ImageClassification:
    def __init__(self):
        
        self.client = boto3.client(
            "rekognition",
            aws_access_key_id="AKIAWPMPWBJM6275X4NG",
            aws_secret_access_key="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"
            )
        
        # TODO: possibly need to delete this self.s3 later
        # well we don't really need an instance of s3 for now, but maybe we will need it later
        self.s3 = boto3.client(
            's3',
            aws_access_key_id="AKIAWPMPWBJM6275X4NG",
            aws_secret_access_key="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")
    
    
    def get_labels(self, image_file_name):
        # this function will detect an existing image in S3 bucket
        # image_name is the file name in that S3 bucket, such as "test.jpg"    
        
        # file_obj = self.s3.get_object(Bucket = "imagerecognizationids", Key = "test.jpg")
        # file_content = file_obj["Body"].read()
        
        
        response = self.client.detect_labels(Image = {"S3Object": {"Bucket":"imagerecognizationids", "Name":image_file_name}}, MaxLabels = 5, MinConfidence = 70)
        # print(response)
        
        labels = []
        for label_json in response['Labels']:
            labels.append(label_json['Name'])
        
        print(labels)
        
        return labels
    

        
if __name__ == '__main__':
    
   ic = ImageClassification()
   # ic.get_labels("test.jpg")
   ic.get_labels("IMG_2842.JPG")
   