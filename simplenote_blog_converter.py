#!/usr/bin/env python

import simplenote
import unidecode

import os, json, re
from datetime import date, datetime as dt

try:
    input
except:
    input = raw_input

post_fmt = """
# {title}

* Status: {status}
* Categories: {categories}
* Tags: {tags}
* Creation Date: {creation_date}
* Modification Date: {modification_date}
* Slug: {slug}

### Content

{content}
""".strip()


def main():
    import argparse, getpass
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', '-u', help='The email address of the Simplenote user.')
    parser.add_argument('--password', '-p', help='If not stated, you will be asked for it.')
    parser.add_argument('--published-tag', '-t', default='published', help='The tag to decide if the post should be included')
    parser.add_argument('--extension', default='.mdtxt', help='The file extension for the posts (.mdtxt)')
    parser.add_argument('target_folder',
        help="Specify the folder to store the blog posts in. ")
    args = parser.parse_args()
    d = date.today().isoformat()
    datetime = dt.now().replace(microsecond=0).isoformat().replace(':', '-')
    print(args)
    args.target_folder = os.path.expanduser(args.target_folder)
    if not args.user:
        args.user = input('Simplenote username: ')
    if not args.password:
        args.password = getpass.getpass()
    backup(args.target_folder, args.user, args.password, ext=args.extension, pub_tag=args.published_tag)

def slugify(title):
    return re.sub(r'\W+', '-', str(unidecode.unidecode(title)).lower()).strip(' -')

def backup(folder, user, password, ext='.mdtxt', pub_tag='published', **kwargs):
    os.makedirs(folder, exist_ok=True)
    sn = simplenote.Simplenote(user, password)
    note_list = sn.get_note_list()
    note_list = note_list[0]
    for i, note in enumerate(note_list):
        print("Processing note {} of {}.".format(i, len(note_list)))
        if note['deleted']: continue
        if pub_tag not in note['tags']: continue
        individual_note = sn.get_note(note['key'])
        individual_note = individual_note[0]
        note_path_md = os.path.join(folder, note['key'] + ext)
        data = {}
        tags = [tag for tag in individual_note['tags'] if not tag.startswith('category_')]
        tags = [tag for tag in tags if tag != pub_tag]
        categories = [tag.partition('category_')[2] for tag in individual_note['tags'] if tag.startswith('category_')]
        content = individual_note['content'].strip().split('\n')
        data['title'] = content[0].lstrip('# ')
        data['content'] = '\n'.join(content[1:])
        creation_date = dt.utcfromtimestamp(float(individual_note['createdate']))
        modification_date = dt.utcfromtimestamp(float(individual_note['modifydate']))
        creation_date = creation_date.replace(microsecond=0)
        modification_date = modification_date.replace(microsecond=0)
        data['categories'] = ' '.join(categories)
        data['tags'] = ' '.join(tags)
        data['status'] = 'published'
        data['slug'] = slugify(data['title'])
        data['creation_date'] = creation_date.isoformat(' ')
        data['modification_date'] = modification_date.isoformat(' ')
        md_content = post_fmt.format(**data)
        with open(note_path_md, 'w') as f:
            f.write(md_content)

if __name__ == "__main__":
    main()
