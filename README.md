# Facebook Analytics
A collection of Python-scripts for analyzing the data of a Facebook Dump. 

## Convert your messages to JSON format
For you to be able to use the tools, your messages must be converted/parsed from the original HTML format to JSON. Run the following command to convert the `messages.htm`-file from your dump to JSON:

```
python parse_fb_conversations.py <path_to_messages.htm>
```

This will create a `fb_messages.json` file to be used by the tools

## Messaging history plot tool
Plot how frequent you have texted your friends to see how your friendships have varied over time.

```
python closest_friends.py <path_to_fb_messages.json>
```
