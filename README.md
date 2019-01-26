# autoelab

Automagically solve all questions in your elab.

## How do I use it?

- Download the latest executable from the [Release](https://github.com/autoelab/autoelab/releases) tab of this repo.
- Running it for the first time will create a `config.json` file.
- Set it up as specified below and run the executable again.

## Configuration

The user info is stored in config.json. You can edit it using any text editor. Just don't use Notepad please, it's blasphemy. Use [Notepad++](https://notepad-plus-plus.org/) at the very least or a code editor like [CodeWriter](https://www.microsoft.com/en-us/p/code-writer/9wzdncrfhzdt), [Atom](https://atom.io/) or [Visual Studio Code](https://code.visualstudio.com/).

### Expected values in config.json

- username : `your register number`
- password : `your password` 
- department : `cse` or `it`
- campuscode : `ktr` or `rmp` or `vdp`
- skill : `java` or `daa`
- level : `1` or `2` or `3`
- start : `0` to `99` - question number to start solving from
- end : `0` to `99` - question number to solve up to
- delay : `0` for no delay; or any integer `n` for n minutes of delay
- generatereports : `true` or `false`

You can leave any of the fields blank, as long as you don't remove the double quotes.
Any information with a blank field will be asked for during runtime.

**Note:** Question numbering starts from 0 and level numbering starts from 1.

If you're not familiar with json files, make sure every entry is enclosed within double quotes and there's a comma at the end of each line, except the last one. The last line has neither comma nor quotes. This is what a [final config file](https://textuploader.com/1andb) should look like.

**Pro Tip:** It's a good idea to keep the `start` and `end` values blank so you don't have to edit the config every time you use it. You can also leave the `password` field blank if you're paranoid about security.

### Additional features:

#### Random delays
You can optionally add a random delay between solving questions so you don't suddenly shoot up in ranks overnight. The time specified here is in minutes. If it's set to `0` there won't be any delay. Any other number would delay the solution of the next question by `<that number + any random number between 1 to 10>` minutes.

#### Generate reports
If this is set to `true`, the app will also generate reports and save them in a new `Reports` folder.
Yes, you don't need to use that half-assesd chrome plugin anymore.

## Some info, for normies

```
I am not responsible for you failing the exams because you kanged all of the answers.
YOU are choosing to use the script. If you point a finger at me, I will laugh at you.
```

*This script only solves the questions that aren't evaluated to 100%. If you already solved a question correctly on your own, it will not overwrite your solution.*

It's fairly new so there may be bugs. At the moment, only a few subjects like `java` and `daa` are verified to be working but it can potentially support a lot more. Is your subject not supported yet? Open a request for it in the [Issues](https://github.com/autoelab/autoelab/issues) section and I'll see what I can do.

## More info, for nerds

This script is written in python and compiled into an executable with all it's dependencies so any prior setup or installation is not required.

It accesses the database online, directly from this repository so an offline copy of data folder is not necessary, which reduces the total file size by 90%.

This executable can be compiled by cloning/downloading this repository and running this command:
```bash
pyinstaller --onefile -n autoelab --icon icon.ico autoelab.py
```

The executable also takes input from command line so you can use it for further scripting or in your own application. All nine parameters are required and genratereports is set to false by default. The syntax is:
```bash
autoelab.exe [username] [password] [department] [campuscode] [skill] [level] [start] [end] [delay]
```

## FAQ

#### I'm unable to login. Why?
Change your password to something that doesn't have any special characters. 
I'm pretty sure there's a workaround to fix this but I'm lazy.

#### Still not working. What do I do?
Read and follow the instructions properly. Properly.
If there are problems, report them in the [Issues](https://github.com/autoelab/autoelab/issues) section.

#### Why did you make this?
I just told you, I'm lazy. 
Also, because I could and because nobody else had done it despite it being so easy to implement. Just to show that it can be done. Barely took me a day to get it working and a whole week to make a user friendly somewhat final release.

#### Did you 'hack' the database?
No. 
The data extracted from it is already floating around on GitHub. I just modified some parts of it to add support for more subjects.

#### How do I contact you?
You don't.

#### How does this work?
It's AI.

#### Are you kidding me?
Yes.
