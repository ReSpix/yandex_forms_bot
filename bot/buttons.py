messages_text = ['Взято в работу', 'Позвонили клиенту', 'Клиент принял работу', 'Клиент отказался']

def get_new_text(current_text, add_text):
    txt = current_text.split('\n')
    
    if txt[-1] in messages_text:
        txt[-1] = add_text
    else:
        txt.append('')
        txt.append(add_text)
        
    return '\n'.join(txt)