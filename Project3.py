import random
import os.path

# A global constant defining the alphabet.
LETTERS = "abcdefghijklmnopqrstuvwxyz"
PROMPT = "Enter a command (getKey, changeKey, encryptFile, decryptFile, quit): "
GOODBYE_MESSAGE = "Thanks for visiting! \n"
CHANGE_KEY_MESSAGE = (
    "  Enter a valid cipher key, 'random' for a random key, or 'quit' to quit: "
)


def isLegalKey(key):
    # A key is legal if it has length 26 and contains all letters.
    # from LETTERS.
    key = key.lower()
    return len(key) == 26 and all([ch in key for ch in LETTERS])


def makeRandomKey():
    # A legal random key is a permutation of LETTERS.
    lst = list(LETTERS)  # Turn string into list of letters
    random.shuffle(lst)  # Shuffle the list randomly
    return "".join(lst)  # Assemble them back into a string


def makeConversionDictionary(key1, key2):
    dict = {}
    key1 = key1.lower()
    key2 = key2.lower()

    # maps each key (letters used for plaintext) to a value (letters used for ciphertext)
    # assumes that keys are legal and placed correspondingly
    for c in range(26):
        dict[key1[c]] = key2[c]

    return dict


def generateName(inFile, ext):

    # Renames each file so that program can run on WindowsOS

    if inFile.endswith(".txt"):
        outfileName = inFile[:-4] + ext + ".txt"
    else:
        outfileName = inFile + ext

    return outfileName


class SubstitutionCipher:
    def __init__(self, key=makeRandomKey()):
        """Create an instance of the cipher with stored key, which
        defaults to a randomly generated key."""
        self.__key = key.lower()

    def getKey(self):
        """Getter for the stored key."""
        return self.__key

    def setKey(self, newKey):
        """Setter for the stored key.  Check that it's a legal
        key."""
        if isLegalKey(newKey):
            self.__key = newKey.lower()
            return

    def encryptFile(self, inFile, outFile):
        """Encrypt the contents of inFile using the stored key
        and write the results into outFile.  Assume inFile exists.
        """
        infile = open(inFile, "r")
        line = infile.readline()
        outfile = open(outFile, "w")
        dict = makeConversionDictionary(LETTERS, self.getKey())

        # Loop through the lines in the plaintext
        while line:

            # Loop through each character in the plaintext
            for c in line:

                # Check if the character is in the alphabet
                if c.isalpha():

                    # Loop through the conversion dictionary
                    for key in dict:

                        # If the key matches the character, write the converted character
                        # to the ciphertext
                        if key == c.lower():
                            if c.isupper():
                                outfile.write(dict[key].upper())
                            else:
                                outfile.write(dict[key])

                # If character is not in the alphabet, write it to ciphertext
                # without changing
                else:
                    outfile.write(c)

            # Set line to the next line in the plaintext
            line = infile.readline()

        infile.close()
        outfile.close()

        return outFile

    def decryptFile(self, inFile, outFile):
        """Decrypt the contents of inFile using the stored key
        and write the results into outFile.  Assume inFile exists.
        """
        infile = open(inFile, "r")
        line = infile.readline()
        outfile = open(outFile, "w")
        dict = makeConversionDictionary(self.getKey(), LETTERS)

        # Loop through the lines in the plaintext
        while line:

            # Loop through each character in the plaintext
            for c in line:

                # Check if the character is in the alphabet
                if c.isalpha():

                    # Loop through the conversion dictionary
                    for key in dict:

                        # If the key matches the character, write the converted character
                        # to the "ciphertext," which will match the plaintext

                        if key == c.lower():
                            if c.isupper():
                                outfile.write(dict[key].upper())
                            else:
                                outfile.write(dict[key])

                # If character is not in the alphabet, write it to ciphertext
                # without changing
                else:
                    outfile.write(c)

            # Set line to the next line in the ciphertext
            # (the plaintext for this functions purposes)
            line = infile.readline()

        infile.close()
        outfile.close()

        return outFile


def main():
    """
    This implements the top level command loop.  It
    creates an instance of the SubstitutionCipher class and allows the user
    to invoke within a loop the following commands: getKey, changeKey,
    encryptFile, decryptFile, quit.
    """

    print()

    cipher = SubstitutionCipher()

    # While the user does not input quit to the main prompt, keep asking it
    while True:

        # Makes the input lowercase to facilitate robustness
        ipt = input(PROMPT).lower()
        if ipt == "quit":
            print(GOODBYE_MESSAGE)
            break

        # Returns the key if the user inputs any case variation of getKey
        elif ipt == "getkey":
            print("  Current cipher key:", cipher.getKey(), "\n")

        # Case where user inputs any case variation of changeKey
        elif ipt == "changekey":
            while True:

                # If user inputs "quit" to changeKey prompt, quit out of this inner loop
                change_ipt = input(CHANGE_KEY_MESSAGE).lower()
                if change_ipt == "quit":
                    print()
                    break

                # If the user inputs "random" to changeKey prompt, generate a random key,
                # replace the current key with the new key, display the new key, and exit
                # the inner loop
                elif change_ipt == "random":
                    key = makeRandomKey()
                    cipher.setKey(key)
                    print("    New cipher key:", cipher.getKey(), "\n")
                    break

                # If the user inputs anything else, check if it is a valid key
                else:

                    # If the key is valid, change the key, display the new key and
                    # exit the inner loop
                    if isLegalKey(change_ipt):
                        cipher.setKey(change_ipt)
                        print("    New cipher key:", cipher.getKey(), "\n")
                        break

                    # If the key is not valid, print an error message and continue the inner loop
                    else:
                        print("    Illegal key entered. Try again!")

        # Case where user inputs any case variation of encryptFile
        elif ipt == "encryptfile":
            file = input("  Enter a filename: ")

            # Check if the file exists within the current working directory
            # if not, print an error message
            if not os.path.isfile(file):
                print("File does not exist \n")

            # If the file exists, encrypt the file and print the encrypted file name
            else:
                out = generateName(file, "-Enc")
                print(
                    "The encrypted output filename is",
                    cipher.encryptFile(file, out),
                    "\n",
                )

        # Case where the user inputs any case variation of decryptFile
        elif ipt == "decryptfile":
            file = input("  Enter a filename: ")

            # Check if the inputted file exists within the current working directory
            # if not, print an error message
            if not os.path.isfile(file):
                print("File does not exist \n")

            # If the file exists, decrypt the file and print the encrypted file name
            else:
                out = generateName(file, "-Dec")
                print(
                    "The decrypted output filename is",
                    cipher.decryptFile(file, out),
                    "\n",
                )

        # If the user inputs anything besides the 5 given options, print an error message
        else:
            print("  Command not recognized. Try again! \n")


main()
