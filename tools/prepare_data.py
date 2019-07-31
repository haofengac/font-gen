import os
from tqdm import tqdm
import argparse
import shutil
from gftools.fonts_public_pb2 import FamilyProto
from google.protobuf import text_format


def parse_args():
    parser = argparse.ArgumentParser(description='Prepare Google Fonts data')
    parser.add_argument(
          "-l", "--license",
          default="all",
          help="filter fonts by license",
    )
    parser.add_argument(
          "-o", "--out-dir",
          default="data/google-fonts",
          help="path to save the Google Fonts dataset",
    )
    parser.add_argument(
          "-i", "--in-dir",
          default="data/fonts-master",
          help="path of the decompressed fonts folder",
    )
    return parser.parse_args()


def mkdir(dir):

	if not os.path.exists(dir):
		os.makedirs(dir)


if __name__ == '__main__':

	args = parse_args()

	license_sets = []
	if args.license == 'all':
		license_sets = ['apache', 'ofl', 'ufl']
	elif args.license == 'apache':
		license_sets = ['apache']
	elif args.license == 'ofl':
		license_sets = ['ofl']
	elif args.license == 'ufl':
		license_sets = ['ufl']

	category_dict = {}
	for license_set in license_sets:

		license_dir_in = os.path.join(args.in_dir, license_set)

		for font_fam in os.listdir(license_dir_in):

			font_dir_in = os.path.join(license_dir_in, font_fam)
			if not os.path.isdir(font_dir_in):
				continue

			# FIXME: check missing metadata files
			if not os.path.exists(os.path.join(font_dir_in, 'METADATA.pb')):
				continue

			# check category
			with open(os.path.join(font_dir_in, 'METADATA.pb')) as f:
				metadata = FamilyProto()
				text_data = f.read()

			text_format.Merge(text_data, metadata)
			
			if not metadata.category in category_dict.keys():
				category_dict[metadata.category] = []

			category_dict[metadata.category] += ['{}/{}'.format(license_set, font_fam)]

	print('Font Summary:')
	print({k: len(v) for k, v in category_dict.items()})

	mkdir(args.out_dir)
	for category in category_dict.keys():

		print('Saving category {}...'.format(category))
		category_dir = os.path.join(args.out_dir, category)
		mkdir(category_dir)

		for font_path in tqdm(category_dict[category]):
			font_dir_in = os.path.join(args.in_dir, font_path)
			font_dir_out = os.path.join(category_dir, font_path.split('/')[-1])
			mkdir(font_dir_out)

			for fn in os.listdir(font_dir_in):
				if fn == 'METADATA.pb' or fn.endswith('.ttf'):
					shutil.copyfile(
						os.path.join(font_dir_in, fn),
						os.path.join(font_dir_out, fn)
						)

				if fn.endswith('.ttf'):
					svg_dir = os.path.join(font_dir_out, fn.split('.')[0])
					mkdir(svg_dir)

					# convert ttf to svg
					cmd = "cd {}; fontforge -lang=ff -c 'Open(\"{}\"); SelectWorthOutputting(); foreach Export(\"svg\"); endloop;'>/dev/null 2>&1;".format(
						os.path.abspath(svg_dir),
						os.path.abspath(os.path.join(font_dir_out, fn))
						)
					os.system(cmd)

