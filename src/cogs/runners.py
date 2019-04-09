import config as c
import re
import os
import shutil
import subprocess

from cogs.utils import checks

import discord
from discord.ext import commands


class Runners():
    """ Runners for different languages.
    """
    def python(message, code: str):
        homedir = f'{c.srcDir}/runners/{message.author.id}'
        if os.path.isdir(homedir):
            return 'File already exists.'
        else:
            os.mkdir(homedir)

        with open(f'{homedir}/code.py', 'w+') as codeFile:
            codeFile.write(code)

        dockerfile = f"""FROM python
COPY . /bot
WORKDIR /bot
RUN python --version
CMD ["python", "-u", "/bot/code.py"]"""
        with open(f'{homedir}/dockerfile', 'w+') as dockerfileFile:
            dockerfileFile.write(dockerfile)

        # run container and capture output
        with open(f'{homedir}/stdout.py', 'a') as stdout, open(f'{homedir}/stderr.py', 'a') as stderr:
            subprocess.call(f'cd {homedir} && docker build -t {message.author.id}rbot {homedir} && docker run --rm {message.author.id}rbot', shell=True, stdout=stdout, stderr=stderr)
        with open(f'{homedir}/stdout.py', 'r') as stdout:
            rstdout = stdout.readlines()
        with open(f'{homedir}/stderr.py', 'r') as stderr:
            rstderr = stderr.readlines()

        result = f"""``stderr:``
```py
{'None' if ''.join(rstderr) == '' else ''.join(rstderr)}```
``stdout:``
```py
{'None' if ''.join(rstdout).split("rbot:latest",1)[1] == '' else
''.join(rstdout).split("rbot:latest",1)[1]}```"""

        shutil.rmtree(homedir)
        return result



    def old_python(message, code: str):
        # make folder to hold temporary files

        homedir = f'{c.srcDir}/runners/{message.author.id}'
        if os.path.isdir(homedir):
            return 'File already exists.'
        else:
            os.mkdir(homedir)

        # write code to a temporary file
        # pattern = r"(input\s*\(\"*\'*.*\'*\"*)"
        # regArray = re.findall(pattern, code)
        # def userCheck(m):
            # return m.author.id == ctx.message.author.id
        # for item in regArray:
            # try:
                # await ctx.send('Input:')
                # userInput = await self.bot.wait_for('message', check=userCheck, timeout=10)
            # except Exception:
                # shutil.rmtree(homedir)
                # return


        with open(f'{homedir}/code.py', 'w+') as codeFile:
            codeFile.write(code)

        # make dockerfile
        #dockerfile = ['FROM python', 'COPY']
        #'\n'.join(dockerfile)
        dockerfile = f"""FROM python
COPY . /bot
WORKDIR /bot
RUN python --version
CMD ["python", "-u", "/bot/code.py"]"""
        with open(f'{homedir}/dockerfile', 'w+') as dockerfileFile:
            dockerfileFile.write(dockerfile)

        # run container and capture output
        with open(f'{homedir}/output.py', 'a') as outputFile:
            subprocess.call(f'cd {homedir} && docker build -t {message.author.id}rbot {homedir} && docker run --rm {message.author.id}rbot', shell=True, stdout=outputFile, stderr=outputFile)
        with open(f'{homedir}/output.py', 'r') as outputFile:
            result = outputFile.readlines()

        shutil.rmtree(homedir)
        return result

class RunnerCog(commands.Cog, name="Runner Commands"):
    """ RunnerCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='run')
    @checks.is_dev()
    async def _runner(self, ctx, customLimit: int = 2, *customInput):
        """ Run the most recent code block written by you.
            Custom limit may not exceed 50 messages.
        """
        # if int(customLimit) >= 100000000000000000:
        #    message = await ctx.get_message(customLimit)
        #^ to make this work, the async for message part could be turned into two async functions and return message object and language
        languages = ['python', 'py']
        customLimit = 51 if customLimit > 50 else customLimit + 1
        counter = 0
        async for message in ctx.channel.history(limit=int(customLimit)):
            message.content = message.content[message.content.find('```'):]
            message.content = message.content[:int(6+message.content[3:].find('```'))]
            # check if message is a codeblock
            if message.content.startswith('```') and message.content.endswith('```'):
                lang = str(re.findall(r'^\w+[^\n]', message.content[3:-3])).strip('[\',]').lower()
                if any(lin in lang.lower() for lin in languages):

                    if lang == 'python' or lang == 'py':
                        code = message.content[3+len(lang):-3]
                        if len(customInput) != code.count('input('):
                            await ctx.send('Uneven amount of inputs, aborting.')
                            return
                        #output = ''.join(Runners.python(ctx.message, code))
                        #await ctx.send('```py\n{}```'.format(output.split("rbot:latest",1)[1]))
                        output = Runners.python(ctx.message, code)
                        await ctx.send(output)
                    return

                else:
                    await ctx.send('```No supported languages detected in codeblock header.```')
                    return
            counter += 1

def setup(bot):
    bot.add_cog(RunnerCog(bot))
