## simplenote\_blog\_converter

 This code prepares notes on Simplenote as blog posts (served by [local-blog]).

    usage: simplenote_blog_converter.py [-h] [--user USER] [--password PASSWORD]
                                        [--published-tag PUBLISHED_TAG]
                                        [--extension EXTENSION]
                                        target_folder
    
    positional arguments:
      target_folder         Specify the folder to store the blog posts in.
    
    optional arguments:
      -h, --help            show this help message and exit
      --user USER, -u USER  The email address of the Simplenote user.
      --password PASSWORD, -p PASSWORD
                            If not stated, you will be asked for it.
      --published-tag PUBLISHED_TAG, -t PUBLISHED_TAG
                            The tag to decide if the post should be included
      --extension EXTENSION
                            The file extension for the posts (.mdtxt)

[local-blog]: https://github.com/pklaus/local-blog
