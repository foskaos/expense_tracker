from menu_system import Form, ChoiceField, PromptField
class Schedule:
#    fields = [
#        ChoiceField('Schedule Choice','type',{'a':lambda :print('anchor'), 'b':lambda :print('banchor')})
#    ]
    @classmethod
    def from_ui(cls, context):
        print(f'calling schedule ui with {context}')
        choices = {sub.label[0]:sub.from_ui for sub in cls.__subclasses__()}
        print(f'schedule choices: {choices}')
        form = Form([ChoiceField('schedule','schedule builder',choices)])
        context = form.run_form(context)
        print(f"main schedule out{context}")
        return context['schedule']

class ASched(Schedule):
    label = ('a','anchor')
    fields = [
        PromptField('anchor',label='Anchor Day'),
        PromptField('title', label='Title')
    ]

    def __init__(self,anchor, title):
        self.anchor = anchor
        self.title = title
    @classmethod
    def from_ui(cls, context=None):
        print('called a sched from ui')
        context = context or {}
        form = Form(cls.fields)
        context = form.run_form(context)
        print(f"a sched from ui out {context}")
        return cls(**context)

    def __repr__(self):
        return f"Anchored Schedule {self.title} on {self.anchor}"
