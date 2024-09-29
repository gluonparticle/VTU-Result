import os
import logging

# Configure logging to output to both the console and a file
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler('output.txt')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)

def print_directory_tree(root_dir, prefix=""):
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        logger.info('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            logger.info('{}{}'.format(sub_indent, f))

def output_file_contents(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir)
            logger.info(f"\nFile: {relative_path}")
            logger.info("-" * 80)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logger.info(content)
            except (UnicodeDecodeError, IOError) as e:
                logger.info(f"Error reading {relative_path}: {e}")
            logger.info("-" * 80)

def main():
    root_dir = '/home/gluonparticle/Projects/Result-Analysis/References/VTU-Result_Scraper-CAPTCHA_Bypass-main'  # Change this to your root directory

    logger.info("Directory Tree:")
    print_directory_tree(root_dir)

    logger.info("\nOutputting file contents...")
    output_file_contents(root_dir)
    logger.info("Done.")

if __name__ == "__main__":
    main()