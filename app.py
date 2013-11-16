"""
app

This is the application's main module.
"""

import web
from web import form
from twilio.rest import TwilioRestClient
import twilio.twiml
import twiliocreds
import web              # A simple-looking Python HTTP framework I just found

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',              'index',
    '/createdeath',   'createdeath',
    '/deathmatch',    'deathmatch',
    '/join',          'join',
    '/activation',    'activation',
    '/seeMsg',        'seeMsg',
    '/echoChamber',   'echoChamber',
)

# Tell web.py where to look to find page templates
render = web.template.render('templates/');

# Classes that handle URLs

# Form that handles the buttons on the index page
landing = form.Form(
    form.Button('Create a Deathmatch', class_='btn btn-lg btn-primary'),
    form.Button('Join a Deathmatch', class_='btn btn-lg btn-primary'),
)

class index:
    def GET(self):
        landingForm = landing()
        return render.index(landingForm)

    def POST(self):
        landingForm = landing()
        if landingForm.validates():
            # Handle the landing form here
            return render.index(landingForm)

class createdeath:
    def GET(self):
        return render.createdeath()

class death:
    def GET(self):
        return render.death()

class join:
    def GET(self):
        return render.join()

class activation:
    def GET(self):
        return render.activation()

class twilTest:
    def GET(self):
        client = TwilioRestClient(twiliocreds.account_sid,
                twiliocreds.auth_token)
        message = client.messages.create(to=twiliocreds.sams_phone,
                from_=twiliocreds.our_phone,
                body="Test")
        return render.twilTest(str(message.sid))

message = form.Form(
    form.Textbox('message'),
    form.Button('Send'),
)

class seeMsg:
    def GET(self):
        msgForm = message()
        return render.seeMsg(msgForm, None)

    def POST(self):
        msgForm = message()
        if not msgForm.validates():
            return render.seeMsg(msgForm, None)
        else:
            user_data = web.input()
            client = TwilioRestClient(twiliocreds.account_sid,
                    twiliocreds.auth_token)
            sms = client.messages.create(to=twiliocreds.sams_phone,
                    from_=twiliocreds.our_phone,
                    body=user_data.message)
            return render.seeMsg(msgForm, "Sent " + user_data.message + " " +
                    str(sms.sid))

class target:
    def GET(self):
        return render.target()

class echoChamber:
    def GET(self):
        resp = twilio.twiml.Response()
        resp.message("This is a reply")
        return str(resp)

    def POST(self):
        user_data = web.input()
        resp = twilio.twiml.Response()
        try:
            resp.message(user_data.Body)
        except AttributeError:
            resp.message("You said nothing.")
        web.debug("Sayin' this:" + str(resp))
        web.header('Content-Type', 'text/xml')
        return str(resp)

# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()

