from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   bad_words = ('цензура', 'нехорошее', 'фылдвар', 'текст')

   if not isinstance(value, str):
      raise TypeError('Фильтр можно применять только для текста')

   for b_word in bad_words:
      for word in value.split():
         if word.lower().count(b_word):
            value = value.replace(word, f"{word[0]}{'*' * (len(b_word) - 1)}{word[-1]}")

   return value