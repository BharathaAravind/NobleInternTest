import tornado.ioloop
import tornado.web
import Settings
from Models import model

#Main class for application that redirects to all the handlers
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", LoginHandler),
            (r"/login",LoginHandler),
            (r"/logout",LogoutHandler),
            (r"/dashboard",DashBoardHandler),
            (r"/tradeCheck",TradebalanceCheckHandler),
        ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
            "cookie_secret": Settings.COOKIE_SECRET,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

#Login handler that handles login that intiates session and redirects to dashboard
class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        print 'inside login get req'
        if self.get_cookie('username') != None:
            self.redirect('/dashboard')
        else:
            message = ''
            self.render("login.html", message = message)
    def post(self):
        print 'inside login post request'
        username = self.get_argument('username','no data found')
        password = self.get_argument('password','no data found')
        if username == password:
            self.set_cookie('username', username)
            self.redirect('/dashboard')
        else:
            message = 'Login unsuccessful. Both username and password are same.'
            self.render("login.html", message = message)

#Logout handler that clears session
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        print 'inside logout get method'
        self.clear_cookie('username')
        message = ''
        self.render("login.html", message=message)

#dashboard handler that loads the  dashboard view
class DashBoardHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('username') == None:
            self.redirect('/login')
        else:
            print 'inside dashboard'
            username = self.get_cookie('username')
            user1 = model.getUserBalances(username)
            errorMessage = ''
            successMessage = ''
            self.render('dashboard.html',userdetails=user1, errormessage=errorMessage, successmessage=successMessage)

#handler that handles trades performed my views
class TradebalanceCheckHandler(tornado.web.RequestHandler):

    def post(self):
        if self.get_cookie('username') == None:
            self.redirect('/login')
        else:
            print 'inside trade checker'
            username = self.get_cookie('username')
            user1 = model.getUserBalances(username)
            errorMessage = ''
            successMessage = 'Trade Successful!'
            amountTobetraded = self.get_argument('amountToTrade')
            try:
                amountTobetraded = int(amountTobetraded)
            except:
                errorMessage = 'Only numbers are accepted'

            totalamountBalance = user1.tradingbalance + user1.checkingbalance
            print totalamountBalance
            print amountTobetraded
            tempAmount = amountTobetraded + 0.2 * amountTobetraded
            if totalamountBalance >= tempAmount:
                successMessage = ''
                if user1.tradingbalance >= amountTobetraded:
                    user1.tradingbalance = user1.tradingbalance - amountTobetraded
                else:
                    if user1.tradingbalance > 0:
                        user1.checkingbalance = amountTobetraded - user1.tradingbalance
                        user1.tradingbalance = 0
                    else:
                        user1.checkingbalance = totalamountBalance - amountTobetraded
                        user1.tradingbalance = 0
                model.updateUserBalances(username, user1)
                successMessage = 'Trade Successful. Amount updated in your balance'
                errorMessage= ''
                print 'trade permitted'
            else:
                amp = tempAmount - totalamountBalance
                successMessage = ''
                errorMessage = 'The amount balance is low. Add $' + str(amp) +' to the accounts for successful transaction.'
                print 'trade denied'

            user1 = model.getUserBalances(username)
            self.render('dashboard.html', userdetails=user1, errormessage=errorMessage, successmessage=successMessage)

#This method starts the server at 8888 port
def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
