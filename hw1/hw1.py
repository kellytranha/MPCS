from reservation import App

def reserve(name):
    return("Hello {}!".format(name))


if __name__ == '__main__':
    print('MPCS, Inc. - Laboratory Coworking Space Provider Management Application')
    print('=======================================================================')
    print('Choose one of the options:')
    print('For example, if you want to make a reservation, type 1 and hit enter')
    print('1- Make reservations')
    print('2- Cancel reservations')
    print('3- Generate reservation report')
    print('4- List financial transactions')
    print('5- List reservations for a customer')
    
    option = input("Option: ")
    app = App();
    
    if option == '1':
        app.make()
    elif option == '2':
        app.cancel()
    elif option == '3':
        app.generat()
    elif option == '4':
        app.list_fin()
    # assume users choose 1-5
    else:
        app.list_rev()

    