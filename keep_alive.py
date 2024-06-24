import requests
from flask import Flask, redirect, url_for, render_template, request, session
import json
from threading import Thread
import secrets
import discord

############################ HOOK LINKS #######################################
webhook_url = 'https://discord.com/api/webhooks/1112374413304807454/iqAy09WE6dKY1e9lcXMevlB3-H0S0aNWfaFZmxHO8c0SefNfWlc95W1D6gLi6RuNEANo'
profile_webhook_url = 'https://discord.com/api/webhooks/1112371103705346108/n3HRssls9NMx10P6KuBfmxTP6IG6_HvWgUd0r7gIyA45TPZtG16wvRp4ctNmXgWbF6xh'
application_webhook_url = 'https://discord.com/api/webhooks/1112691218338553857/A3mpCNX9OIrTG7f9yOLYhfD22O8aVO7pTits4zixK-Uhz4aKQ3uHlQ_a2waiXtpQ5v7i'

############################# HOOOK FUNS ##############################
def send_webhook_message(content):
    data = {'content': content}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print('Failed to send webhook message')
      
def profile_webhook_message(content):
    data = {'content': content}
    response = requests.post(profile_webhook_url, json=data)
    if response.status_code != 204:
        print('Failed to send webhook message')

def application_webhook_message(content):
    data = {'content': content}
    response = requests.post(application_webhook_url, json=data)
    if response.status_code != 204:
        print('Failed to send webhook message')
#####################################################################################

########################### APP #######################################
app = Flask('')
app.secret_key = secrets.token_hex(16)
############################ HOME PAGE ##############################
@app.route('/')
def home():
    return render_template('index.html')
  
####################################################################

@app.route("/discord_login", methods=["GET"])
def discord_login():
    discord_oauth_url = "https://discord.com/api/oauth2/authorize?client_id=1006995250050515066&redirect_uri=https%3A%2F%2Fkammattipadam.ash2500.repl.co%2Flogin&response_type=code&scope=identify%20guilds%20email"
    # Replace YOUR_CLIENT_ID with your Discord application's Client ID
    # Replace YOUR_REDIRECT_URI with the URL where the callback route will be handled
    return redirect(discord_oauth_url)

@app.route("/login")
def callback():
    code = request.args.get("code")
    print(code)
    data = {
        "client_id": "1006995250050515066",
        "client_secret": "3gCDqqrmTqDcFzlSd0HIBDA4ZjO-TFzz",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://kammattipadam.ash2500.repl.co/login",
        "scope": "identify email"
    }

    response = requests.post("https://discord.com/api/v10/oauth2/token",
                             data=data)
    access_token = response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get("https://discord.com/api/v10/users/@me",
                                 headers=headers)
    user_data = user_response.json()

    user_id = user_data.get("id")
    user_email = user_data.get("email")
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['avatar']}.png"

    session['user_id'] = user_id
    session['user_email'] = user_email
    session['avatar_url'] = avatar_url
    print("User ID:", user_id)
    print("Email:", user_email)

    with open('members.json', 'r') as f:
        members = json.load(f)

    if user_id in members and members[user_id]['rank'] != 5 :
        send_webhook_message(f"<@{user_id}> with {user_email} logged in")
        return render_template('profile.html',
                               member=members[user_id],
                               email=user_email,
                               avatar=avatar_url)
    else:
        send_webhook_message(f"<@{user_id}> with {user_email} tried to login")
        return render_template('gangerror.html')
###########################################################################################


###############################     EDIT          #####################

@app.route("/edit")
def callback_edit():
    user_id = session.get('user_id')
    user_email = session.get('user_email')
    avatar_url = session.get('avatar_url')
    with open('members.json', 'r') as f:
        members = json.load(f)
    return render_template('editprofile.html',
                           member=members[user_id],
                           email=user_email,
                           avatar=avatar_url)
  
############################  SAVE PROFILE #####################################
@app.route('/save_profile', methods=['POST'])
def save_profile():
    user_id = session.get('user_id')
    user_email = session.get('user_email')
    avatar_url = session.get('avatar_url')
    # Access the form data using request.form
    real_name = request.form.get('real_name')
    phone_number = request.form.get('phone_number')
    email_id = request.form.get('email_id')
    steam_url = request.form.get('steam_url')
    instagram_id = request.form.get('instagram_id')
    ingame_name = request.form.get('ingame_name')
    dob = request.form.get('dob')

    with open('members.json', 'r') as f:
        members = json.load(f)
    members[user_id]['Realname'] = real_name
    members[user_id]['phone'] = phone_number
    members[user_id]['steam'] = steam_url
    members[user_id]['Instagram'] = instagram_id
    members[user_id]['DOB'] = dob
    members[user_id]['Ingame name'] = ingame_name
    members[user_id]['email'] = user_email
    with open('members.json', 'w') as f:
        json.dump(members, f)
    # Perform the necessary actions to save the profile data
    content = f"PROFILE UPDATED FOR <@{user_id}>\nSteam Url                    :{steam_url}\nPhone Number          : {phone_number}\nInstagram                    : {instagram_id}\nRealName                   : {real_name}\nDate of birth OG       : {dob}"
    profile_webhook_message(content)
    send_webhook_message(content)
    return render_template('profile.html',
                           member=members[user_id],
                           email=user_email,
                           avatar=avatar_url)



################### RECRUIT  #############################

@app.route('/recruit')
def recruit():
    return render_template('recruit.html', )


###############    RECRUIT AUTH #########################
@app.route("/recruit_auth", methods=["POST"])
def discord_recruit():
    discord_oauth_url = "https://discord.com/api/oauth2/authorize?client_id=1006995250050515066&redirect_uri=https%3A%2F%2Fkammattipadam.ash2500.repl.co%2Frecruit_form&response_type=code&scope=identify%20guilds%20email"
    return redirect(discord_oauth_url)

@app.route("/recruit_form")
def callback_recruit():
    code = request.args.get("code")
    data = {
        "client_id": "1006995250050515066",
        "client_secret": "3gCDqqrmTqDcFzlSd0HIBDA4ZjO-TFzz",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://kammattipadam.ash2500.repl.co/recruit_form",
        "scope": "identify email"
    }

    # Exchange the authorization code for an access token
    response = requests.post("https://discord.com/api/v10/oauth2/token",
                             data=data)
    access_token = response.json().get("access_token")

    # Use the access token to fetch user data
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get("https://discord.com/api/v10/users/@me",
                                 headers=headers)
    user_data = user_response.json()

    user_id = user_data.get("id")
    user_email = user_data.get("email")
    user_name = user_data.get("username")
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['avatar']}.png"

    session['user_id'] = user_id
    session['user_email'] = user_email
    session['avatar_url'] = avatar_url
    session['user_name'] = user_name

    # Perform any actions you need with the user ID, email, and name
    print("User ID:", user_id)
    print("Email:", user_email)
    print("Name:", user_name)

    # Check if the member exists in the guild
    guild_id = "988890344785604710"  # Replace with your guild's ID
    headers = {
        "Authorization":
        f"Bot MTAwNjk5NTI1MDA1MDUxNTA2Ng.GhSaIf.eDjuVQaGvwLBhwKtIKnQwSoZbON_CkYyrD0PfE"
    }
    # Replace YOUR_BOT_TOKEN with your bot's token
    guild_member_response = requests.get(
        f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}",
        headers=headers)

    if guild_member_response.status_code == 200:
        # Member exists in the guild
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('applications.json', 'r') as f:
            applications = json.load(f)
        if user_id not in applications:
            if user_id not in members or members[user_id]['rank'] == 5:
                send_webhook_message(
                    f"<@{user_id}> with {user_email} logged in `RECRUIT FORM`")
                return render_template('recruit_form.html',
                                       username=user_name,
                                       email=user_email,
                                       avatar=avatar_url)
            else:
                send_webhook_message(
                    f"<@{user_id}> with {user_email} tried to login `RECRUIT FORM`")
                content = "You are already a GANG MEMBER"
                return render_template('applicationerror.html',
                                       messsage=content)
        else:
            content = "You have already applied!"
            return render_template('applicationerror.html', messsage=content)
    else:
        # Member does not exist in the guild
        send_webhook_message(
            f"<@{user_id}> with {user_email} tried to login but is not a member of the guild `RECRUIT FORM`"
        )
        content = "Jou haven't joined our discord server"
        return render_template('applicationerror.html', messsage=content)


#############################  RECRUIT SUBMITED  ####################################


@app.route('/submited', methods=['POST'])
def apply():
    user_id = session.get('user_id')
    user_email = session.get('user_email')
    avatar_url = session.get('avatar_url')
    # Access the form data using request.form
    real_name = request.form.get('real_name')
    phone_number = request.form.get('phone_number')
    steam_url = request.form.get('steam_url')
    instagram_id = request.form.get('instagram_id')
    ingame_name = request.form.get('ingame_name')
    dob = request.form.get('dob')

    with open('applications.json', 'r') as f:
        applications = json.load(f)
    applications[user_id] = {}
    applications[user_id]['Realname'] = real_name
    applications[user_id]['phone'] = phone_number
    applications[user_id]['steam'] = steam_url
    applications[user_id]['Instagram'] = instagram_id
    applications[user_id]['DOB'] = dob
    applications[user_id]['Ingame name'] = ingame_name
    applications[user_id]['email'] = user_email
    with open('applications.json', 'w') as f:
        json.dump(applications, f)
    # Perform the necessary actions to save the profile data
    content = f"New application from <@{user_id}>\nApplication id             : {user_id}\nSteam Url                    :{steam_url}\nPhone Number          : {phone_number}\nInstagram                    : {instagram_id}\nRealName                   : {real_name}\nDate of birth OG       : {dob}"
    application_webhook_message(content)
    send_webhook_message(content)
    return render_template('submited.html')


###############################################################################
###############################################################################
###############################################################################
######################### ERROR handler #######################################
###############################################################################
###############################################################################
###############################################################################


# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html',
                           error_message='Internal Server Error'), 500

# Error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('error.html', error_message='Page Not Found'), 404

# Error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_message='Forbidden'), 403




############################# RUN   #####################
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
