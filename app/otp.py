

def checkAge(age):
    try:
        if(age.isalpha() or (age<1 or age>150)):
            return False
        else:
            return True
    except Exception as e:
        return e
    
print(checkAge(20))