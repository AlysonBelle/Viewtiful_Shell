


from flask_wtf import Form
from wtforms import TextField, SubmitField
from flask import Flask, render_template, url_for, request
from shell import  init_shell, parse
import shell

app = Flask(__name__)
app.secret_key = 'ASDFBOI'
init_sh = False
ShellCommand = None



class ShellPrompt(Form):
    prompt = TextField("$>")
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def shell():
    global my_environ
    global init_sh
    global ShellCommand

    prompt = ShellPrompt()
    output = ''

    if init_sh == False:
        my_environ, ShellCommand = init_shell()
        init_sh = True
    print('here')
    if prompt.validate_on_submit():
        print('not here')
        command = prompt.prompt.data
        output, my_environ = parse(command, ShellCommand, my_environ)
        print('output is ', output)
    return render_template('shell.html', output=output, prompt=prompt)



if __name__ == '__main__':
   app.run()





