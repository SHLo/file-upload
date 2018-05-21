"""Modules for pre-processing original NDA documents"""
from docx import Document
import pandas as pd
import os
import sys
import re

commands = {
    0: "NDAParser",
    1: "TextPreprocessor"
}


class BasicFileIO:
    def __init__(self):
        return

    def save_df_to_csv(self, df, filename):
        """
        Save a DataFrame to a csv file.

        :param df: DataFrame
        :param filename: the output file name
        :return: None
        """
        df.to_csv(filename, index=False, encoding="utf-8")


class NDAParser(BasicFileIO):
    def __init__(self):
        BasicFileIO.__init__(self)
        return

    def parse_doc_to_df(self, path):
        """
        Parse a NDA in doc/docx format into a pandas DataFrame.
        The path could be a file or directory that contains the NDA files.
        The NDA will be parsed into paragraph level.

        :param path: file/directory
        :return: DataFrame
        """
        if os.path.isfile(path):
            filename = os.path.basename(path)
            doc = Document(path)

            d = []
            i = 1
            for para in doc.paragraphs:
                if para.text.strip():
                    d.append({"0": filename, "1": None, "2": i, "3": para.text})
                    i += 1

            df = pd.DataFrame(d)
            df.columns = ['File_Name', 'Article_No', 'Paragraph_No', 'Clause']
            df = self.extract_article_no(df)
            return df

        elif os.path.isdir(path):
            df = pd.DataFrame(columns=['File_Name', 'Article_No', 'Paragraph_No', 'Clause'])
            for p in os.listdir(path):
                df.append(self.parse_doc_to_df(p))

            return df

        else:
            raise Exception(path + " is not a file or dir")

    def extract_article_no(self, df):
        """
        Extract the article no and assign it to each paragraph.

        :param df: DataFrame
        :return: A new DataFrame with article no assigned
        """
        i = 0
        old_article_no = ''
        article_no = ''
        # Article starts with list number like "1.", "2.", etc.
        rule = re.compile(r"[0-9]+\.[ \t]+")
        for index, row in df.iterrows():
            if len(re.findall(rule, row['Clause'])) > 0:
                article_no = re.findall(rule, row['Clause'])[0]
            if old_article_no == article_no:
                df.at[index, 'Article_No'] = i
            else:
                i += 1
                df.at[index, 'Article_No'] = i
                old_article_no = article_no

        df = df.loc[df['Article_No'] != 0]
        return df


class TextPreprocessor(BasicFileIO):
    def __init__(self):
        BasicFileIO.__init__(self)
        return

    def parse_csv_to_df(self, path):
        """
        Parse a csv file into a pandas DataFrame.
        The path could only be a file.

        :param path: file
        :return: DataFrame
        """
        if os.path.isfile(path):
            df = pd.read_csv(path, encoding="ISO-8859-1")
            return df

        else:
            raise Exception(path + " is not a file")

    def consolidate_by_article(self, df):
        """
        Concatenate all paragraphs under the same article.

        :param df: DataFrame contained the parsed NDA
        :return: A new DataFrame concatenate paragraphs by article.
        """
        df = df.loc[:, ['File_Name', 'Article_No', 'Clause']].groupby(['File_Name', 'Article_No'])['Clause'].apply(
            lambda x: "%s" % ' '.join(x)).reset_index()
        return df

    def remove_punctuation_df(self, df, columns=None):
        """
        Remove the punctuation in a DataFrame for the specified columns.

        :param df: DataFrame
        :param columns: list of columns need to remove punctuation
        :return: A new DataFrame with punctuation removed
        """
        if columns is None:
            columns = df.columns
        for col in columns:
            df[col] = df[col].map(lambda x: self.remove_punctuation(x))

        return df

    def remove_punctuation(self, text):
        """
        Remove the defined punctuation in a text string.

        :param text: A text string
        :return: A new text string with punctuation removed
        """

        # Remove all list number like (a), (i), (1)
        rule = re.compile(r"\((\d+|\w+)\)")
        text = rule.sub('', text)

        # Remove all list number like 1.1, 1.1.1
        rule = re.compile(r"[0-9]+\.[0-9 \t]*\.*")
        text = rule.sub('', text)

        # Remove all remaining punctuation
        rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5 ]")
        text = rule.sub('', text)
        return text


def print_usage(argv):
    print("Usage: python {0} {1}".format(argv[0], "<command>"))
    print("Candidate Commands: {0}, {1}\n".format("NDAParser", "TextPreprocessor"))
    print("Detail Usage:")
    print_nda_parser_usage(argv)
    print_text_preprocessor_usage(argv)


def print_nda_parser_usage(argv):
    print("Usage: python {0} NDAParser {1} {2}".format(argv[0], "<input_path>", "<output_path>"))


def print_text_preprocessor_usage(argv):
    print("Usage: python {0} TextPreprocessor {1} {2} {3}".format(argv[0], "<input_path>", "<output_path>",
                                                          "<article|paragraph>"))


def main():
    """
    The entry point when running this script as a standalone application.

    Usage: python preprocess.py <command>
    Candidate Commands: NDAParser, TextPreprocessor
    1. NDAParser accepts a doc/docx as input and save the parsed result into a csv file.
    2. TextPreprocessor accepts the output from an NDAParser and conducts text pre-processing on the extracted Clauses.
    The result can be grouped to article or paragraph.

    Detail Usage:
    Usage: python preprocess.py NDAParser <input_path> <output_path>
    Usage: python preprocess.py TextPreprocessor <input_path> <output_path> <article|paragraph>
    :return:
    """

    if len(sys.argv) < 2:
        print_usage(sys.argv)
        return

    # NDAParser
    if sys.argv[1] == commands[0]:
        if len(sys.argv) < 4:
            print_nda_parser_usage(sys.argv)
            return

        if not os.path.isdir(sys.argv[3]):
            print_nda_parser_usage(sys.argv)
            print("<output_path> must be a directory")
            return

        nda_parser = NDAParser()
        df = nda_parser.parse_doc_to_df(sys.argv[2])
        nda_parser.save_df_to_csv(df, os.path.join(sys.argv[3], "NDA_parsed_result.csv"))

    # TextPreprocessor
    elif sys.argv[1] == commands[1]:

        if len(sys.argv) < 5:
            print_text_preprocessor_usage(sys.argv)
            return

        if not os.path.isdir(sys.argv[3]):
            print_text_preprocessor_usage(sys.argv)
            print("<output_path> must be a directory")
            return

        mode = sys.argv[4]

        if mode == "article" or mode == "paragraph":
            text_preprocessor = TextPreprocessor()
            df = text_preprocessor.parse_csv_to_df(sys.argv[2])
            if mode == "article":
                df = text_preprocessor.consolidate_by_article(df)
            df = text_preprocessor.remove_punctuation_df(df, ["Clause"])
            text_preprocessor.save_df_to_csv(df, os.path.join(sys.argv[3], "text_preprocessed_result.csv"))
        else:
            print_text_preprocessor_usage(sys.argv)
            print("The final argument can only be article or paragraph")
            return

    else:
        print("No Command found: {0}".format(sys.argv[0]))
        print_usage(sys.argv)
        return

if __name__ == "__main__":
    main()


