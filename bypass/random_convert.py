# Fix Soon

import random
import mojimoji
import jaconv

def random_convert(input_str):
    result = ''
    exclude_list = ['@everyone', '@here']
    
    i = 0
    while i < len(input_str):
        found = False
        for exclusion in exclude_list:
            if input_str[i:i+len(exclusion)] == exclusion:
                result += exclusion
                i += len(exclusion)
                found = True
                break
        
        if not found:
            char = input_str[i]
            choice = random.choices(['fullwidth', 'halfwidth', 'kana', 'keep'])[0]
            
            if choice == 'fullwidth':
                result += mojimoji.han_to_zen(char)
            elif choice == 'halfwidth':
                result += mojimoji.zen_to_han(char)
            elif choice == 'kana':
                result += jaconv.z2h(jaconv.hira2hkata(char), digit=True, ascii=True)
            else:
                result += char
            i += 1

    return result
