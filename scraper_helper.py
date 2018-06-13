# associate reactions to the messages they react to
# return the new list without the reactions
def link_reactions_for_imessages(allMessages):
    ret = []
    for message in allMessages:
        if not message['is_reaction']:
            ret.append(message)
            continue
        
        # find the associated message index
        # the message that this reaction is reacting to
        for index, content in enumerate(allMessages):
            if 'guid' in content and content['guid'] in message['associated_message_guid']:
                idx = index

        if idx is None:
            continue
        
        reacted = allMessages[idx]
        reacted['reactions'].append(message)
    return ret

# parse for messenger message attachments
def hook_messenger_attachment(message, raw):
    if 'blob_attachments' in raw:
        blobs = raw['blob_attachments']
        if len(blobs) > 0:
            attachment = blobs[0]
            if 'large_preview' in attachment:
                message['attachment'] = attachment['large_preview']['uri']
            
            if 'animated_image' in attachment:
                message['attachment'] = attachment['animated_image']['uri']
