


from flask_wtf import Form
from wtform import TextField, SubmitField
from flask import Flask, render_template, url_for, request
import shell

app = Flask(__name__)
init_shell = False
ShellCommand = None


class ShellPrompt(Form):
    prompt = TextField("$>"))
    submit = SubmitField("Submit")


@app.route('/')
def shell():
    global my_environ
    global init_shell

    prompt = ShellPrompt()
    output = ''

    if init_shell == False:
        my_environ, ShellCommand = init_shell()
        init_shell = True
    if prompt.validate_on_submit():
        command = prompt.prompt.data
    output, my_environ = shell.parse(command, ShellCommand, my_environ)
    return render_template('shell.html', output=output, prompt=prompt)



if __name__ == '__main__':
   app.run()





