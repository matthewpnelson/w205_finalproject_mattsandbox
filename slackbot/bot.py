import os
import time
from slackclient import SlackClient


# starterbot's ID as an environment variable
# BOT_ID = os.environ.get("BOT_ID")
BOT_ID = os.getenv("BOT_ID","")
# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient(os.getenv('SLACK_BOT_TOKEN', ""))
#counter as global variable
command_count=0

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    if command==1:
        response = "What zip code do you want to live in?"
    elif command==2:
        response = "What is your min rent price? ###"
    elif command==3:
        response = "What is your max rent price? ###"
    elif command==3:
        response = "Do you care to have a lot of businesses nearby? 1 if you don't care about this, 10 if you really do."
    elif command==4:
        response = "Do you care if there have been a lot of evictions nearby? 1 if you don't care about this, 10 if you really do."
    elif command==5:
        response = "Do you care if there are a lot of schools nearby? 1 if you don't care about this, 10 if you really do."
    elif command==6:
        response = "Is bike parking important to you? yes or no."
    elif command==7:
        response = "Proximity you want to be from bike share? short, medium or long."
    elif command==8:
        response = "What level of offstreet parking to you prefer? low, medium or high (density)."
    elif command==9:
        response = "What level of crime incidents in the area are you comfortable with? low, medium or high"
    elif command==10:
        response = "What tree density do you prefer? low, medium or high"
    else:
        response = "Not sure what you mean."

    slack_client.api_call("chat.postMessage", channel=channel,
                    text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                file=open('starterbot.txt','a')
                file.write(output['text'].split(AT_BOT)[1].strip().lower()+"\n")
                file.close()
                global command_count
                command_count+=1
                return command_count, \
                          output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
