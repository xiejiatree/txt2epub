#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import pathlib
import uuid
import re

import langdetect
from ebooklib import epub


class Txt2Epub:
    def __init__(
        self,
        book_identifier=None,
        book_title=None,
        book_author=None,
        book_delineator = None,
        book_language="en",
    ):
        self.book_identifier = book_identifier or str(uuid.uuid4())
        self.book_title = book_title
        self.book_author = book_author
        self.book_language = book_language
        self.book_delineator = book_delineator

#
    def is_digit_1_to_9(s):
        pattern = r'^[1-9]$'
        return re.match(pattern, s) is not None
    
    def split(self, input_file: pathlib.Path, chapters):
        s = self.book_delineator
        valid_characters = {"一", "二", "三", "四", "五", "六", "七", "八", "九", "十"}
        with input_file.open("r", encoding="utf-8") as txt_file:
            text = txt_file.read()
            for line in text:
                chapters = text.split("/n"+line+"/n")
                '''if .is_space_separated(s)==True and len(line)>=2 and self.book_delineator(0) == line[0] and line[1] in valid_characters or self.is_digit_1_to_9(line[0]):'''
                


    def create_epub(self, input_file: pathlib.Path, output_file: pathlib.Path = None):
        # get the book title from the file namef
        book_title = self.book_title or input_file.stem

        # read text from file
        with input_file.open("r", encoding="utf-8") as txt_file:
            text = txt_file.read()
            try:
                book_language = self.book_language or langdetect.detect(text)
            except langdetect.lang_detect_exception.LangDetectException:
                book_language = "en"

        # split text into chapters
        chapters = None
        self.split(input_file, chapters)

        # create new EPUB book
        book = epub.EpubBook()

        # set metadata
        book.set_identifier(self.book_identifier)
        book.set_title(book_title)
        book.set_language(book_language)
        book.add_author(self.book_author or "Unknown")

        # create chapters
        spine = ["nav"]
        toc = []
        for chapter_id, chapter_content_full in enumerate(chapters):
            chapter_lines = chapter_content_full.split("\n")
            chapter_title = chapter_lines[0]
            chapter_content = chapter_lines[1:]

            # write chapter title and contents
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name="chap_{:02d}.xhtml".format(chapter_id + 1),
                lang=book_language,
            )
            chapter.content = "<h1>{}</h1>{}".format(
                chapter_title,
                "".join("<p>{}</p>".format(line) for line in chapter_content),
            )

            # add chapter to the book and TOC
            book.add_item(chapter)
            spine.append(chapter)
            toc.append(chapter)

        # update book spine and TOC
        book.spine = spine
        book.toc = toc

        # add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # generate new file path if not specified
        if output_file is None:
            output_file = input_file.with_suffix(".epub")

        # create EPUB file
        epub.write_epub(output_file, book)

'''        def is_space_separated():
            if(self[0]=="\n" and self[len(s)-1]=="\n"):
                return(1)
'''
