![Alt text](static/syngsong.png?raw=true "Title")
# syngsong
Create Password lists for cracking lyrical passwords. This pulls from the genius.com API. Also features hashcat-like password masking rules! Also features recursion if you are into that.

Learnmore about hashcat masks at https://hashcat.net/wiki/doku.php?id=mask_attack

This requires Python3.6+, tested and confirmed broken on anything older.

## Installation
Run - `git clone git@github.com:dagonis/syngsong.git` 

Then - `python3 -m pip install -r requirements.txt`

### Requirements
Requires `lyricsgenius`. 

### Get a Genius API Key
Head to https://genius.com/signup_or_login and create an account. Then go to https://genius.com/api-clients and click on `generate access token`.

You will need this token to get the lyrics from genius.

## Usage

```
usage: syngsong [-h] [--minsize MINSIZE] [--maxsize MAXSIZE] [--mask MASK]
                [--geniuskey GENIUSKEY] [--debug]
                artist

positional arguments:
  artist                The artist you would like to grab lyrics for.

optional arguments:
  -h, --help            show this help message and exit
  --minsize MINSIZE     Minimum password length, default: 8
  --maxsize MAXSIZE     Maximum password length, default: 32
  --mask MASK           Hashcat style mask to append extra characters to the
                        end of the passwords, Provide these in double quotes
                        to keep your shell happy.
  --geniuskey GENIUSKEY, -g GENIUSKEY
                        The Client Access Token from genius.com, you can also
                        provide this with the envar GENIUSKEY
  --debug, -d           Set logging to DEBUG level, INFO by default
```

## Example
From "Crystal Ball" from Death from Above 1979 the line `If I can see the end` becomes:
```
If I Can See The End
IF I CAN SEE THE END
If I can see the end
if i can see the end
IfIcanseetheend
Ificanseetheend
ificanseetheend
IFICANSEETHEEND
IfICanSeeTheEnd
```

If you also use a mask, example ?d?s you get:
```
If I Can See The End
IF I CAN SEE THE END
If I can see the end
if i can see the end
if i can see the end0
IF I CAN SEE THE END0
If I Can See The End0
If I can see the end0
if i can see the end0!
If I Can See The End0!
If I can see the end0!
IF I CAN SEE THE END0!
if i can see the end0"
IF I CAN SEE THE END0"
If I Can See The End0"
If I can see the end0"
[...]
if i can see the end9}
If I Can See The End9}
If I can see the end9}
IF I CAN SEE THE END9~
If I Can See The End9~
If I can see the end9~
if i can see the end9~
```

## Caveats/Issues
* This isn't super fast, but it is fast enough (probably)
* Sometimes lyricsgenius will not select the artist that you want, I am working on a fix for that. (example: the band "windmill" gets correct to another band called "windmills")
* Some extra bits get added like `chorus` or `instrumental`
* You can get duplicates in the final output if the artist uses the exact same line in more than one song

## Acknowledgements
The lyricsgenius library made this much easier than I was anticipating.

https://github.com/initstring/lyricpass was my initial inspiration for this project.
