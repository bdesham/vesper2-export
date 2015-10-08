#!/usr/bin/env python
#
# vesper2-export
# https://github.com/bdesham/vesper2-export
#
# Copyright (c) Benjamin Esham, 2015
# See README.md for full copyright information.

from __future__ import print_function
from argparse import ArgumentParser
from errno import EEXIST
from os import makedirs
from os.path import abspath, expanduser, isdir, join
from shutil import copy2
import sqlite3

def mkdir_p(path):
	try:
		makedirs(path)
	except OSError as exc:
		if exc.errno == EEXIST and isdir(path):
			pass
		else:
			raise

def filename_from_first_line(text):
	result = ''
	for word in text.split(' '):
		result += word + ' '
		if len(result) >= 32:
			break

	# Omit characters that are illegal (or ill-advised) in paths
	result = result.replace(':', '-')
	result = result.replace('/', '-')

	# Get rid of the trailing space if there is one
	if result[-1] == ' ':
		return result[:-1]
	else:
		return result

def export_notes(input_directory, output_directory):
	mkdir_p(output_directory)
	mkdir_p(join(output_directory, 'Archive'))

	connection = sqlite3.connect(join(input_directory, 'Vesper2-Notes.sqlite3'))
	cursor = connection.cursor()

	cursor.execute('''SELECT uniqueID, text, archived
		FROM notes
		ORDER BY sortDate DESC''')
	notes = cursor.fetchall()

	archived_index = 1
	unarchived_index = 1

	for note in notes:
		uniqueID, text, archived = note

		cursor.execute('''SELECT name
			FROM tags
			LEFT JOIN tagsNotesLookup ON tagsNotesLookup.tagID=tags.uniqueID
			WHERE tagsNotesLookup.noteID=?
			ORDER BY ix''', (uniqueID,))
		tags_text = ', '.join([t[0] for t in cursor.fetchall()])

		text_for_filename = filename_from_first_line(text.splitlines()[0])

		if archived:
			filename_with_number = '{} {}'.format(archived_index, text_for_filename.encode('utf-8'))
			basename = join('Archive', filename_with_number)
			archived_index += 1
		else:
			filename_with_number = '{} {}'.format(unarchived_index, text_for_filename.encode('utf-8'))
			basename = join(filename_with_number)
			unarchived_index += 1

		text_file_path = basename + '.txt'
		with open(join(output_directory, text_file_path), 'w') as f:
			f.write(text.encode('utf-8'))
			if tags_text != '':
				f.write('\n\nTags: ' + tags_text)
			f.write('\n')
		print('Wrote file "' + text_file_path + '"')

		cursor.execute('''SELECT uniqueID, mimeType
			FROM attachments
			LEFT JOIN attachmentsNotesLookup ON attachmentsNotesLookup.attachmentID=attachments.uniqueID
			WHERE attachmentsNotesLookup.noteID=?
			LIMIT 1''', (uniqueID,))
		attachment = cursor.fetchone()
		if attachment is not None:
			uuid, mime_type = attachment

			source_path = join(input_directory, 'Attachments', uuid)
			if mime_type == 'image/png':
				extension = '.png'
			elif mime_type == 'image/gif':
				extension = '.gif'
			elif mime_type == 'image/tiff':
				extension = '.tiff'
			else:
				extension = '.jpeg'

			image_file_path = basename + extension
			copy2(source_path, join(output_directory, image_file_path))
			print('Copied image "' + image_file_path + '"')


if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('input_directory',
		help='The directory containing the Vesper database and the Attachments directory')
	parser.add_argument('output_directory', help='The directory where the exported files will go')
	args = parser.parse_args()

	export_notes(abspath(expanduser(args.input_directory)), abspath(expanduser(args.output_directory)))
