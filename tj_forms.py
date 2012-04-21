from wtforms import Form, BooleanField, TextField, PasswordField, DateField, validators

class tj_tadd_basic_form(Form):
  title = TextField('title', [validators.length(min=1,max=30)])
  date  = DateField('date',[validators.required()],format='%d.%m.%Y')
  route = TextField('route',[validators.optional(), validators.length(max=200)],default='No route')
  
