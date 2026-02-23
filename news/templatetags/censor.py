from django import template

register = template.Library()

BAD_WORDS = ['хуй', 'пизда', 'сука', 'блядь', 'нахуй']

@register.filter()
def censor(text):
    if not isinstance(text, str):
        return text
    
    for word in BAD_WORDS:
        replacement = word[0] + '*' * (len(word) - 1)
        text = text.replace(word, replacement)
        text = text.replace(word.capitalize(), replacement.capitalize())
    return text