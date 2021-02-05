#Reference: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
#Reference: https://www.codementor.io/blog/desktop-app-pyqt-8jwfnotu1y

import boto3 
import PyQt5
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog
  
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


# for obj in bucket.objects.filter(Prefix='Input/'):
#     print(obj.key)


#SETTING UP THE APPLICATION WINDOW:
app = QApplication([])
window = QMainWindow()
screen = QWidget()
layout = QGridLayout()
screen.setLayout(layout)

#Two labels that show the freelancer's yearly income and the 
#top marginal tax rate they should be prepared for
yearly_income = QLabel()
yearly_income.setText('Number of Songs: 0')
layout.addWidget(yearly_income, 0, 0)

tax_rate = QLabel()
tax_rate.setText('Number of Albums: 0')
layout.addWidget(tax_rate, 0, 1)

#Creating a Button and Opening a QInputDialog
button = QPushButton()
button.setText('Calculator')

def open_calculator():
    value, ok = QInputDialog.getDouble(
        window, # parent widget
        'Tax Calculator', # window title
        'Yearly Income:', # entry label
        min=0.0,
        max=1000000.0,
    )
    if not ok:
        return
    yearly_income.setText('Yearly Income: ${:,.2f}'.format(value))
    if value <= 9700:
        rate = 10.0
    elif value <= 39475:
        rate = 12.0
    elif value <= 84200:
        rate = 22.0
    elif value <= 160725:
        rate = 24.0
    elif value <= 204100:
        rate = 32.0
    tax_rate.setText('Highest Marginal Tax Rate: {}%'.format(rate))

#Connect the callback to the button and position it in the layout:
button.clicked.connect(open_calculator)
layout.addWidget(button, 1, 0, 1, 2)

#DISPLAYING A TABLE OF DATA:

#Defining table columns: 
columns = ('Week', 'Hours Worked', 'Hourly Rate', 'Earned Income')

#Use some placeholder data:
table_data = [
    [7, 40.0, 100.0],
    [8, 37.5, 85.0],
    [9, 65, 150.0],
]

#Set up the QTableWidget to create the table.ArithmeticError
#Setting the number of columns that will be displayed and their labels
table = QTableWidget()
table.setColumnCount(len(columns))
table.setHorizontalHeaderLabels(columns)

#Set the # of rows that will be displayed which will match the #
#Of rows we have in table_data:
table.setRowCount(len(table_data))

#Use the QTableWidgetItem to Display Data in the Table:
#Search through each row's vaues from the table_data.ArithmeticError
#Loop through each column's values, create a QTableWidgetItem, and store in the exact table
#cell where it needs to be. ALSO calculate the sum and store it in the last column of the row. 
for row_index, row in enumerate(table_data):
    # Set each column value in the table
    for column_index, value in enumerate(row):
        item = QTableWidgetItem(str(value))
        table.setItem(row_index, column_index, item)
    # Calculate the total and add it as another column
    table.setItem(row_index, 3, QTableWidgetItem(str(row[1] * row[2])))

#Add the table to the layout in the third row, spanning two columns: 
layout.addWidget(table, 2, 0, 1, 2)




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


#Sets the screen widets as the one to display and shows it.
#The app.exec_ kickstarts the Qt event loop 
window.setCentralWidget(screen)
window.setWindowTitle('Meusick Content Manager')
window.setMinimumSize(800, 500)
window.show()

app.exec_()
