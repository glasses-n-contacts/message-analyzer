

# associate reactions to the messages they react to
# return the new list without the reactions
def link_reactions_for_imessages(all_messages):
    ret = []
    idxs = None
    for message in all_messages:
        if not message['is_reaction']:
            ret.append(message)
            continue
        
        # find the associated message index
        # the message that this reaction is reacting to
        for index, content in enumerate(all_messages):
            if 'guid' in content and content['guid'] in message['associated_message_guid']:
                idx = index

        if idx is None:
            continue
        
        reacted = all_messages[idx]
        reacted['reactions'].append(message)
    return ret


# parse for messenger message attachments
def hook_messenger_attachment(message, raw):
    attachments = []

    if not message['message'] and raw['extensible_attachment']:
        story_attachment = raw['extensible_attachment']['story_attachment']
        message['is_system_message'] = 1
        if story_attachment['media']:
            attachments.append({
                'url': story_attachment['media']['image']['uri']
            })
        message['message'] = story_attachment['title_with_entities']['text']

    if 'blob_attachments' in raw:
        blobs = raw['blob_attachments']
        if len(blobs) > 0:
            for blob in blobs:
                if 'large_preview' in blob:
                    attachments.append({
                        'url': blob['large_preview']['uri']
                    })
                
                if 'animated_image' in blob:
                    attachments.append({
                        'url': blob['animated_image']['uri']
                    })
                
                if 'url' in blob:
                    attachments.append({
                        'filename': blob['filename'],
                        'url': blob['url']
                    })
    
    sticker = raw['sticker']
    if sticker:
        attachments.append({
            'url': sticker['url']
        })
    
    message['attachments'] = attachments
