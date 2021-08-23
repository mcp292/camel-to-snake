# AUTHOR: Michael Partridge <mcp292@nau.edu>
#
# USAGE: camel_to_snake IN_FILE -o OUT_FILE

import argparse


def get_default_out_file(in_file):
    SEPARATOR = '.'
    DISTINCTION = "_snake"

    in_file_split = in_file.split(SEPARATOR)

    if len(in_file_split) == 1:
        # no extension given
        file_base = in_file_split[0]
        file_ext = ""
    elif len(in_file_split) == 2:
        # one period in filename; as it should be
        file_base = in_file_split[0]
        file_ext = in_file_split[1]
    elif len(in_file_split) > 2:
        # periods in file name base
        file_ext = in_file_split[-1]

        file_base = ""
        for item in in_file_split:
            if item is not file_ext: # if not last element
                file_base += item + SEPARATOR

        # NOTE: this algorithm is actually slower;
        # see https://github.com/mcp292/find-last for timings
        # file_base = ""
        # for ind in range(len(in_file_split) - 1): # skip last element
        #     file_base += in_file_split[ind] + SEPARATOR

    return file_base + DISTINCTION + SEPARATOR + file_ext


def convert_word(line, ind):     # TODO: handle nums
    converted_word = ""

    while ind < len(line):
        char = line[ind]

        if char.isupper():      # implicit isalpha()
            converted_word += '_'
            converted_word += char.lower()
            # no need to increment ind further because it maps to the
            # orignal line which is unchanged
        elif char.islower() or char.isalnum():
            # write as-is (lowercase and digits)
            converted_word += char
        elif not char.isalnum():
            # word boundary exceeded
            # return character to be parsed (unget char)
            ind -= 1
            break

        # update
        ind += 1

    return converted_word, ind


def get_word(line, ind):
    word = ""

    while ind < len(line):
        char = line[ind]

        if char.isalnum():
            word += char
        else:
            # word boundary exceeded
            # return character to be parsed (unget char)
            ind -= 1
            break

        # update
        ind += 1

    return word, ind


def main():
    parser = argparse.ArgumentParser(description="This script converts a "
                                     "camelCase file to snake_case.")
    parser.add_argument("in_file")
    parser.add_argument("-o", "--out_file", help="The file to write to. If not "
                        "provided, appends \"_snake\" to file base.")

    args = parser.parse_args()

    # handle default output file
    if args.out_file == None:
        args.out_file = get_default_out_file(args.in_file)

    in_file = open(args.in_file, "r")
    out_file = open(args.out_file, "w")

    # convert to snake case line by line until EOF encountered ("")
    line = in_file.readline()
    while line != "":
        ind = 0
        while ind < len(line):
            char = line[ind]

            if char.isalpha() and char.islower():
                word, ind = convert_word(line, ind)
                out_file.write(word)
            elif char.isalpha() and char.isupper():
                word, ind = get_word(line, ind)
                out_file.write(word)
            else:
                # accounts for '\n', operators, literals, etc.
                out_file.write(char)

            # update
            ind += 1

        # update
        line = in_file.readline()

    in_file.close()
    out_file.close()


if __name__ == "__main__":
    main()
