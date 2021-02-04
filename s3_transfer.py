#Reference: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
import boto3 
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget

#CREDENTIAL SETUP TO SWITCH ROLES:
# Create an STS client object that represents a live connection to the 
# STS service
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
assumed_role_object=sts_client.assume_role(
    RoleArn="arn:aws:iam::589772831734:role/role4dan",
    RoleSessionName="AssumeRoleSession1"
)

# From the response that contains the assumed role, get the temporary 
# credentials that can be used to make subsequent API calls
credentials=assumed_role_object['Credentials']

# Use the temporary credentials that AssumeRole returns to make a 
# connection to Amazon S3  
s3_resource=boto3.resource(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
)

# Use the Amazon S3 resource object that is now configured with the 
# credentials to access your S3 buckets. 
for bucket in s3_resource.buckets.all():
    print(bucket.name)

#SETTING UP THE APPLICATION WINDOW:
app = QApplication([])
window = QMainWindow()
widget = QWidget(window)
layout = QGridLayout()
widget.setLayout(layout)

#The Hello World Label:
label = QLabel()
label.setText('Hello world!')

#Added to the first row and column
layout.addWidget(label, 0, 0)

#Start the Qt event loop, which starts the app:
window.setCentralWidget(widget)
window.show()
app.exec_()






# s3 = boto3.client('s3')
# s3.upload_file('hello.txt', 'rewrite')

# #Uplioad files from a system folder to s3 bucket
# # Upload file
# src_folder = './input/'
# dest_folder = 'Output/'
# for file in os.listdir(src_folder):
#  s3.meta.client.upload_file(src_folder+file, bucket_name, dest_folder+file)

#  # Retreive all files bucket
# for obj in bucket.objects.all():
#     print(obj.key)

# # Retreive files of specific folder of bucket
# for obj in bucket.objects.filter(Prefix='Input/'):
#     print(obj.key)


