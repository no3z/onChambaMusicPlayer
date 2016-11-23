import random
import re
 
# We want to be able to process some command line options.
from optparse import OptionParser
 
def process_lines(options, all_lines):
  'process the list of all playlist lines into three chunks'
  # Eventually we want to support several formats
  m3u = True
  extm3u = False
  if options.verbose:
    print "Read %u lines..." % len(all_lines)
  header = list()
  middle = list()
  footer = list()
  
  # Check first line for #EXTM3U
  if re.match("^#EXTM3U$", all_lines[0]):
    if options.verbose:
      print "EXTM3U format file..."
    extm3u = True
    header.append(all_lines[0])
    del all_lines[0]
  
  loop = 0
  while loop < len(all_lines):
    # Each 'item' may be multiline
    item = list()
    if re.match("^#EXTINF.*$", all_lines[loop]):
      item.append(all_lines[loop])
      loop = loop + 1
    # A proper regexp for filenames would be good
    if loop < len(all_lines):
      item.append(all_lines[loop])
      loop = loop + 1
    if options.verbose: print item
    middle.append(item)
            
  return (header, middle, footer)
 
def load_playlist(options):
  'loads the playlist into an array of arrays'
  if options.verbose:
    print "Reading playlist %s ..." % options.in_filename
  with open(options.in_filename, 'r') as file:
    all_lines = file.readlines()
  (header, middle, footer) = process_lines(options, all_lines)
  return (header, middle, footer)
 
def write_playlist(options, header, middle, footer):
  'writes the shuffled playlist'
  if options.verbose:
    print "Writing playlist %s ..." % options.out_filename
  with open(options.out_filename, 'w') as file:
    for line in header:
      file.write(line)
    for item in middle:
      for line in item:
        file.write(line)
    for line in footer:
      file.write(line)
 
 
def shuffle(options):
  'perform the shuffle on the playlist'
  # read the existing data into three arrays in a tuple
  (header, middle, footer) = load_playlist(options)
  # and shuffle the lines array
  if options.verbose:
    print "Shuffling..."
  random.shuffle(middle)
  # now spit them back out
  write_playlist(options, header, middle, footer)
 
def print_banner():
  print "playlist-shuffle"
 
def main():
  'the main function that kicks everything else off'
  
  usage = "usage: %prog [options] arg"
  parser = OptionParser(usage)
  parser.add_option("-i", "--input-file", dest="in_filename",
                    help="read playlist from FILENAME")
  parser.add_option("-o", "--output-file", dest="out_filename",
                    help="write new playlist to FILENAME")
  parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose")
  parser.add_option("-q", "--quiet", default=False,
                    action="store_true", dest="quiet")
                    
  (options, args) = parser.parse_args()
#  if len(args) == 0:
#      parser.error("use -h for more help")
  
  if not options.quiet:
    print_banner()
  
  shuffle(options)
  
  if not options.quiet:
      print "Playlist shuffle complete..."
  
 
if  __name__ == '__main__':
  main()

