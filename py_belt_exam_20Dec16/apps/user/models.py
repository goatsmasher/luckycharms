from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager
import re, datetime, bcrypt
# import mixin

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
SPACE_REGEX = re.compile(r'\S+')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+=_-]+$')
UPPER_CASE_REGEX = re.compile(r'[A-Z]')
NUMBER_REGEX = re.compile(r'[0-9]+')
ILLEGAL_REGEX = re.compile(r'[~`()+={}|\\:;\'\"<>,.?/]')

def validateLength(value):
    if len(value) < 4:
        raise ValidationError('{} must be longer than 3 characters'.format(value))

def convertDate(value):
    return datetime.datetime.strptime(value, '%m/%d/%Y')

def validateSignup(data):
    valid = True
    errors = []
    if len(data['first_name']) < 1:
        errors.append("First name must not be empty!")
        valid = False
    elif not NAME_REGEX.match(data['first_name']):
        errors.append("First name must contain letters only!")
        valid = False
    if len(data['last_name']) < 1:
        errors.append("Last name must not be empty")
        valid = False
    elif not NAME_REGEX.match(data['last_name']):
        errors.append("Last name must contain letters only!")
        valid = False
    if len(data['email']) < 1:
        errors.append("Email must not be empty!")
        valid = False
    elif not EMAIL_REGEX.match(data['email']):
        errors.append("Email must be valid")
        valid = False
    if len(data['password']) < 8:
        errors.append("Password must be more than 8 characters!")
        valid = False
    elif not UPPER_CASE_REGEX.search(data['password']):
        errors.append("Must contain at least 1 uppercase letter.")
        valid = False
    elif not NUMBER_REGEX.search(data['password']):
        errors.append("Must contain at least 1 number.")
        valid = False
    elif ILLEGAL_REGEX.search(data['password']):
        errors.append("Password must not contain illegal characters (~`()+={}|\\:;\'\"<>,.?/)") #~`()+={}|\\:;\'\"<>,.?/
        valid = False
    if data['confirm_password'] != data['password']:
        errors.append("Password not confirmed.")
        valid = False
    # if convertDate(data['dob']) > datetime.datetime.today():
    #     errors.append("Date invalid. Check format and ensure it's in the past.")
    #     valid = False

    response = {
        'errors': errors,
        'status': valid
    }
    return response

class UserManager(models.Manager):
    def signin(self, postData):
        errors = []
        response = {}
        user = self.filter(email = postData['email'])
        if not user:
            response['status'] = False
            errors.append('User not found')
        else:
            if bcrypt.checkpw(postData['password'].encode('utf-8'), user[0].password.encode('utf-8')):
                response['user_id'] = user[0].id
                response['status'] = True
            else:
                errors.append('Invalid email/password')
        if errors:
            response['status'] = False
            response['errors'] = errors
        return response

    def signup(self, postData):
        errors = []
        response = {}
        #Validate form data
        dataResponse = validateSignup(postData)
        if not dataResponse['status']:
            for error in dataResponse['errors']:
                errors.append(error)
        if not EMAIL_REGEX.match(postData['email']):
            error.append('Email error')
        if postData['password'] != postData['confirm_password']:
            errors.append('Confirm password did not match.')
        elif not PASSWORD_REGEX.match(postData['password']):
            errors.append('Password must blah.')

        # Compile errors and send to response messages
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
            response['user'] = self.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=bcrypt.hashpw(postData['password'].encode('utf-8'),bcrypt.gensalt())
                )
        return response




class User(models.Model):
    first_name = models.CharField(max_length=100, validators = [validateLength])
    last_name = models.CharField(max_length=100, validators = [validateLength])
    email = models.EmailField(max_length=255, validators = [validateLength], unique=True, default='') #write new user for each email invite and attach them to event
    password = models.CharField(max_length=255, validators = [validateLength])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    avatar = models.CharField(max_length=255, default='')
    friends = models.ManyToManyField('self')
    address = models.ForeignKey(Address)
    objects = UserManager()

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    allow_others = models.BooleanField(deafult=False)
    creater_approve_other_invites = models.BooleanField(deafult=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address)

class Invited(models.Model):
    check_if_user = models.ForeignKey(User) #we can use this to traverse to user table to check if the email is already registered? possible in the future we can just notify the user on their dashboard they have a pending invite
    to_event = models.ForeignKey(Event)
    status = models.CharField(default="Pending") #we can display and count the number of people going from status
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    location_name = models.CharField(max_length=50)
    address_primary = models.CharField(max_length=50) #read it is better to save these fields as text because what if address has a 1/2 or 123'B' Street Ave
    address_street = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    related_message = models.ForeignKey(Message)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

# class Poll(models.Model):