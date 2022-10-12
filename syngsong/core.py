import logging
import os
import string

import lyricsgenius


def basic_password_transform(password_set: set, min_len: int, max_len: int) -> set:
    """Basic password transformations. Add all lower, all upper, and title case

    Args:
        password_set (set): passwords to work on
        min_len (int): minimum password length
        max_len (int): maximum password length

    Returns:
        set: transformed passwords
    """
    transformed_passwords = set()
    for line in password_set:
        if min_len <= len(line) <= max_len:
            transformed_passwords.add(line)
            transformed_passwords.add(line.lower())
            transformed_passwords.add(line.upper())
            transformed_passwords.add(line.title())
            if " " in line:
                transformed_passwords.add(line.title().replace(" ", "")) #  This lets us get title cased passwords without spaces 
    return transformed_passwords

def generate_passwords(artist: str, genius_api_key:str, masking:str = "", min_len:int = 8, max_len:int = 32, top_songs=0) -> bool:
    """The core of Syngsong. This is where the passwords get created

    Args:
        Note: All of these args can be supplied by the user at runtime, but I have provided some sensible defaults so they don't have to.
        artist (str): The artist for which we want to get lyrics
        masking (str, optional): Optional password mask, similar to what Hashcat does. Defaults to "", which is the same as no mask.
        genius_api_key (str): genius.com Client access token
        min_len (int, optional): Minimum password length. Defaults to 8.
        max_len (int, optional): Maximum password length. Defaults to 32.

    Returns:
        bool: Return True right now, might do something else later, but this value shouldn't be used anywhere else.
    """
    genius = lyricsgenius.Genius(genius_api_key)
    if top_songs == 0:
        genius_artist = genius.search_artist(artist)
    else:
        genius_artist = genius.search_artist(artist, max_songs=top_songs)
    logging.info("Connection to Genius was successful, generating passwords.")
    for song in genius_artist.songs:
        logging.debug(f"Working on song {song}.")
        # Using a set because I don't want duplicates in the final password set
        passwords = set()
        raw_lyrics = song.lyrics.splitlines()
        raw_lyrics.append(raw_lyrics[0].split("Lyrics")[-1])
        # Setting up some basic sets to build on later
        base_password_lyrics = set([_.translate(str.maketrans('', '', string.punctuation)).strip() for _ in raw_lyrics if not _ == ""])
        base_password_no_space = set([_.replace(" ", "") for _ in base_password_lyrics.copy()])
        base_password_lyrics.add(song.title)
        base_password_no_space.add(song.title.replace(" ", ""))
        # Time to do some basic transformation on the base sets of passwords
        passwords.update(basic_password_transform(base_password_lyrics, min_len, max_len))
        passwords.update(basic_password_transform(base_password_no_space, min_len, max_len))
        if len(masking) > 0:
            logging.info("Found a mask, working on that now")
            raw_mask = masking.lstrip("?").split("?")
            passwords.update(handle_mask(passwords, raw_mask))
        with open(f"./{artist}_tmp.txt", "a") as password_out_file:
            for password in passwords:
                if min_len <= len(password) <= max_len: #  One last check to make sure we constrain the size of our passwords
                    password_out_file.write(password + "\n")
    final_file = open(f"./{artist}_tmp.txt", "r")
    final_output = set(final_file.readlines())
    final_file.close()
    os.remove(f"./{artist}_tmp.txt")
    final_linecount = len(final_output)
    with open(f"./{artist}_out.txt", "w") as password_out_file: #  I am doing this to dedupe the final file
        for entry in final_output:
                password_out_file.write(entry)
    logging.info(f"Generated {final_linecount} passwords.")
    return True



def handle_mask(working_password_set: set, mask: list) -> set:
    """Function to append characters to each password based on a user supplied mask.

    This is a recursive function, it will recurse until there is no more mask characters to process.

    Args:
        working_password_set (set): Password set to 
        mask (list): I chop up the mask into a list in the calling function to make the mask easier to handle

    Returns:
        set: Passwords with masks added
    """
    logging.debug(f"Current Mask {mask}")
    new_password_set = set()
    mask_character = mask[0]
    if mask_character.lower() == "l":
        logging.debug("Adding lower case letters")
        for password in working_password_set:
            for letter in string.ascii_lowercase:
                new_password_set.add(password + letter)
    if mask_character.lower() == "u":
        logging.debug("Adding upper case letters")
        for password in working_password_set:
            for letter in string.ascii_uppercase:
                new_password_set.add(password + letter)
    if mask_character.lower() == "d":
        logging.debug("Adding digits")
        for password in working_password_set:
            for digit in string.digits:
                new_password_set.add(password + digit)
    if mask_character.lower() == "s":
        logging.debug("Adding symbols")
        for password in working_password_set:
            for symbol in string.punctuation:
                new_password_set.add(password + symbol)
    if mask_character.lower() == "a":
        logging.debug("Adding lower case letters, upper case letters, digits, and symbols")
        for password in working_password_set:
            for letter in string.ascii_lowercase:
                new_password_set.add(password + letter)
        for password in working_password_set:
            for letter in string.ascii_uppercase:
                new_password_set.add(password + letter)
        for password in working_password_set:
            for symbol in string.punctuation:
                new_password_set.add(password + symbol)
        for password in working_password_set:
            for digit in string.digits:
                new_password_set.add(password + digit)
    mask = mask[1:] #  Chop off the front mask character and proceed
    if len(mask) > 0: #  If there are more masks characters, recurse!
        logging.debug("Moving on to the next mask character")
        set([new_password_set.add(_) for _ in handle_mask(new_password_set, mask)])
    # Return passwords when the mask is empty
    return new_password_set
